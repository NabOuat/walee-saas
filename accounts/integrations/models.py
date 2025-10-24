"""
Modèles pour le système d'intégrations modulaires Walee
"""
from django.db import models
from django.utils import timezone
import uuid


class CategorieIntegration(models.Model):
    """Catégories d'intégrations"""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nom = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    icone = models.CharField(max_length=50)  # Nom icône Lucide
    couleur = models.CharField(max_length=20)  # Couleur hex
    ordre = models.IntegerField(default=0)
    
    date_creation = models.DateTimeField(default=timezone.now)
    date_modification = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'categories_integration'
        ordering = ['ordre', 'nom']
        verbose_name = 'Catégorie d\'intégration'
        verbose_name_plural = 'Catégories d\'intégration'
    
    def __str__(self):
        return self.nom


class Integration(models.Model):
    """Intégrations disponibles dans Walee"""
    
    TYPE_ENTREPRISE_CHOICES = [
        ('hotel', 'Hôtel'),
        ('restaurant', 'Restaurant'),
        ('lavage', 'Lavage/Pressing'),
        ('supermarche', 'Supermarché'),
        ('superette', 'Superette'),
        ('bar', 'Bar/Café'),
        ('boutique', 'Boutique'),
        ('salon', 'Salon de coiffure'),
        ('pharmacie', 'Pharmacie'),
        ('tous', 'Tous types'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    categorie = models.ForeignKey(CategorieIntegration, on_delete=models.CASCADE, related_name='integrations')
    
    # Informations de base
    nom = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    description_courte = models.CharField(max_length=200)
    
    # Visuel
    icone = models.CharField(max_length=50)  # Nom icône Lucide
    couleur = models.CharField(max_length=20)  # Couleur hex
    image = models.URLField(blank=True, null=True)
    
    # Configuration
    types_entreprise = models.JSONField(default=list)  # Liste des types compatibles
    actif_par_defaut = models.BooleanField(default=False)
    gratuit = models.BooleanField(default=True)
    prix_mensuel = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    # Fonctionnalités
    fonctionnalites = models.JSONField(default=list)  # Liste des fonctionnalités
    necessite_configuration = models.BooleanField(default=False)
    
    # Documentation
    documentation_url = models.URLField(blank=True)
    video_demo_url = models.URLField(blank=True)
    
    # Ordre d'affichage
    ordre = models.IntegerField(default=0)
    populaire = models.BooleanField(default=False)
    nouveau = models.BooleanField(default=False)
    
    # Audit
    date_creation = models.DateTimeField(default=timezone.now)
    date_modification = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'integrations'
        ordering = ['ordre', 'nom']
        verbose_name = 'Intégration'
        verbose_name_plural = 'Intégrations'
    
    def __str__(self):
        return self.nom
    
    def est_compatible_avec(self, type_entreprise):
        """Vérifie si l'intégration est compatible avec un type d'entreprise"""
        return 'tous' in self.types_entreprise or type_entreprise in self.types_entreprise


class IntegrationUtilisateur(models.Model):
    """Intégrations activées par un utilisateur"""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    utilisateur = models.ForeignKey('Utilisateur', on_delete=models.CASCADE, related_name='integrations')
    integration = models.ForeignKey(Integration, on_delete=models.CASCADE)
    
    # État
    actif = models.BooleanField(default=True)
    
    # Configuration spécifique
    configuration = models.JSONField(default=dict)
    
    # Credentials (si nécessaire)
    api_key = models.CharField(max_length=500, blank=True)
    api_secret = models.CharField(max_length=500, blank=True)
    webhook_url = models.URLField(blank=True)
    
    # Statistiques d'utilisation
    nombre_utilisations = models.IntegerField(default=0)
    derniere_utilisation = models.DateTimeField(null=True, blank=True)
    
    # Audit
    date_activation = models.DateTimeField(default=timezone.now)
    date_desactivation = models.DateTimeField(null=True, blank=True)
    date_modification = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'integrations_utilisateur'
        unique_together = ['utilisateur', 'integration']
        verbose_name = 'Intégration utilisateur'
        verbose_name_plural = 'Intégrations utilisateur'
    
    def __str__(self):
        return f"{self.utilisateur} - {self.integration.nom}"
    
    def activer(self):
        """Active l'intégration"""
        self.actif = True
        self.date_activation = timezone.now()
        self.date_desactivation = None
        self.save()
    
    def desactiver(self):
        """Désactive l'intégration"""
        self.actif = False
        self.date_desactivation = timezone.now()
        self.save()
    
    def incrementer_utilisation(self):
        """Incrémente le compteur d'utilisation"""
        self.nombre_utilisations += 1
        self.derniere_utilisation = timezone.now()
        self.save()
