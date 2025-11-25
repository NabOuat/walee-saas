import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction # Utile pour garantir deux operations indissociable
from django.conf import settings # Importation essentielle pour recuperer les variables
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from .supabase_service import proxy_to_supabase # Utilitaire de verification d'Authentification Bearer avant toute requete vers la base
import logging
# Importation des models
from .models import Utilisateurs
from .serializers import *


SUPABASE_URL = settings.SUPABASE_URL
SUPABASE_ANON_KEY = settings.SUPABASE_ANON_KEY
logger = logging.getLogger(__name__)

###### API VIEWS
class InscriptionPartenaireAPIView(APIView):
    # Cet endpoint n'a pas besoin d'authentification DRF car il crée le compte
    permission_classes = [] 
    throttle_scope = "auth_signup"

    def post(self, request):
        data = request.data
        email = data.get('email')
        password = data.get('password')
        nom_complet = data.get('nom_complet', '')
        telephone = data.get('telephone', '')

        # Validations minimales des champs requis
        if not email or not password:
            return Response(
                {"detail": "L'email et le mot de passe sont requis."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Validation basique du format d'email
        try:
            validate_email(email)
        except ValidationError:
            return Response(
                {"detail": "L'adresse email fournie est invalide."},
                status=status.HTTP_400_BAD_REQUEST
            )
        # redirect_url = f"{settings.FRONTEND_URL}/login" # URL de redirection après vérification email
        redirect_url = f"http://localhost:8000/login" # URL de redirection après vérification email
        supabase_payload = {
            "email": email,
            "password": password,
            "options": {
                "should_create_user": True, # False :Effectue une verification OTP avant la creation du compte et n'utilise pas email_redirect_to
                "email_redirect_to" : redirect_url  # URL de redirection apres verification email
            }
        }
        
        headers = {
            "apikey": SUPABASE_ANON_KEY,
            "Content-Type": "application/json"
        }

        try:
            SUPABASE_AUTH_URL = f"{SUPABASE_URL}/auth/v1/signup"
            with transaction.atomic():
                # Appel à l'API Supabase pour l'inscription
                auth_response = requests.post(SUPABASE_AUTH_URL, json=supabase_payload, headers=headers)
                auth_response.raise_for_status() # Lève une exception si le statut HTTP est un échec (4xx ou 5xx)

                supabase_user_data = auth_response.json()
                print("Données utilisateur Supabase lors de l'inscription:", supabase_user_data)
                # Certains flux Supabase (OTP / email confirmation) peuvent ne pas retourner 'user'
                supabase_user_id = supabase_user_data.get("id") if isinstance(supabase_user_data, dict) else None
                print("ID Utilisateur Supabase:", supabase_user_id)
                if supabase_user_id:
                    # Creation du profil utilisateur dans la table locale uniquement si on a un id
                    Utilisateurs.objects.create(
                        id = supabase_user_id,
                        nom_complet = nom_complet,
                        email = email,
                        telephone = telephone
                    )
            return Response ({
                "success": True,
                "message": "Inscription réussie.",
                "email" : email
            }, status=status.HTTP_201_CREATED)
            
        except requests.exceptions.HTTPError as e:
            print("Erreur HTTP lors de l'inscription Supabase:", str(e))
            # Gérer les erreurs de Supabase (ex: utilisateur déjà enregistré)
            return Response({"detail": "Erreur Supabase Auth: " + str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as e:
            print("Erreur interne lors de l'inscription Supabase:", str(e))
            return Response({"detail": "Erreur interne lors de l'appel Supabase: " + str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class LoginPartenaireAPIView(APIView):
    # Cet endpoint n'a pas besoin d'authentification DRF car il crée le compte
    permission_classes = [] 
    throttle_scope = "auth_login"

    def post(self, request):
        data = request.data
        loginMethod = data.get('loginMethod') # email ou phone
        email = data.get('email')
        phone = data.get('telephone')
        password = data.get('password')

        if loginMethod not in ['email', 'phone']:
            return Response({"detail": "loginMethod doit être 'email' ou 'phone'."}, 
                   status=status.HTTP_400_BAD_REQUEST)

        if loginMethod == 'email' and (not email or not password):
            return Response (
                {"detail": "L'email et le mot de passe sont requis."},
                status= status.HTTP_400_BAD_REQUEST
            )
        
        if loginMethod == "phone" and (not phone or not password) :
            return Response (
                {"detail": "Le numéro et le mot de passe sont requis."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        supabase_payload = {
            "email": email,
            "password": password
        } if loginMethod == "email" else {"phone":phone, 
                                          "password": password}
        
        headers = {
            "apikey": SUPABASE_ANON_KEY,
            "Content-Type": "application/json"
        }

        try:
            SUPABASE_AUTH_URL = f"{SUPABASE_URL}/auth/v1/token?grant_type=password"
            # Appel à l'API Supabase pour la connexion
            login_response = requests.post(SUPABASE_AUTH_URL, json=supabase_payload, headers=headers)
            login_response.raise_for_status() # Lève une exception si le statut HTTP est un échec (4xx ou 5xx)

            session_data = login_response.json()
            print("Données de session Supabase:", session_data)
            
            logger.debug(f"Session data: {session_data}")
            # Retourner simplement le token sans créer d'utilisateur local
            # L'utilisateur local sera créé lors de la première inscription
            return Response ( 
                {"success": True,
                 "message" : "Connexion réussie.",
                 "access_token" : session_data.get("access_token"),
                 "refresh_token" : session_data.get("refresh_token"),
                 "user": session_data.get("user")
                 },
                 status=status.HTTP_200_OK
            )
            
        except requests.exceptions.HTTPError as e:
            # Gérer les erreurs de Supabase (ex: identifiants invalides)
            # error_message = "Email ou mot de passe invalide."

            return Response({"detail": "L'adresse email/ téléphone ou le mot de passe est incorrect."}, 
                            status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as e:
            return Response({"detail": "Erreur interne lors de l'authentification: " + str(e)}, 
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class VerifyOtpAPIView(APIView):
    """Vérification OTP logique côté frontend :

    Option A2 : on s'appuie sur Supabase pour valider le couple email/téléphone + mot de passe,
    le code OTP saisi dans le front n'est pas encore vérifié côté Django (il est supposé géré
    via le flux Supabase ou utilisé uniquement à des fins d'UX en DEV).
    """
    permission_classes = []
    throttle_scope = "auth_verify_otp"

    def post(self, request):
        data = request.data
        email = data.get('email')
        phone = data.get('telephone')
        code = data.get('code')  # Actuellement non utilisé côté backend (option A2)
        password = data.get('password')

        # Validations minimales
        if not password:
            return Response(
                {"success": False, "message": "Le mot de passe est requis."},
                status=status.HTTP_400_BAD_REQUEST
            )

        if not email and not phone:
            return Response(
                {"success": False, "message": "Un email ou un téléphone est requis."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Préparer payload pour Supabase (même logique que LoginPartenaireAPIView)
        login_method = 'phone' if phone and not email else 'email'
        supabase_payload = (
            {"email": email, "password": password}
            if login_method == 'email'
            else {"phone": phone, "password": password}
        )

        headers = {
            "apikey": SUPABASE_ANON_KEY,
            "Content-Type": "application/json",
        }

        try:
            SUPABASE_AUTH_URL = f"{SUPABASE_URL}/auth/v1/token?grant_type=password"
            login_response = requests.post(SUPABASE_AUTH_URL, json=supabase_payload, headers=headers)
            login_response.raise_for_status()

            session_data = login_response.json()

            access_token = session_data.get("access_token")
            refresh_token = session_data.get("refresh_token")
            user_data = session_data.get("user") or {}
            user_id = user_data.get("id")

            # Création/mise à jour du profil local Utilisateurs
            if user_id:
                utilisateur, _ = Utilisateurs.objects.update_or_create(
                    id=user_id,
                    defaults={
                        "email": user_data.get("email", email),
                        "nom_complet": user_data.get("user_metadata", {}).get("nom_complet", ""),
                        "telephone": phone or "",
                        "actif": True,
                    },
                )
            else:
                utilisateur = None

            utilisateur_payload = None
            if utilisateur is not None:
                utilisateur_payload = {
                    "id": str(utilisateur.id),
                    "email": utilisateur.email,
                    "nom_complet": utilisateur.nom_complet,
                    "telephone": utilisateur.telephone,
                }

            return Response(
                {
                    "success": True,
                    "data": {
                        "access_token": access_token,
                        "refresh_token": refresh_token,
                        "utilisateur": utilisateur_payload or user_data,
                    },
                },
                status=status.HTTP_200_OK,
            )

        except requests.exceptions.HTTPError as e:
            return Response(
                {
                    "success": False,
                    "message": "Code / identifiants invalides ou non vérifiés.",
                    "detail": str(e),
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Exception as e:
            return Response(
                {
                    "success": False,
                    "message": "Erreur interne lors de la vérification du code.",
                    "detail": str(e),
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class ProfilePartenaireAPIView(APIView):
    # Cet endpoint nécessite une authentification DRF
    permission_classes = [] 

    def get(self, request):
        # Récupérer le token d'accès depuis les en-têtes de la requête
        auth_header = request.headers.get('Authorization', '')

        if not auth_header:
            return Response({"detail": "En-tête Authorization manquant."}, status=status.HTTP_401_UNAUTHORIZED)

        if not auth_header.startswith('Bearer '):
            return Response({"detail": "Format de l'en-tête Authorization invalide. Attendu: 'Bearer <token>'."}, status=status.HTTP_401_UNAUTHORIZED)

        access_token = auth_header.split(' ', 1)[1].strip()

        if not access_token:
            return Response({"detail": "Token d'accès manquant."}, status=status.HTTP_401_UNAUTHORIZED)

        headers = {
            "apikey": SUPABASE_ANON_KEY,
            "Authorization": f"Bearer {access_token}"
        }

        try:
            SUPABASE_USER_URL = f"{SUPABASE_URL}/auth/v1/user"
            # Appel à l'API Supabase pour récupérer le profil utilisateur
            user_response = requests.get(SUPABASE_USER_URL, headers=headers)
            user_response.raise_for_status() # Lève une exception si le statut HTTP est un échec (4xx ou 5xx)

            user_data = user_response.json()
            user_id = user_data.get("id")
            
            # Chercher aussi les données locales (nom_complet, etc.)
            utilisateur_local = None
            if user_id:
                try:
                    utilisateur_local = Utilisateurs.objects.get(id=user_id)
                except Utilisateurs.DoesNotExist:
                    utilisateur_local = None
            
            # Fusionner les données : Supabase + données locales
            if utilisateur_local:
                user_data["nom_complet"] = utilisateur_local.nom_complet
                user_data["telephone"] = utilisateur_local.telephone
            
            return Response ( 
                {"success": True,
                 "user": user_data
                 },
                 status=status.HTTP_200_OK
            )
            
        except requests.exceptions.HTTPError as e:
            # Gérer les erreurs de Supabase (ex: token invalide)
            return Response({"detail": "Erreur lors de la récupération du profil: " + str(e)}, 
                            status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as e:
            return Response({"detail": "Erreur interne lors de la récupération du profil: " + str(e)}, 
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class OrganisationAPIView(APIView):
    """
    Gère la liste (GET), la création (POST) et les opérations de détail 
    (GET, PATCH, DELETE) pour les organisations.
    """

    # --- LISTE (GET) et CRÉATION (POST) ---

    def get(self, request):
        """Récupère la liste des organisations."""
        data, status_code = proxy_to_supabase('GET', request)
        return Response(data, status=status_code)

    def post(self, request):
        """Crée une nouvelle organisation."""
        serializer = OrganisationsSerializer(data=request.data)
        print("Données reçues pour création d'organisation:", request.data)
        if serializer.is_valid():
            # Le serializer valide les données, le proxy les envoie
            data, status_code = proxy_to_supabase('POST', request, data=serializer.validated_data)
            return Response({
                "success": True,
                "message": "Organisation créée avec succès.",
                "data": data
            }, status=status_code)
        
        return Response({
            "sucess": False,
            "message":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


    # --- DÉTAIL (GET, PATCH, DELETE) ---
    # Nous utilisons les méthodes ci-dessous pour gérer les opérations DETAIL sur une instance unique.
    # Note: L'URL doit être configurée avec un paramètre (pk).

    def patch(self, request, pk):
        """Met à jour partiellement une organisation (requiert l'ID dans l'URL)."""
        serializer = OrganisationsSerializer(data=request.data, partial=True) 
        if serializer.is_valid():
            data, status_code = proxy_to_supabase('PATCH', request, pk=pk, data=serializer.validated_data)
            return Response(data, status=status_code)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        """Supprime une organisation (requiert l'ID dans l'URL)."""
        data, status_code = proxy_to_supabase('DELETE', request, pk=pk)
        
        if status.is_success(status_code) or status_code == status.HTTP_204_NO_CONTENT:
            return Response(status=status.HTTP_204_NO_CONTENT)
            
        return Response(data, status=status_code)
