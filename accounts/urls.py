from django.urls import path
from .views import (
    InscriptionView,
    VerificationOTPView,
    ConnexionView,
    RenvoyerOTPView,
    DeconnexionView,
    ForgotPasswordView,
    ResetPasswordView,
    ProfilUtilisateurView
)

app_name = 'accounts'

urlpatterns = [
    # Inscription (avec OTP)
    path('register/', InscriptionView.as_view(), name='register'),
    path('verify-otp/', VerificationOTPView.as_view(), name='verify-otp'),
    path('resend-otp/', RenvoyerOTPView.as_view(), name='resend-otp'),
    
    # Connexion classique (email/téléphone + mot de passe)
    path('login/', ConnexionView.as_view(), name='login'),
    
    # Mot de passe oublié (avec OTP)
    path('forgot-password/', ForgotPasswordView.as_view(), name='forgot-password'),
    path('reset-password/', ResetPasswordView.as_view(), name='reset-password'),
    
    # Déconnexion
    path('logout/', DeconnexionView.as_view(), name='logout'),
    
    # Profil utilisateur
    path('profile/', ProfilUtilisateurView.as_view(), name='profile'),
]
