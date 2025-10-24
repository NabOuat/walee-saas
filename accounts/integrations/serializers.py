"""
Serializers pour les intégrations Walee
"""
from rest_framework import serializers
from .models import CategorieIntegration, Integration, IntegrationUtilisateur


class CategorieIntegrationSerializer(serializers.ModelSerializer):
    """Serializer pour les catégories d'intégrations"""
    
    nombre_integrations = serializers.SerializerMethodField()
    
    class Meta:
        model = CategorieIntegration
        fields = [
            'id', 'nom', 'slug', 'description', 'icone', 'couleur',
            'ordre', 'nombre_integrations'
        ]
    
    def get_nombre_integrations(self, obj):
        return obj.integrations.count()


class IntegrationSerializer(serializers.ModelSerializer):
    """Serializer pour les intégrations"""
    
    categorie = CategorieIntegrationSerializer(read_only=True)
    est_activee = serializers.SerializerMethodField()
    
    class Meta:
        model = Integration
        fields = [
            'id', 'categorie', 'nom', 'slug', 'description', 'description_courte',
            'icone', 'couleur', 'image', 'types_entreprise', 'actif_par_defaut',
            'gratuit', 'prix_mensuel', 'fonctionnalites', 'necessite_configuration',
            'documentation_url', 'video_demo_url', 'ordre', 'populaire', 'nouveau',
            'est_activee'
        ]
    
    def get_est_activee(self, obj):
        """Vérifie si l'intégration est activée pour l'utilisateur connecté"""
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return IntegrationUtilisateur.objects.filter(
                utilisateur=request.user,
                integration=obj,
                actif=True
            ).exists()
        return False


class IntegrationUtilisateurSerializer(serializers.ModelSerializer):
    """Serializer pour les intégrations utilisateur"""
    
    integration = IntegrationSerializer(read_only=True)
    
    class Meta:
        model = IntegrationUtilisateur
        fields = [
            'id', 'integration', 'actif', 'configuration',
            'nombre_utilisations', 'derniere_utilisation',
            'date_activation', 'date_desactivation'
        ]
        read_only_fields = [
            'nombre_utilisations', 'derniere_utilisation',
            'date_activation', 'date_desactivation'
        ]
