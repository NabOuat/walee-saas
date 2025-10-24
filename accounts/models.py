from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone
import uuid
import random
import string


class UtilisateurManager(BaseUserManager):
    """Manager personnalisé pour le modèle Utilisateur"""
    
    def create_user(self, email=None, telephone=None, password=None, **extra_fields):
        """Créer et sauvegarder un utilisateur"""
        if not email and not telephone:
            raise ValueError('L\'utilisateur doit avoir un email ou un téléphone')
        
        if email:
            email = self.normalize_email(email)
        
        user = self.model(
            email=email,
            telephone=telephone,
            **extra_fields
        )
        
        if password:
            user.set_password(password)
        
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password=None, **extra_fields):
        """Créer et sauvegarder un superutilisateur"""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('actif', True)
        extra_fields.setdefault('email_verifie', True)
        
        return self.create_user(email=email, password=password, **extra_fields)


class Utilisateur(AbstractBaseUser, PermissionsMixin):
    """Modèle utilisateur principal (basé sur la table 'utilisateurs' de la BD)"""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    supabase_user_id = models.UUIDField(unique=True, null=True, blank=True)
    
    # Informations de base
    email = models.EmailField(unique=True, null=True, blank=True)
    telephone = models.CharField(max_length=20, unique=True, null=True, blank=True)
    nom_complet = models.CharField(max_length=255)
    avatar_url = models.URLField(max_length=500, null=True, blank=True)
    
    # Mot de passe (ajouté pour Django)
    password = models.CharField(max_length=128)
    
    # Préférences
    langue = models.CharField(max_length=5, default='fr')
    fuseau_horaire = models.CharField(max_length=50, default='Africa/Abidjan')
    preferences = models.JSONField(default=dict, blank=True)
    
    # Statut
    actif = models.BooleanField(default=True)
    email_verifie = models.BooleanField(default=False)
    telephone_verifie = models.BooleanField(default=False)
    date_verification_email = models.DateTimeField(null=True, blank=True)
    date_verification_telephone = models.DateTimeField(null=True, blank=True)
    
    # Mapper last_login de Django vers derniere_connexion
    last_login = models.DateTimeField(null=True, blank=True, db_column='derniere_connexion')
    
    # Permissions Django
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    
    # Audit
    date_creation = models.DateTimeField(default=timezone.now)
    date_modification = models.DateTimeField(auto_now=True)
    date_suppression = models.DateTimeField(null=True, blank=True)
    
    objects = UtilisateurManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nom_complet']
    
    class Meta:
        db_table = 'utilisateurs'
        verbose_name = 'Utilisateur'
        verbose_name_plural = 'Utilisateurs'
        ordering = ['-date_creation']
    
    def __str__(self):
        return self.email or self.telephone or str(self.id)
    
    @property
    def derniere_connexion(self):
        """Alias pour last_login"""
        return self.last_login
    
    def save(self, *args, **kwargs):
        # S'assurer qu'au moins email ou téléphone est fourni
        if not self.email and not self.telephone:
            raise ValueError('L\'utilisateur doit avoir un email ou un téléphone')
        super().save(*args, **kwargs)


class CodeOTP(models.Model):
    """Codes OTP pour vérification email/téléphone"""
    
    TYPE_CHOICES = [
        ('email', 'Email'),
        ('telephone', 'Téléphone'),
    ]
    
    MOTIF_CHOICES = [
        ('inscription', 'Inscription'),
        ('connexion', 'Connexion'),
        ('verification', 'Vérification'),
        ('reset_password', 'Réinitialisation mot de passe'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    utilisateur = models.ForeignKey(
        Utilisateur,
        on_delete=models.CASCADE,
        related_name='codes_otp',
        null=True,
        blank=True
    )
    
    # Destination
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    email = models.EmailField(null=True, blank=True)
    telephone = models.CharField(max_length=20, null=True, blank=True)
    
    # Code OTP
    code = models.CharField(max_length=6)
    motif = models.CharField(max_length=50, choices=MOTIF_CHOICES)
    
    # Statut
    utilise = models.BooleanField(default=False)
    date_utilisation = models.DateTimeField(null=True, blank=True)
    
    # Sécurité
    tentatives = models.IntegerField(default=0)
    max_tentatives = models.IntegerField(default=3)
    
    # Dates
    date_creation = models.DateTimeField(default=timezone.now)
    date_expiration = models.DateTimeField()
    
    class Meta:
        db_table = 'codes_otp'
        verbose_name = 'Code OTP'
        verbose_name_plural = 'Codes OTP'
        ordering = ['-date_creation']
        indexes = [
            models.Index(fields=['code', 'type']),
            models.Index(fields=['email']),
            models.Index(fields=['telephone']),
            models.Index(fields=['-date_creation']),
        ]
    
    def __str__(self):
        return f"{self.code} - {self.get_type_display()} - {self.motif}"
    
    @staticmethod
    def generer_code():
        """Générer un code OTP à 6 chiffres"""
        return ''.join(random.choices(string.digits, k=6))
    
    def est_valide(self):
        """Vérifier si le code est encore valide"""
        if self.utilise:
            return False
        if self.tentatives >= self.max_tentatives:
            return False
        if timezone.now() > self.date_expiration:
            return False
        return True
    
    def incrementer_tentatives(self):
        """Incrémenter le nombre de tentatives"""
        self.tentatives += 1
        self.save(update_fields=['tentatives'])
    
    def marquer_utilise(self):
        """Marquer le code comme utilisé"""
        self.utilise = True
        self.date_utilisation = timezone.now()
        self.save(update_fields=['utilise', 'date_utilisation'])


class SessionUtilisateur(models.Model):
    """Sessions utilisateur pour tracking"""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    utilisateur = models.ForeignKey(
        Utilisateur,
        on_delete=models.CASCADE,
        related_name='sessions'
    )
    
    # Informations session
    token = models.CharField(max_length=255, unique=True)
    refresh_token = models.CharField(max_length=255, unique=True, null=True, blank=True)
    
    # Tracking
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(null=True, blank=True)
    device_info = models.JSONField(default=dict, blank=True)
    
    # Dates
    date_creation = models.DateTimeField(default=timezone.now)
    date_expiration = models.DateTimeField()
    derniere_activite = models.DateTimeField(default=timezone.now)
    date_deconnexion = models.DateTimeField(null=True, blank=True)
    
    # Statut
    active = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'sessions_utilisateur'
        verbose_name = 'Session utilisateur'
        verbose_name_plural = 'Sessions utilisateur'
        ordering = ['-date_creation']
        indexes = [
            models.Index(fields=['utilisateur', 'active']),
            models.Index(fields=['token']),
            models.Index(fields=['-date_creation']),
        ]
    
    def __str__(self):
        return f"Session {self.utilisateur} - {self.date_creation}"
    
    def est_valide(self):
        """Vérifier si la session est encore valide"""
        if not self.active:
            return False
        if timezone.now() > self.date_expiration:
            return False
        return True
    
    def deconnecter(self):
        """Déconnecter la session"""
        self.active = False
        self.date_deconnexion = timezone.now()
        self.save(update_fields=['active', 'date_deconnexion'])


# Importer les modèles d'intégrations
from .integrations.models import CategorieIntegration, Integration, IntegrationUtilisateur
