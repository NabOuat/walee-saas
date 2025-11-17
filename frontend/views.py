"""
Views for frontend pages (authentication and landing page)
"""
import requests
from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction # Utile pour garantir deux operations indissociable
from django.conf import settings # Importation essentielle pour recuperer les variables
import resend # Pour l'envoi d'email via Resend API
# Importation des models
from backend.walee.models import Utilisateurs

SUPABASE_URL = settings.SUPABASE_URL
SUPABASE_ANON_KEY = settings.SUPABASE_ANON_KEY

###### API VIEWS
class InscriptionPartenaireAPIView(APIView):
    # Cet endpoint n'a pas besoin d'authentification DRF car il crée le compte
    permission_classes = [] 

    def post(self, request):
        data = request.data
        email = data.get('email')
        password = data.get('password','azerty123')  # Mot de passe par defaut si non fourni
        nom_complet = data.get('nom_complet', '')
        telephone = data.get('telephone', '')

        supabase_payload = {
            "email": email,
            "password": password,
            "options": {
                "should_create_user": False, # False :Effectue une verification OTP avant la creation 
                "email_redirect_to" : "http://localhost:8000/login"  # URL de redirection apres verification email
            }
        }
        
        headers = {
            "apikey": SUPABASE_ANON_KEY,
            "Content-Type": "application/json"
        }

        try:
            SUPABASE_AUTH_URL = f"{SUPABASE_URL}/auth/v1/signup"
            # Appel à l'API Supabase pour l'inscription
            auth_response = requests.post(SUPABASE_AUTH_URL, json=supabase_payload, headers=headers)
            auth_response.raise_for_status() # Lève une exception si le statut HTTP est un échec (4xx ou 5xx)
            # print("Réponse Supabase Auth:", auth_response.json())
            # Récupérer l'ID utilisateur généré par Supabase
            supabase_user_data = auth_response.json()
            supabase_user_id = supabase_user_data['user']['id']

            # Creation du profil utilisateur dans la table locale
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
            # Gérer les erreurs de Supabase (ex: utilisateur déjà enregistré)
            return Response({"detail": "Erreur Supabase Auth: " + str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as e:
            return Response({"detail": "Erreur interne lors de l'appel Supabase: " + str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class LoginPartenaireAPIView(APIView):
    # Cet endpoint n'a pas besoin d'authentification DRF car il crée le compte
    permission_classes = [] 

    def post(self, request):
        data = request.data
        loginMethod = data.get('loginMethod') # email ou phone
        email = data.get('email')
        phone = data.get('telephone')
        password = data.get('password')

        if loginMethod == 'email' and not email or not password:
            return Response (
                {"detail": "L'email et le mot de passe sont requis."},
                status= status.HTTP_400_BAD_REQUEST
            )
        
        if loginMethod == "phone" and not phone or not password :
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
            return Response ( 
                {"success": True,
                 "message" : "Connexion réussie.",
                 "access_token" : session_data.get("access_token"),
                 "refresh_token" : session_data.get("refresh_token"),
                 "user": session_data.get("user") # Possibilité de le retirer pour y acceder seulement apres un GetProfile
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

class ProfilePartenaireAPIView(APIView):
    # Cet endpoint nécessite une authentification DRF
    permission_classes = [] 

    def get(self, request):
        # Récupérer le token d'accès depuis les en-têtes de la requête
        access_token = request.headers.get('Authorization', '').split('Bearer ')[-1]

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
            print("Réponse Supabase User:", user_response.json())

            user_data = user_response.json()
            print("Données utilisateur récupérées:", user_data)
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


# Error handlers
def error_404(request, exception):
    """Custom 404 error page"""
    return render(request, '404.html', status=404)


def error_500(request):
    """Custom 500 error page"""
    return render(request, '500.html', status=500)


class HomeView(TemplateView):
    """Landing page view"""
    template_name = 'home.html'


class LoginView(TemplateView):
    """Login page view"""
    template_name = 'auth/login.html'


class RegisterView(TemplateView):
    """Registration page view with OTP"""
    template_name = 'auth/register_otp.html'


class ForgotPasswordView(TemplateView):
    """Forgot password page view with OTP"""
    template_name = 'auth/forgot_password_otp.html'


class LoadingView(TemplateView):
    """Loading page after login"""
    template_name = 'loading.html'


class OnboardingView(TemplateView):
    """Onboarding slides view"""
    template_name = 'onboarding.html'


class DashboardView(TemplateView):
    """Dashboard view (placeholder for now)"""
    template_name = 'dashboard/admin/index.html'


class EntreprisesView(TemplateView):
    """Entreprises management view"""
    template_name = 'dashboard/admin/entreprises.html'


class EntrepriseDetailView(TemplateView):
    """Entreprise detail view"""
    template_name = 'dashboard/admin/entreprise_detail.html'


class EmployeesView(TemplateView):
    """Employees management view"""
    template_name = 'dashboard/admin/employees.html'


class CaisseView(TemplateView):
    """Point of Sale (POS) view"""
    template_name = 'dashboard/admin/caisse.html'


class VentesView(TemplateView):
    """Sales management view"""
    template_name = 'dashboard/admin/ventes.html'


class StockView(TemplateView):
    """Stock management view"""
    template_name = 'dashboard/admin/stock.html'


class IntegrationsView(LoginRequiredMixin, TemplateView):
    """Integrations management view"""
    template_name = 'integrations/index.html'
    login_url = '/login/'


class FacturesView(TemplateView):
    """Invoices management view"""
    template_name = 'dashboard/admin/factures.html'


class StatistiquesView(TemplateView):
    """Statistics and reports view"""
    template_name = 'dashboard/admin/statistiques.html'


class ParametresView(TemplateView):
    """Settings view"""
    template_name = 'dashboard/admin/parametres.html'


class ProfilView(TemplateView):
    """User profile view"""
    template_name = 'dashboard/admin/profil.html'


class IntelligenceView(TemplateView):
    """Intelligence Hub view"""
    template_name = 'dashboard/admin/intelligence.html'


# Vues par Rôle
class CaissierView(TemplateView):
    """Cashier view"""
    template_name = 'dashboard/roles/caissier/dashboard.html'


class CaissierMesVentesView(TemplateView):
    """Cashier sales history view"""
    template_name = 'dashboard/roles/caissier/mes_ventes.html'


class CaissierSessionView(TemplateView):
    """Cashier session management view"""
    template_name = 'dashboard/roles/caissier/ma_session.html'


class CaissierClientsView(TemplateView):
    """Cashier clients management view"""
    template_name = 'dashboard/roles/caissier/clients.html'


class CaissierAideView(TemplateView):
    """Cashier help and support view"""
    template_name = 'dashboard/roles/caissier/aide.html'


class GestionnaireStockView(TemplateView):
    """Stock manager view"""
    template_name = 'dashboard/roles/gestionnaire_stock/dashboard.html'


class StockInventaireView(TemplateView):
    """Stock inventory view"""
    template_name = 'dashboard/roles/gestionnaire_stock/inventaire.html'


class StockMouvementsView(TemplateView):
    """Stock movements view"""
    template_name = 'dashboard/roles/gestionnaire_stock/mouvements.html'


class StockAlertesView(TemplateView):
    """Stock alerts view"""
    template_name = 'dashboard/roles/gestionnaire_stock/alertes.html'


class StockFournisseursView(TemplateView):
    """Stock suppliers view"""
    template_name = 'dashboard/roles/gestionnaire_stock/fournisseurs.html'


class StockStatsView(TemplateView):
    """Stock statistics view"""
    template_name = 'dashboard/roles/gestionnaire_stock/stats.html'


class ComptableView(TemplateView):
    """Accountant view"""
    template_name = 'dashboard/roles/comptable/dashboard.html'


class ComptableFacturationView(TemplateView):
    """Accountant invoicing view"""
    template_name = 'dashboard/roles/comptable/facturation.html'


class ComptableDepensesTresorerieView(TemplateView):
    """Accountant expenses and treasury view"""
    template_name = 'dashboard/roles/comptable/depenses_tresorerie.html'


class ComptableComptabiliteView(TemplateView):
    """Accountant accounting entries view"""
    template_name = 'dashboard/roles/comptable/comptabilite.html'


class ComptableRapportsView(TemplateView):
    """Accountant financial reports view"""
    template_name = 'dashboard/roles/comptable/rapports.html'


class ComptableExportsView(TemplateView):
    """Accountant exports and archives view"""
    template_name = 'dashboard/roles/comptable/exports.html'


class VendeurView(TemplateView):
    """Salesperson view"""
    template_name = 'dashboard/roles/vendeur/dashboard.html'


class VendeurMesVentesView(TemplateView):
    """Salesperson sales view"""
    template_name = 'dashboard/roles/vendeur/mes_ventes.html'


class VendeurDevisView(TemplateView):
    """Salesperson quotes view"""
    template_name = 'dashboard/roles/vendeur/mes_devis.html'


class VendeurCommandesView(TemplateView):
    """Salesperson orders view"""
    template_name = 'dashboard/roles/vendeur/commandes.html'


class VendeurClientsView(TemplateView):
    """Salesperson clients view"""
    template_name = 'dashboard/roles/vendeur/clients.html'


class VendeurObjectifsView(TemplateView):
    """Salesperson objectives view"""
    template_name = 'dashboard/roles/vendeur/objectifs.html'


class VendeurStatsView(TemplateView):
    """Salesperson statistics view"""
    template_name = 'dashboard/roles/vendeur/stats.html'


class VendeurVenteView(TemplateView):
    """Salesperson new sale view"""
    template_name = 'dashboard/roles/vendeur/vente.html'


class CaissierCaisseView(TemplateView):
    """Cashier register view"""
    template_name = 'dashboard/roles/caissier/caisse.html'


class CaissierProduitsView(TemplateView):
    """Cashier products view"""
    template_name = 'dashboard/roles/caissier/produits.html'


class CaissierClientsView(TemplateView):
    """Cashier clients view"""
    template_name = 'dashboard/roles/caissier/clients.html'


class RHView(TemplateView):
    """HR view"""
    template_name = 'dashboard/roles/rh/dashboard.html'


class RHEmployeesView(TemplateView):
    """HR employees management view"""
    template_name = 'dashboard/roles/rh/employees.html'


class RHRecrutementView(TemplateView):
    """HR recruitment view"""
    template_name = 'dashboard/roles/rh/recrutement.html'


class RHCongesView(TemplateView):
    """HR leave management view"""
    template_name = 'dashboard/roles/rh/conges.html'


class RHAbsencesView(TemplateView):
    """HR absences view"""
    template_name = 'dashboard/roles/rh/absences.html'


class RHPaieView(TemplateView):
    """HR payroll view"""
    template_name = 'dashboard/roles/rh/paie.html'


class RHFormationsView(TemplateView):
    """HR training view"""
    template_name = 'dashboard/roles/rh/formations.html'


class RHEvaluationsView(TemplateView):
    """HR evaluations view"""
    template_name = 'dashboard/roles/rh/evaluations.html'


# Function-based views (alternative)
def home(request):
    """Landing page"""
    return render(request, 'home.html')


def login_page(request):
    """Login page"""
    return render(request, 'auth/login.html')


def register_page(request):
    """Registration page"""
    return render(request, 'auth/register.html')


def forgot_password_page(request):
    """Forgot password page"""
    return render(request, 'auth/forgot_password.html')


def loading_page(request):
    """Loading page"""
    return render(request, 'loading.html')


def onboarding_page(request):
    """Onboarding page"""
    return render(request, 'onboarding.html')


def dashboard_page(request):
    """Dashboard page"""
    return render(request, 'dashboard/admin/index.html')


