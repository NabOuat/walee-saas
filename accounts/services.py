"""
Services pour l'envoi d'OTP via Email et SMS (Twilio)
"""
import os
from django.core.mail import send_mail
from django.conf import settings
from twilio.rest import Client


def envoyer_otp_email(email, code, motif='inscription'):
    """Envoyer un code OTP par email"""
    
    # Définir le sujet et le message selon le motif
    if motif == 'inscription':
        sujet = 'Code de vérification Walee - Inscription'
        message = f'''
Bonjour,

Votre code de vérification pour créer votre compte Walee est :

{code}

Ce code est valide pendant 10 minutes.

Si vous n'avez pas demandé ce code, ignorez cet email.

Cordialement,
L'équipe Walee
        '''
    elif motif == 'reset_password':
        sujet = 'Code de vérification Walee - Réinitialisation mot de passe'
        message = f'''
Bonjour,

Votre code de vérification pour réinitialiser votre mot de passe Walee est :

{code}

Ce code est valide pendant 10 minutes.

Si vous n'avez pas demandé ce code, ignorez cet email et votre mot de passe restera inchangé.

Cordialement,
L'équipe Walee
        '''
    else:
        sujet = 'Code de vérification Walee'
        message = f'''
Bonjour,

Votre code de vérification Walee est :

{code}

Ce code est valide pendant 10 minutes.

Cordialement,
L'équipe Walee
        '''
    
    try:
        send_mail(
            sujet,
            message,
            settings.EMAIL_HOST_USER,
            [email],
            fail_silently=False,
        )
        return True
    except Exception as e:
        print(f"Erreur envoi email: {e}")
        return False


def envoyer_otp_sms(telephone, code, motif='inscription'):
    """Envoyer un code OTP par SMS via Twilio"""
    
    # Vérifier si Twilio est configuré
    account_sid = os.environ.get('TWILIO_ACCOUNT_SID')
    auth_token = os.environ.get('TWILIO_AUTH_TOKEN')
    twilio_phone = os.environ.get('TWILIO_PHONE_NUMBER')
    
    if not all([account_sid, auth_token, twilio_phone]):
        print("Twilio non configuré - Mode DEV")
        return False
    
    # Définir le message selon le motif
    if motif == 'inscription':
        message = f"Walee - Votre code de vérification pour l'inscription est : {code}. Valide 10 minutes."
    elif motif == 'reset_password':
        message = f"Walee - Votre code de réinitialisation de mot de passe est : {code}. Valide 10 minutes."
    else:
        message = f"Walee - Votre code de vérification est : {code}. Valide 10 minutes."
    
    try:
        client = Client(account_sid, auth_token)
        
        message = client.messages.create(
            body=message,
            from_=twilio_phone,
            to=telephone
        )
        
        print(f"SMS envoyé avec succès - SID: {message.sid}")
        return True
    except Exception as e:
        print(f"Erreur envoi SMS: {e}")
        return False
