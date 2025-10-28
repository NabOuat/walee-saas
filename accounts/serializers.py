from rest_framework import serializers
from django.contrib.auth import authenticate
from django.utils import timezone
from datetime import timedelta
from .models import Utilisateur, CodeOTP, SessionUtilisateur
from .services import envoyer_otp_email, envoyer_otp_sms
import re


class UtilisateurSerializer(serializers.ModelSerializer):
    """Serializer pour le modèle Utilisateur"""
    
    class Meta:
        model = Utilisateur
        fields = [
            'id', 'email', 'telephone', 'nom_complet', 'avatar_url',
            'langue', 'fuseau_horaire', 'actif', 'email_verifie',
            'telephone_verifie', 'date_creation', 'derniere_connexion'
        ]
        read_only_fields = [
            'id', 'email_verifie', 'telephone_verifie',
            'date_creation', 'derniere_connexion'
        ]


class InscriptionSerializer(serializers.Serializer):
    """Serializer pour l'inscription (étape 1: envoi OTP)"""
    
    email = serializers.EmailField(required=False, allow_blank=True)
    telephone = serializers.CharField(required=False, allow_blank=True, max_length=20)
    nom_complet = serializers.CharField(required=True, max_length=255)
    
    def validate(self, data):
        """Valider qu'au moins email ou téléphone est fourni"""
        email = data.get('email')
        telephone = data.get('telephone')
        
        if not email and not telephone:
            raise serializers.ValidationError(
                "Vous devez fournir un email ou un numéro de téléphone"
            )
        
        # Valider le format du téléphone (Côte d'Ivoire)
        if telephone:
            # Nettoyer le numéro
            telephone_clean = re.sub(r'[\s\-\(\)]', '', telephone)
            
            # Vérifier le format
            if not re.match(r'^(\+225|0)[0-9]{10}$', telephone_clean):
                raise serializers.ValidationError({
                    'telephone': 'Format invalide. Utilisez +225 XX XX XX XX XX ou 07 XX XX XX XX'
                })
            
            data['telephone'] = telephone_clean
        
        # Vérifier si l'utilisateur existe déjà
        if email and Utilisateur.objects.filter(email=email).exists():
            raise serializers.ValidationError({
                'email': 'Un compte avec cet email existe déjà'
            })
        
        if telephone and Utilisateur.objects.filter(telephone=telephone).exists():
            raise serializers.ValidationError({
                'telephone': 'Un compte avec ce numéro existe déjà'
            })
        
        return data
    
    def create(self, validated_data):
        """Créer un utilisateur et envoyer un code OTP"""
        email = validated_data.get('email')
        telephone = validated_data.get('telephone')
        nom_complet = validated_data['nom_complet']
        
        # Créer l'utilisateur (inactif jusqu'à vérification OTP)
        utilisateur = Utilisateur.objects.create_user(
            email=email,
            telephone=telephone,
            nom_complet=nom_complet,
            actif=False  # Sera activé après vérification OTP
        )
        
        # Générer et envoyer le code OTP
        type_otp = 'email' if email else 'telephone'
        code = CodeOTP.generer_code()
        
        code_otp = CodeOTP.objects.create(
            utilisateur=utilisateur,
            type=type_otp,
            email=email,
            telephone=telephone,
            code=code,
            motif='inscription',
            date_expiration=timezone.now() + timedelta(minutes=10)
        )
        
        # Envoyer le code par email ou SMS
        if email:
            envoyer_otp_email(email, code, 'inscription')
        elif telephone:
            envoyer_otp_sms(telephone, code, 'inscription')
        
        # En mode DEV, retourner le code dans la réponse
        utilisateur.code_otp_dev = code
        
        return utilisateur


class VerificationOTPSerializer(serializers.Serializer):
    """Serializer pour vérifier le code OTP"""
    
    email = serializers.EmailField(required=False, allow_blank=True)
    telephone = serializers.CharField(required=False, allow_blank=True, max_length=20)
    code = serializers.CharField(required=True, max_length=6, min_length=6)
    password = serializers.CharField(required=True, min_length=8, write_only=True)  # Mot de passe à définir
    
    def validate(self, data):
        """Valider le code OTP"""
        email = data.get('email')
        telephone = data.get('telephone')
        code = data.get('code')
        
        if not email and not telephone:
            raise serializers.ValidationError(
                "Vous devez fournir un email ou un numéro de téléphone"
            )
        
        # Chercher le code OTP
        query = CodeOTP.objects.filter(code=code, utilise=False)
        
        if email:
            query = query.filter(email=email, type='email')
        else:
            query = query.filter(telephone=telephone, type='telephone')
        
        code_otp = query.order_by('-date_creation').first()
        
        if not code_otp:
            raise serializers.ValidationError({
                'code': 'Code OTP invalide'
            })
        
        if not code_otp.est_valide():
            if code_otp.utilise:
                raise serializers.ValidationError({
                    'code': 'Ce code a déjà été utilisé'
                })
            elif code_otp.tentatives >= code_otp.max_tentatives:
                raise serializers.ValidationError({
                    'code': 'Trop de tentatives. Demandez un nouveau code'
                })
            else:
                raise serializers.ValidationError({
                    'code': 'Ce code a expiré. Demandez un nouveau code'
                })
        
        data['code_otp'] = code_otp
        return data
    
    def save(self):
        """Marquer le code comme utilisé et activer l'utilisateur"""
        code_otp = self.validated_data['code_otp']
        password = self.validated_data['password']
        utilisateur = code_otp.utilisateur
        
        # Marquer le code comme utilisé
        code_otp.marquer_utilise()
        
        # Définir le mot de passe
        utilisateur.set_password(password)
        
        # Activer l'utilisateur et marquer comme vérifié
        utilisateur.actif = True
        
        if code_otp.type == 'email':
            utilisateur.email_verifie = True
            utilisateur.date_verification_email = timezone.now()
        else:
            utilisateur.telephone_verifie = True
            utilisateur.date_verification_telephone = timezone.now()
        
        utilisateur.save()
        
        return utilisateur


class ConnexionSerializer(serializers.Serializer):
    """Serializer pour la connexion classique (email/téléphone + mot de passe)"""
    
    email = serializers.EmailField(required=False, allow_blank=True)
    telephone = serializers.CharField(required=False, allow_blank=True, max_length=20)
    password = serializers.CharField(required=True, write_only=True)
    
    def validate(self, data):
        """Valider les credentials"""
        email = data.get('email')
        telephone = data.get('telephone')
        password = data.get('password')
        
        if not email and not telephone:
            raise serializers.ValidationError(
                "Vous devez fournir un email ou un numéro de téléphone"
            )
        
        # Chercher l'utilisateur
        try:
            if email:
                utilisateur = Utilisateur.objects.get(email=email)
            else:
                utilisateur = Utilisateur.objects.get(telephone=telephone)
        except Utilisateur.DoesNotExist:
            raise serializers.ValidationError(
                "Email/téléphone ou mot de passe incorrect"
            )
        
        # Vérifier le mot de passe
        if not utilisateur.check_password(password):
            raise serializers.ValidationError(
                "Email/téléphone ou mot de passe incorrect"
            )
        
        if not utilisateur.actif:
            raise serializers.ValidationError(
                "Ce compte est désactivé. Contactez le support"
            )
        
        data['utilisateur'] = utilisateur
        return data


class ResetPasswordSerializer(serializers.Serializer):
    """Serializer pour réinitialiser le mot de passe avec OTP"""
    
    email = serializers.EmailField(required=False, allow_blank=True)
    telephone = serializers.CharField(required=False, allow_blank=True, max_length=20)
    code = serializers.CharField(required=True, max_length=6, min_length=6)
    new_password = serializers.CharField(required=True, min_length=8, write_only=True)
    
    def validate(self, data):
        """Valider le code OTP pour reset password"""
        email = data.get('email')
        telephone = data.get('telephone')
        code = data.get('code')
        
        if not email and not telephone:
            raise serializers.ValidationError(
                "Vous devez fournir un email ou un numéro de téléphone"
            )
        
        # Chercher le code OTP
        query = CodeOTP.objects.filter(code=code, utilise=False, motif='reset_password')
        
        if email:
            query = query.filter(email=email, type='email')
        else:
            query = query.filter(telephone=telephone, type='telephone')
        
        code_otp = query.order_by('-date_creation').first()
        
        if not code_otp:
            raise serializers.ValidationError({
                'code': 'Code OTP invalide'
            })
        
        if not code_otp.est_valide():
            if code_otp.utilise:
                raise serializers.ValidationError({
                    'code': 'Ce code a déjà été utilisé'
                })
            elif code_otp.tentatives >= code_otp.max_tentatives:
                raise serializers.ValidationError({
                    'code': 'Trop de tentatives. Demandez un nouveau code'
                })
            else:
                raise serializers.ValidationError({
                    'code': 'Ce code a expiré. Demandez un nouveau code'
                })
        
        data['code_otp'] = code_otp
        return data
    
    def save(self):
        """Réinitialiser le mot de passe"""
        code_otp = self.validated_data['code_otp']
        new_password = self.validated_data['new_password']
        utilisateur = code_otp.utilisateur
        
        # Marquer le code comme utilisé
        code_otp.marquer_utilise()
        
        # Changer le mot de passe
        utilisateur.set_password(new_password)
        utilisateur.save()
        
        return utilisateur


class ForgotPasswordSerializer(serializers.Serializer):
    """Serializer pour demander un code OTP de réinitialisation"""
    
    email = serializers.EmailField(required=False, allow_blank=True)
    telephone = serializers.CharField(required=False, allow_blank=True, max_length=20)
    
    def validate(self, data):
        """Valider que l'utilisateur existe"""
        email = data.get('email')
        telephone = data.get('telephone')
        
        if not email and not telephone:
            raise serializers.ValidationError(
                "Vous devez fournir un email ou un numéro de téléphone"
            )
        
        # Chercher l'utilisateur
        try:
            if email:
                utilisateur = Utilisateur.objects.get(email=email)
            else:
                utilisateur = Utilisateur.objects.get(telephone=telephone)
        except Utilisateur.DoesNotExist:
            raise serializers.ValidationError(
                "Aucun compte trouvé avec ces identifiants"
            )
        
        data['utilisateur'] = utilisateur
        return data
    
    def create(self, validated_data):
        """Générer et envoyer un code OTP pour reset password"""
        utilisateur = validated_data['utilisateur']
        
        # Déterminer le type d'OTP
        if utilisateur.email:
            type_otp = 'email'
            destination = utilisateur.email
        else:
            type_otp = 'telephone'
            destination = utilisateur.telephone
        
        # Générer le code OTP
        code = CodeOTP.generer_code()
        
        code_otp = CodeOTP.objects.create(
            utilisateur=utilisateur,
            type=type_otp,
            email=utilisateur.email if type_otp == 'email' else None,
            telephone=utilisateur.telephone if type_otp == 'telephone' else None,
            code=code,
            motif='reset_password',
            date_expiration=timezone.now() + timedelta(minutes=10)
        )
        
        # Envoyer le code par email ou SMS
        if type_otp == 'email':
            envoyer_otp_email(utilisateur.email, code, 'reset_password')
        else:
            envoyer_otp_sms(utilisateur.telephone, code, 'reset_password')
        
        # En mode DEV, retourner le code dans la réponse
        utilisateur.code_otp_dev = code
        
        return utilisateur


class SessionSerializer(serializers.ModelSerializer):
    """Serializer pour les sessions utilisateur"""
    
    utilisateur = UtilisateurSerializer(read_only=True)
    
    class Meta:
        model = SessionUtilisateur
        fields = [
            'id', 'utilisateur', 'token', 'ip_address',
            'user_agent', 'date_creation', 'date_expiration',
            'derniere_activite', 'active'
        ]
        read_only_fields = ['id', 'token', 'date_creation']
