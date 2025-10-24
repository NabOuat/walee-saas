"""
URLs pour les intégrations Walee
"""
from django.urls import path
from .views import (
    ListeIntegrationsView,
    ListeCategoriesView,
    MesIntegrationsView,
    ActiverIntegrationView,
    DesactiverIntegrationView,
    ConfigurerIntegrationView
)

urlpatterns = [
    # Liste des intégrations
    path('', ListeIntegrationsView.as_view(), name='liste-integrations'),
    path('categories/', ListeCategoriesView.as_view(), name='liste-categories'),
    
    # Mes intégrations
    path('mes-integrations/', MesIntegrationsView.as_view(), name='mes-integrations'),
    
    # Activer/Désactiver
    path('activer/<slug:slug>/', ActiverIntegrationView.as_view(), name='activer-integration'),
    path('desactiver/<slug:slug>/', DesactiverIntegrationView.as_view(), name='desactiver-integration'),
    
    # Configuration
    path('configurer/<slug:slug>/', ConfigurerIntegrationView.as_view(), name='configurer-integration'),
]
