"""
URL configuration for walee project.
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from frontend import views

urlpatterns = [
    # Admin
    path("admin/", admin.site.urls),
    
    # Landing page
    path("", views.HomeView.as_view(), name='home'),
    
    # Authentication
    path("login/", views.LoginView.as_view(), name='login'),
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
    path("dashboard/ventes/", views.VentesView.as_view(), name='ventes'),
    path("dashboard/stock/", views.StockView.as_view(), name='stock'),
    path("dashboard/factures/", views.FacturesView.as_view(), name='factures'),
    path("dashboard/statistiques/", views.StatistiquesView.as_view(), name='statistiques'),
    path("dashboard/intelligence/", views.IntelligenceView.as_view(), name='intelligence'),
    path("dashboard/parametres/", views.ParametresView.as_view(), name='parametres'),
    path("dashboard/profil/", views.ProfilView.as_view(), name='profil'),
    
    # Dashboards par Rôle
    path("dashboard/caissier/", views.CaissierView.as_view(), name='caissier'),
    path("dashboard/gestionnaire-stock/", views.GestionnaireStockView.as_view(), name='gestionnaire_stock'),
    path("dashboard/comptable/", views.ComptableView.as_view(), name='comptable'),
]

# Serve static and media files in development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
