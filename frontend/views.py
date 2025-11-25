"""
Views for frontend pages (authentication and landing page)
"""
from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin



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
    """Registration page view with OTP"""
    template_name = 'auth/register_otp.html'


class ForgotPasswordView(TemplateView):
    """Forgot password page view with OTP"""
    template_name = 'auth/forgot_password_otp.html'


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


class CaisseView(TemplateView):
    """Point of Sale (POS) view"""
    template_name = 'dashboard/admin/caisse.html'


class VentesView(TemplateView):
    """Sales management view"""
    template_name = 'dashboard/admin/ventes.html'


class StockView(TemplateView):
    """Stock management view"""
    template_name = 'dashboard/admin/stock.html'


class IntegrationsView(LoginRequiredMixin, TemplateView):
    """Integrations management view"""
    template_name = 'integrations/index.html'
    login_url = '/login/'


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
    """Cashier view"""
    template_name = 'dashboard/roles/caissier/dashboard.html'


class CaissierMesVentesView(TemplateView):
    """Cashier sales history view"""
    template_name = 'dashboard/roles/caissier/mes_ventes.html'


class CaissierSessionView(TemplateView):
    """Cashier session management view"""
    template_name = 'dashboard/roles/caissier/ma_session.html'


class CaissierClientsView(TemplateView):
    """Cashier clients management view"""
    template_name = 'dashboard/roles/caissier/clients.html'


class CaissierAideView(TemplateView):
    """Cashier help and support view"""
    template_name = 'dashboard/roles/caissier/aide.html'


class GestionnaireStockView(TemplateView):
    """Stock manager view"""
    template_name = 'dashboard/roles/gestionnaire_stock/dashboard.html'


class StockInventaireView(TemplateView):
    """Stock inventory view"""
    template_name = 'dashboard/roles/gestionnaire_stock/inventaire.html'


class StockMouvementsView(TemplateView):
    """Stock movements view"""
    template_name = 'dashboard/roles/gestionnaire_stock/mouvements.html'


class StockAlertesView(TemplateView):
    """Stock alerts view"""
    template_name = 'dashboard/roles/gestionnaire_stock/alertes.html'


class StockFournisseursView(TemplateView):
    """Stock suppliers view"""
    template_name = 'dashboard/roles/gestionnaire_stock/fournisseurs.html'


class StockStatsView(TemplateView):
    """Stock statistics view"""
    template_name = 'dashboard/roles/gestionnaire_stock/stats.html'


class ComptableView(TemplateView):
    """Accountant view"""
    template_name = 'dashboard/roles/comptable/dashboard.html'


class ComptableFacturationView(TemplateView):
    """Accountant invoicing view"""
    template_name = 'dashboard/roles/comptable/facturation.html'


class ComptableDepensesTresorerieView(TemplateView):
    """Accountant expenses and treasury view"""
    template_name = 'dashboard/roles/comptable/depenses_tresorerie.html'


class ComptableComptabiliteView(TemplateView):
    """Accountant accounting entries view"""
    template_name = 'dashboard/roles/comptable/comptabilite.html'


class ComptableRapportsView(TemplateView):
    """Accountant financial reports view"""
    template_name = 'dashboard/roles/comptable/rapports.html'


class ComptableExportsView(TemplateView):
    """Accountant exports and archives view"""
    template_name = 'dashboard/roles/comptable/exports.html'


class VendeurView(TemplateView):
    """Salesperson view"""
    template_name = 'dashboard/roles/vendeur/dashboard.html'


class VendeurMesVentesView(TemplateView):
    """Salesperson sales view"""
    template_name = 'dashboard/roles/vendeur/mes_ventes.html'


class VendeurDevisView(TemplateView):
    """Salesperson quotes view"""
    template_name = 'dashboard/roles/vendeur/mes_devis.html'


class VendeurCommandesView(TemplateView):
    """Salesperson orders view"""
    template_name = 'dashboard/roles/vendeur/commandes.html'


class VendeurClientsView(TemplateView):
    """Salesperson clients view"""
    template_name = 'dashboard/roles/vendeur/clients.html'


class VendeurObjectifsView(TemplateView):
    """Salesperson objectives view"""
    template_name = 'dashboard/roles/vendeur/objectifs.html'


class VendeurStatsView(TemplateView):
    """Salesperson statistics view"""
    template_name = 'dashboard/roles/vendeur/stats.html'


class VendeurVenteView(TemplateView):
    """Salesperson new sale view"""
    template_name = 'dashboard/roles/vendeur/vente.html'


class CaissierCaisseView(TemplateView):
    """Cashier register view"""
    template_name = 'dashboard/roles/caissier/caisse.html'


class CaissierProduitsView(TemplateView):
    """Cashier products view"""
    template_name = 'dashboard/roles/caissier/produits.html'


class CaissierClientsView(TemplateView):
    """Cashier clients view"""
    template_name = 'dashboard/roles/caissier/clients.html'


class RHView(TemplateView):
    """HR view"""
    template_name = 'dashboard/roles/rh/dashboard.html'


class RHEmployeesView(TemplateView):
    """HR employees management view"""
    template_name = 'dashboard/roles/rh/employees.html'


class RHRecrutementView(TemplateView):
    """HR recruitment view"""
    template_name = 'dashboard/roles/rh/recrutement.html'


class RHCongesView(TemplateView):
    """HR leave management view"""
    template_name = 'dashboard/roles/rh/conges.html'


class RHAbsencesView(TemplateView):
    """HR absences view"""
    template_name = 'dashboard/roles/rh/absences.html'


class RHPaieView(TemplateView):
    """HR payroll view"""
    template_name = 'dashboard/roles/rh/paie.html'


class RHFormationsView(TemplateView):
    """HR training view"""
    template_name = 'dashboard/roles/rh/formations.html'


class RHEvaluationsView(TemplateView):
    """HR evaluations view"""
    template_name = 'dashboard/roles/rh/evaluations.html'


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


