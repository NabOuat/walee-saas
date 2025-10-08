"""
Views for frontend pages (authentication and landing page)
"""
from django.shortcuts import render
from django.views.generic import TemplateView


# Error handlers
def error_404(request, exception):
    """Custom 404 error page"""
    return render(request, '404.html', status=404)


def error_500(request):
    """Custom 500 error page"""
    return render(request, '500.html', status=500)


class HomeView(TemplateView):
    """Landing page view"""
    template_name = 'home.html'


class LoginView(TemplateView):
    """Login page view"""
    template_name = 'auth/login.html'


class RegisterView(TemplateView):
    """Registration page view"""
    template_name = 'auth/register.html'


class ForgotPasswordView(TemplateView):
    """Forgot password page view"""
    template_name = 'auth/forgot_password.html'


class LoadingView(TemplateView):
    """Loading page after login"""
    template_name = 'loading.html'


class OnboardingView(TemplateView):
    """Onboarding slides view"""
    template_name = 'onboarding.html'


class DashboardView(TemplateView):
    """Dashboard view (placeholder for now)"""
    template_name = 'dashboard/admin/index.html'


class EntreprisesView(TemplateView):
    """Entreprises management view"""
    template_name = 'dashboard/admin/entreprises.html'


class EntrepriseDetailView(TemplateView):
    """Entreprise detail view"""
    template_name = 'dashboard/admin/entreprise_detail.html'


class EmployeesView(TemplateView):
    """Employees management view"""
    template_name = 'dashboard/admin/employees.html'


class VentesView(TemplateView):
    """Sales management view"""
    template_name = 'dashboard/admin/ventes.html'


class StockView(TemplateView):
    """Stock management view"""
    template_name = 'dashboard/admin/stock.html'


class FacturesView(TemplateView):
    """Invoices management view"""
    template_name = 'dashboard/admin/factures.html'


class StatistiquesView(TemplateView):
    """Statistics and reports view"""
    template_name = 'dashboard/admin/statistiques.html'


class ParametresView(TemplateView):
    """Settings view"""
    template_name = 'dashboard/admin/parametres.html'


class ProfilView(TemplateView):
    """User profile view"""
    template_name = 'dashboard/admin/profil.html'


class IntelligenceView(TemplateView):
    """Intelligence Hub view"""
    template_name = 'dashboard/admin/intelligence.html'


# Vues par Rôle
class CaissierView(TemplateView):
    """Cashier POS view"""
    template_name = 'dashboard/roles/caissier.html'


class GestionnaireStockView(TemplateView):
    """Stock Manager view"""
    template_name = 'dashboard/roles/gestionnaire_stock.html'


class ComptableView(TemplateView):
    """Accountant view"""
    template_name = 'dashboard/roles/comptable.html'


class GerantView(TemplateView):
    """Manager operational dashboard view"""
    template_name = 'dashboard/roles/gerant.html'


class VendeurView(TemplateView):
    """Salesperson interface view"""
    template_name = 'dashboard/roles/vendeur.html'


# Function-based views (alternative)
def home(request):
    """Landing page"""
    return render(request, 'home.html')


def login_page(request):
    """Login page"""
    return render(request, 'auth/login.html')


def register_page(request):
    """Registration page"""
    return render(request, 'auth/register.html')


def forgot_password_page(request):
    """Forgot password page"""
    return render(request, 'auth/forgot_password.html')


def loading_page(request):
    """Loading page"""
    return render(request, 'loading.html')


def onboarding_page(request):
    """Onboarding page"""
    return render(request, 'onboarding.html')


def dashboard_page(request):
    """Dashboard page"""
    return render(request, 'dashboard/admin/index.html')
