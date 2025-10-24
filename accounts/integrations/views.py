"""
Vues API pour les intégrations Walee
"""
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.shortcuts import get_object_or_404

from .models import CategorieIntegration, Integration, IntegrationUtilisateur
from .serializers import (
    CategorieIntegrationSerializer,
    IntegrationSerializer,
    IntegrationUtilisateurSerializer
)


class ListeIntegrationsView(APIView):
    """Liste toutes les intégrations disponibles"""
    permission_classes = []  # Pas de permission requise
    authentication_classes = []  # Pas d'authentification requise
    
    def get(self, request):
        """
        GET /api/integrations/
        Query params:
          - categorie: slug de la catégorie
          - type_entreprise: type d'entreprise (hotel, restaurant, etc.)
          - populaire: true/false
        """
        integrations = Integration.objects.all()
        
        # Filtres
        categorie_slug = request.query_params.get('categorie')
        if categorie_slug:
            integrations = integrations.filter(categorie__slug=categorie_slug)
        
        type_entreprise = request.query_params.get('type_entreprise')
        if type_entreprise:
            integrations = [i for i in integrations if i.est_compatible_avec(type_entreprise)]
        
        populaire = request.query_params.get('populaire')
        if populaire == 'true':
            integrations = integrations.filter(populaire=True)
        
        serializer = IntegrationSerializer(integrations, many=True, context={'request': request})
        
        return Response({
            'success': True,
            'data': serializer.data
        })


class ListeCategoriesView(APIView):
    """Liste toutes les catégories d'intégrations"""
    permission_classes = []  # Pas de permission requise
    authentication_classes = []  # Pas d'authentification requise
    
    def get(self, request):
        """GET /api/integrations/categories/"""
        categories = CategorieIntegration.objects.all()
        serializer = CategorieIntegrationSerializer(categories, many=True)
        
        return Response({
            'success': True,
            'data': serializer.data
        })


class MesIntegrationsView(APIView):
    """Gère les intégrations de l'utilisateur connecté"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        """
        GET /api/integrations/mes-integrations/
        Liste les intégrations activées par l'utilisateur
        """
        integrations_user = IntegrationUtilisateur.objects.filter(
            utilisateur=request.user
        ).select_related('integration', 'integration__categorie')
        
        serializer = IntegrationUtilisateurSerializer(integrations_user, many=True)
        
        return Response({
            'success': True,
            'data': serializer.data
        })


class ActiverIntegrationView(APIView):
    """Active une intégration pour l'utilisateur"""
    permission_classes = []  # Pas de permission requise
    authentication_classes = []  # Pas d'authentification requise
    
    def post(self, request, slug):
        """
        POST /api/integrations/activer/<slug>/
        Body: {
            "configuration": {}  // optionnel
        }
        """
        integration = get_object_or_404(Integration, slug=slug)
        
        # MODE TEST: Retourner succès sans créer d'enregistrement
        return Response({
            'success': True,
            'message': f'{integration.nom} activée avec succès (mode test)',
            'data': {
                'integration': IntegrationSerializer(integration).data,
                'actif': True
            }
        }, status=status.HTTP_200_OK)
        
        if not created:
            # Réactiver si désactivée
            if not integration_user.actif:
                integration_user.activer()
                message = f'{integration.nom} réactivée avec succès'
            else:
                message = f'{integration.nom} est déjà activée'
        else:
            message = f'{integration.nom} activée avec succès'
        
        serializer = IntegrationUtilisateurSerializer(integration_user)
        
        return Response({
            'success': True,
            'message': message,
            'data': serializer.data
        }, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)


class DesactiverIntegrationView(APIView):
    """Désactive une intégration pour l'utilisateur"""
    permission_classes = []  # Pas de permission requise
    authentication_classes = []  # Pas d'authentification requise
    
    def post(self, request, slug):
        """POST /api/integrations/desactiver/<slug>/"""
        integration = get_object_or_404(Integration, slug=slug)
        
        try:
            integration_user = IntegrationUtilisateur.objects.get(
                utilisateur=request.user,
                integration=integration
            )
            integration_user.desactiver()
            
            return Response({
                'success': True,
                'message': f'{integration.nom} désactivée avec succès'
            })
        except IntegrationUtilisateur.DoesNotExist:
            return Response({
                'success': False,
                'message': 'Cette intégration n\'est pas activée'
            }, status=status.HTTP_404_NOT_FOUND)


class ConfigurerIntegrationView(APIView):
    """Configure une intégration"""
    permission_classes = [IsAuthenticated]
    
    def put(self, request, slug):
        """
        PUT /api/integrations/configurer/<slug>/
        Body: {
            "configuration": {},
            "api_key": "",
            "api_secret": ""
        }
        """
        integration = get_object_or_404(Integration, slug=slug)
        
        try:
            integration_user = IntegrationUtilisateur.objects.get(
                utilisateur=request.user,
                integration=integration
            )
            
            # Mettre à jour la configuration
            if 'configuration' in request.data:
                integration_user.configuration = request.data['configuration']
            if 'api_key' in request.data:
                integration_user.api_key = request.data['api_key']
            if 'api_secret' in request.data:
                integration_user.api_secret = request.data['api_secret']
            
            integration_user.save()
            
            serializer = IntegrationUtilisateurSerializer(integration_user)
            
            return Response({
                'success': True,
                'message': 'Configuration mise à jour',
                'data': serializer.data
            })
        except IntegrationUtilisateur.DoesNotExist:
            return Response({
                'success': False,
                'message': 'Vous devez d\'abord activer cette intégration'
            }, status=status.HTTP_404_NOT_FOUND)
