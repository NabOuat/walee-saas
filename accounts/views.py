from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils import timezone
from datetime import timedelta
import secrets

from .models import Utilisateur, CodeOTP, SessionUtilisateur
from .serializers import (
    UtilisateurSerializer,
    InscriptionSerializer,
    VerificationOTPSerializer,
    ConnexionSerializer,
    ForgotPasswordSerializer,
    ResetPasswordSerializer,
    SessionSerializer
)
from .services import envoyer_otp_email, envoyer_otp_sms


class InscriptionView(APIView):
    """API pour l'inscription (étape 1: envoi OTP)"""
    permission_classes = [AllowAny]
    
    def post(self, request):
        """
        POST /api/auth/register/
        Body: {"email": "user@example.com", "nom_complet": "John Doe"}
        ou {"telephone": "+225 07 XX XX XX XX", "nom_complet": "John Doe"}
        """
        serializer = InscriptionSerializer(data=request.data)
        
        if serializer.is_valid():
            utilisateur = serializer.save()
            
            return Response({
                'success': True,
                'message': 'Code OTP envoyé avec succès',
                'data': {
                    'utilisateur_id': str(utilisateur.id),
                    'email': utilisateur.email,
                    'telephone': utilisateur.telephone,
                    'code_otp': getattr(utilisateur, 'code_otp_dev', None)  # DEV uniquement
                }
            }, status=status.HTTP_201_CREATED)
        
        return Response({
            'success': False,
            'message': 'Erreur de validation',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


class VerificationOTPView(APIView):
    """API pour vérifier le code OTP"""
    permission_classes = [AllowAny]
    
    def post(self, request):
        """
        POST /api/auth/verify-otp/
        Body: {"email": "user@example.com", "code": "123456"}
        ou {"telephone": "+225 07 XX XX XX XX", "code": "123456"}
        """
        serializer = VerificationOTPSerializer(data=request.data)
        
        if serializer.is_valid():
            utilisateur = serializer.save()
            
            # Générer les tokens JWT
            refresh = RefreshToken.for_user(utilisateur)
            access_token = str(refresh.access_token)
            refresh_token = str(refresh)
            
            # Créer une session
            session = SessionUtilisateur.objects.create(
                utilisateur=utilisateur,
                token=access_token,
                refresh_token=refresh_token,
                ip_address=self.get_client_ip(request),
                user_agent=request.META.get('HTTP_USER_AGENT', ''),
                date_expiration=timezone.now() + timedelta(days=7)
            )
            
            # Mettre à jour la dernière connexion
            utilisateur.derniere_connexion = timezone.now()
            utilisateur.save(update_fields=['derniere_connexion'])
            
            return Response({
                'success': True,
                'message': 'Connexion réussie',
                'data': {
                    'access_token': access_token,
                    'refresh_token': refresh_token,
                    'utilisateur': UtilisateurSerializer(utilisateur).data,
                    'session_id': str(session.id)
                }
            }, status=status.HTTP_200_OK)
        
        # Incrémenter les tentatives si le code existe
        code = request.data.get('code')
        email = request.data.get('email')
        telephone = request.data.get('telephone')
        
        if code:
            query = CodeOTP.objects.filter(code=code, utilise=False)
            if email:
                query = query.filter(email=email)
            elif telephone:
                query = query.filter(telephone=telephone)
            
            code_otp = query.first()
            if code_otp:
                code_otp.incrementer_tentatives()
        
        return Response({
            'success': False,
            'message': 'Code OTP invalide',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    
    def get_client_ip(self, request):
        """Récupérer l'IP du client"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip


class ConnexionView(APIView):
    """API pour la connexion classique (email/téléphone + mot de passe)"""
    permission_classes = [AllowAny]
    
    def post(self, request):
        """
        POST /api/auth/login/
        Body: {"email": "user@example.com", "password": "motdepasse"}
        ou {"telephone": "+225 07 XX XX XX XX", "password": "motdepasse"}
        """
        serializer = ConnexionSerializer(data=request.data)
        
        if serializer.is_valid():
            utilisateur = serializer.validated_data['utilisateur']
            
            # Générer les tokens JWT
            refresh = RefreshToken.for_user(utilisateur)
            access_token = str(refresh.access_token)
            refresh_token = str(refresh)
            
            # Créer une session
            session = SessionUtilisateur.objects.create(
                utilisateur=utilisateur,
                token=access_token,
                refresh_token=refresh_token,
                ip_address=self.get_client_ip(request),
                user_agent=request.META.get('HTTP_USER_AGENT', ''),
                date_expiration=timezone.now() + timedelta(days=7)
            )
            
            # Mettre à jour la dernière connexion
            utilisateur.derniere_connexion = timezone.now()
            utilisateur.save(update_fields=['derniere_connexion'])
            
            return Response({
                'success': True,
                'message': 'Connexion réussie',
                'data': {
                    'access_token': access_token,
                    'refresh_token': refresh_token,
                    'utilisateur': UtilisateurSerializer(utilisateur).data,
                    'session_id': str(session.id)
                }
            }, status=status.HTTP_200_OK)
        
        return Response({
            'success': False,
            'message': 'Erreur de validation',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    
    def get_client_ip(self, request):
        """Récupérer l'IP du client"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip


class RenvoyerOTPView(APIView):
    """API pour renvoyer un code OTP"""
    permission_classes = [AllowAny]
    
    def post(self, request):
        """
        POST /api/auth/resend-otp/
        Body: {"email": "user@example.com", "motif": "inscription"}
        ou {"telephone": "+225 07 XX XX XX XX", "motif": "connexion"}
        """
        email = request.data.get('email')
        telephone = request.data.get('telephone')
        motif = request.data.get('motif', 'connexion')
        
        if not email and not telephone:
            return Response({
                'success': False,
                'message': 'Email ou téléphone requis'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Chercher l'utilisateur
        try:
            if email:
                utilisateur = Utilisateur.objects.get(email=email)
            else:
                utilisateur = Utilisateur.objects.get(telephone=telephone)
        except Utilisateur.DoesNotExist:
            return Response({
                'success': False,
                'message': 'Utilisateur non trouvé'
            }, status=status.HTTP_404_NOT_FOUND)
        
        # Générer un nouveau code
        type_otp = 'email' if email else 'telephone'
        code = CodeOTP.generer_code()
        
        code_otp = CodeOTP.objects.create(
            utilisateur=utilisateur,
            type=type_otp,
            email=email,
            telephone=telephone,
            code=code,
            motif=motif,
            date_expiration=timezone.now() + timedelta(minutes=10)
        )
        
        # TODO: Envoyer le code par email ou SMS
        
        return Response({
            'success': True,
            'message': 'Nouveau code OTP envoyé',
            'data': {
                'code_otp': code  # DEV uniquement
            }
        }, status=status.HTTP_200_OK)


class DeconnexionView(APIView):
    """API pour la déconnexion"""
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        """
        POST /api/auth/logout/
        Headers: Authorization: Bearer {token}
        """
        # Récupérer le token de l'en-tête
        auth_header = request.META.get('HTTP_AUTHORIZATION', '')
        if auth_header.startswith('Bearer '):
            token = auth_header.split(' ')[1]
            
            # Désactiver la session
            try:
                session = SessionUtilisateur.objects.get(
                    token=token,
                    utilisateur=request.user,
                    active=True
                )
                session.deconnecter()
            except SessionUtilisateur.DoesNotExist:
                pass
        
        return Response({
            'success': True,
            'message': 'Déconnexion réussie'
        }, status=status.HTTP_200_OK)


class ForgotPasswordView(APIView):
    """API pour demander un code OTP de réinitialisation de mot de passe"""
    permission_classes = [AllowAny]
    
    def post(self, request):
        """
        POST /api/auth/forgot-password/
        Body: {"email": "user@example.com"}
        ou {"telephone": "+225 07 XX XX XX XX"}
        """
        serializer = ForgotPasswordSerializer(data=request.data)
        
        if serializer.is_valid():
            utilisateur = serializer.save()
            
            return Response({
                'success': True,
                'message': 'Code de réinitialisation envoyé avec succès',
                'data': {
                    'utilisateur_id': str(utilisateur.id),
                    'email': utilisateur.email,
                    'telephone': utilisateur.telephone,
                    'code_otp': getattr(utilisateur, 'code_otp_dev', None)  # DEV uniquement
                }
            }, status=status.HTTP_200_OK)
        
        return Response({
            'success': False,
            'message': 'Erreur de validation',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


class ResetPasswordView(APIView):
    """API pour réinitialiser le mot de passe avec OTP"""
    permission_classes = [AllowAny]
    
    def post(self, request):
        """
        POST /api/auth/reset-password/
        Body: {"email": "user@example.com", "code": "123456", "new_password": "nouveaumotdepasse"}
        """
        serializer = ResetPasswordSerializer(data=request.data)
        
        if serializer.is_valid():
            utilisateur = serializer.save()
            
            return Response({
                'success': True,
                'message': 'Mot de passe réinitialisé avec succès',
                'data': {
                    'utilisateur_id': str(utilisateur.id)
                }
            }, status=status.HTTP_200_OK)
        
        # Incrémenter les tentatives si le code existe
        code = request.data.get('code')
        email = request.data.get('email')
        telephone = request.data.get('telephone')
        
        if code:
            query = CodeOTP.objects.filter(code=code, utilise=False, motif='reset_password')
            if email:
                query = query.filter(email=email)
            elif telephone:
                query = query.filter(telephone=telephone)
            
            code_otp = query.first()
            if code_otp:
                code_otp.incrementer_tentatives()
        
        return Response({
            'success': False,
            'message': 'Code OTP invalide',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


class ProfilUtilisateurView(generics.RetrieveUpdateAPIView):
    """API pour récupérer et mettre à jour le profil utilisateur"""
    permission_classes = [IsAuthenticated]
    serializer_class = UtilisateurSerializer
    
    def get_object(self):
        return self.request.user
