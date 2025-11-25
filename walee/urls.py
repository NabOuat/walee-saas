"""
URL configuration for walee project.
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from frontend import views
from frontend.api_supabase import add_user
from backend.walee import api_views

# Custom error handlers
handler404 = 'frontend.views.error_404'
handler500 = 'frontend.views.error_500'

urlpatterns = [
    # Admin
    path("admin/", admin.site.urls),
    
    # API Integrations (mode frontend uniquement)
    # path("api/integrations/", include('accounts.integrations.urls')),
    
    # Landing page
    path("", views.HomeView.as_view(), name='home'),
    
    # Authentication
    path("login/", views.LoginView.as_view(), name='login'),
    # path("register/", include('frontend.views.register'), name='register'),
    path("register/", views.RegisterView.as_view(), name='register'),
    path("forgot-password/", views.ForgotPasswordView.as_view(), name='forgot_password'),
    
    # Onboarding
    path("loading/", views.LoadingView.as_view(), name='loading'),
    path("onboarding/", views.OnboardingView.as_view(), name='onboarding'),
    
    # Dashboard
    path("dashboard/", views.DashboardView.as_view(), name='dashboard'),
    path("dashboard/entreprises/", views.EntreprisesView.as_view(), name='entreprises'),
    path("dashboard/entreprises/<int:id>/", views.EntrepriseDetailView.as_view(), name='entreprise_detail'),
    path("dashboard/employees/", views.EmployeesView.as_view(), name='employees'),
    path("dashboard/caisse/", views.CaisseView.as_view(), name='caisse'),
    path("dashboard/ventes/", views.VentesView.as_view(), name='ventes'),
    path("dashboard/stock/", views.StockView.as_view(), name='stock'),
    path("dashboard/factures/", views.FacturesView.as_view(), name='factures'),
    path("dashboard/statistiques/", views.StatistiquesView.as_view(), name='statistiques'),
    path("dashboard/intelligence/", views.IntelligenceView.as_view(), name='intelligence'),
    path("dashboard/integrations/", views.IntegrationsView.as_view(), name='integrations'),
    path("dashboard/parametres/", views.ParametresView.as_view(), name='parametres'),
    path("dashboard/profil/", views.ProfilView.as_view(), name='profil'),
    
    # Dashboards par Rôle
    path("dashboard/caissier/", views.CaissierView.as_view(), name='caissier'),
    path("dashboard/caissier/mes-ventes/", views.CaissierMesVentesView.as_view(), name='caissier_mes_ventes'),
    path("dashboard/caissier/ma-session/", views.CaissierSessionView.as_view(), name='caissier_session'),
    path("dashboard/caissier/clients/", views.CaissierClientsView.as_view(), name='caissier_clients'),
    path("dashboard/caissier/aide/", views.CaissierAideView.as_view(), name='caissier_aide'),
    path("dashboard/gestionnaire-stock/", views.GestionnaireStockView.as_view(), name='gestionnaire_stock'),
    path("dashboard/gestionnaire-stock/inventaire/", views.StockInventaireView.as_view(), name='stock_inventaire'),
    path("dashboard/gestionnaire-stock/mouvements/", views.StockMouvementsView.as_view(), name='stock_mouvements'),
    path("dashboard/gestionnaire-stock/alertes/", views.StockAlertesView.as_view(), name='stock_alertes'),
    path("dashboard/gestionnaire-stock/fournisseurs/", views.StockFournisseursView.as_view(), name='stock_fournisseurs'),
    path("dashboard/gestionnaire-stock/stats/", views.StockStatsView.as_view(), name='stock_stats'),
    path("dashboard/comptable/", views.ComptableView.as_view(), name='comptable'),
    path("dashboard/comptable/facturation/", views.ComptableFacturationView.as_view(), name='comptable_facturation'),
    path("dashboard/comptable/depenses-tresorerie/", views.ComptableDepensesTresorerieView.as_view(), name='comptable_depenses_tresorerie'),
    path("dashboard/comptable/comptabilite/", views.ComptableComptabiliteView.as_view(), name='comptable_comptabilite'),
    path("dashboard/comptable/rapports/", views.ComptableRapportsView.as_view(), name='comptable_rapports'),
    path("dashboard/comptable/exports/", views.ComptableExportsView.as_view(), name='comptable_exports'),
    path("dashboard/vendeur/", views.VendeurView.as_view(), name='vendeur'),
    path("dashboard/vendeur/mes-ventes/", views.VendeurMesVentesView.as_view(), name='vendeur_mes_ventes'),
    path("dashboard/vendeur/devis/", views.VendeurDevisView.as_view(), name='vendeur_devis'),
    path("dashboard/vendeur/commandes/", views.VendeurCommandesView.as_view(), name='vendeur_commandes'),
    path("dashboard/vendeur/clients/", views.VendeurClientsView.as_view(), name='vendeur_clients'),
    path("dashboard/vendeur/objectifs/", views.VendeurObjectifsView.as_view(), name='vendeur_objectifs'),
    path("dashboard/vendeur/stats/", views.VendeurStatsView.as_view(), name='vendeur_stats'),
    path("dashboard/vendeur/vente/", views.VendeurVenteView.as_view(), name='vendeur_vente'),
    path("dashboard/caissier/caisse/", views.CaissierCaisseView.as_view(), name='caissier_caisse'),
    path("dashboard/caissier/produits/", views.CaissierProduitsView.as_view(), name='caissier_produits'),
    path("dashboard/caissier/clients/", views.CaissierClientsView.as_view(), name='caissier_clients'),
    path("dashboard/rh/", views.RHView.as_view(), name='rh'),
    path("dashboard/rh/employees/", views.RHEmployeesView.as_view(), name='rh_employees'),
    path("dashboard/rh/recrutement/", views.RHRecrutementView.as_view(), name='rh_recrutement'),
    path("dashboard/rh/conges/", views.RHCongesView.as_view(), name='rh_conges'),
    path("dashboard/rh/absences/", views.RHAbsencesView.as_view(), name='rh_absences'),
    path("dashboard/rh/paie/", views.RHPaieView.as_view(), name='rh_paie'),
    path("dashboard/rh/formations/", views.RHFormationsView.as_view(), name='rh_formations'),
    path("dashboard/rh/evaluations/", views.RHEvaluationsView.as_view(), name='rh_evaluations'),

    # API Supabase
    # path('api/utilisateurs/', add_user, name='add_user'),
    path('api/auth/register/',api_views.InscriptionPartenaireAPIView.as_view(), name='auth_signup' ),
    path('api/auth/login/',api_views.LoginPartenaireAPIView.as_view(), name='auth_login'),
    path('api/auth/profile/',api_views.ProfilePartenaireAPIView.as_view(), name='auth_profile'),
    # path('api/entreprises/', api_views.OrganisationsAPIView.as_view(), name='entreprises_api'),
    path('api/auth/verify-otp/', api_views.VerifyOtpAPIView.as_view(), name='auth_verify_otp'),
    # path('api/auth/logout/',api_views.LoginPartenaireAPIView.as_view(), name='logout')
    # 1. Route LISTE/CREATE: Sans ID. Appelle les méthodes get() et post()
    path('api/organisations/', api_views.OrganisationAPIView.as_view(), name='organisation-list-create'),
    
    # 2. Route DETAIL/UPDATE/DELETE: AVEC ID. Appelle les méthodes patch() et delete()
    # L'ID est passé comme argument 'pk' à la vue
    path('api/organisations/<uuid:pk>/', api_views.OrganisationAPIView.as_view(), name='organisation-detail'),
]

# Serve static and media files in development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
