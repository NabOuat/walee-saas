"""
Commande pour initialiser les intégrations Walee
Usage: python manage.py init_integrations
"""
from django.core.management.base import BaseCommand
from accounts.integrations.models import CategorieIntegration, Integration


class Command(BaseCommand):
    help = 'Initialise les intégrations Walee'

    def handle(self, *args, **options):
        self.stdout.write('Initialisation des integrations Walee...\n')
        
        # Créer les catégories
        categories = self.creer_categories()
        
        # Créer les intégrations
        self.creer_integrations(categories)
        
        self.stdout.write(self.style.SUCCESS('\nIntegrations initialisees avec succes !'))

    def creer_categories(self):
        """Crée les catégories d'intégrations"""
        self.stdout.write('Creation des categories...')
        
        categories_data = [
            {
                'nom': 'Gestion',
                'slug': 'gestion',
                'description': 'Outils de gestion quotidienne',
                'icone': 'briefcase',
                'couleur': '#10B981',
                'ordre': 1
            },
            {
                'nom': 'Intelligence',
                'slug': 'intelligence',
                'description': 'Intelligence artificielle et automatisation',
                'icone': 'brain',
                'couleur': '#8B5CF6',
                'ordre': 2
            },
            {
                'nom': 'Communication',
                'slug': 'communication',
                'description': 'Communication avec vos clients',
                'icone': 'message-circle',
                'couleur': '#3B82F6',
                'ordre': 3
            },
            {
                'nom': 'Paiement',
                'slug': 'paiement',
                'description': 'Solutions de paiement',
                'icone': 'credit-card',
                'couleur': '#F59E0B',
                'ordre': 4
            },
        ]
        
        categories = {}
        for data in categories_data:
            cat, created = CategorieIntegration.objects.get_or_create(
                slug=data['slug'],
                defaults=data
            )
            categories[data['slug']] = cat
            status = 'Creee' if created else 'Existe deja'
            self.stdout.write(f'  {status}: {cat.nom}')
        
        return categories

    def creer_integrations(self, categories):
        """Crée les intégrations"""
        self.stdout.write('\nCreation des integrations...')
        
        integrations_data = [
            # GESTION
            {
                'categorie': categories['gestion'],
                'nom': 'Walee Réservations',
                'slug': 'walee-reservations',
                'description': 'Système de réservation intelligent pour gérer vos rendez-vous, tables, chambres. Calendrier en temps réel, rappels automatiques, gestion des annulations.',
                'description_courte': 'Gestion intelligente des réservations',
                'icone': 'calendar-check',
                'couleur': '#10B981',
                'types_entreprise': ['hotel', 'restaurant', 'lavage', 'salon'],
                'actif_par_defaut': True,
                'gratuit': True,
                'fonctionnalites': [
                    'Calendrier en temps réel',
                    'Rappels SMS automatiques',
                    'Gestion des annulations',
                    'Liste d\'attente',
                    'Acomptes en ligne'
                ],
                'populaire': True,
                'ordre': 1
            },
            {
                'categorie': categories['gestion'],
                'nom': 'Walee Stock',
                'slug': 'walee-stock',
                'description': 'Gestion de stock intelligente avec alertes automatiques, prédictions de rupture, suggestions de commandes. Scan code-barres, inventaire rapide.',
                'description_courte': 'Gestion de stock prédictive',
                'icone': 'package',
                'couleur': '#10B981',
                'types_entreprise': ['supermarche', 'superette', 'restaurant', 'hotel', 'pharmacie'],
                'actif_par_defaut': True,
                'gratuit': True,
                'fonctionnalites': [
                    'Alertes de rupture',
                    'Prédictions intelligentes',
                    'Scan code-barres',
                    'Inventaire rapide',
                    'Analyse de rotation'
                ],
                'populaire': True,
                'ordre': 2
            },
            {
                'categorie': categories['gestion'],
                'nom': 'Walee Caisse',
                'slug': 'walee-caisse',
                'description': 'Caisse ultra-rapide et moderne. Vente en 3 clics, mode hors-ligne, multi-paiements, facture instantanée. Parfait pour les heures de pointe.',
                'description_courte': 'Caisse rapide et moderne',
                'icone': 'shopping-cart',
                'couleur': '#10B981',
                'types_entreprise': ['supermarche', 'superette', 'restaurant', 'bar', 'boutique'],
                'actif_par_defaut': True,
                'gratuit': True,
                'fonctionnalites': [
                    'Vente en 3 clics',
                    'Mode hors-ligne',
                    'Multi-paiements',
                    'Facture instantanée',
                    'Rapport de caisse'
                ],
                'populaire': True,
                'ordre': 3
            },
            {
                'categorie': categories['gestion'],
                'nom': 'Walee Livraison',
                'slug': 'walee-livraison',
                'description': 'Système de livraison intégré avec suivi en temps réel, gestion des livreurs, calcul automatique des tarifs selon la distance.',
                'description_courte': 'Livraison avec suivi en temps réel',
                'icone': 'truck',
                'couleur': '#10B981',
                'types_entreprise': ['restaurant', 'supermarche', 'lavage', 'pharmacie'],
                'actif_par_defaut': False,
                'gratuit': True,
                'fonctionnalites': [
                    'Suivi en temps réel',
                    'Gestion livreurs',
                    'Calcul automatique tarifs',
                    'App livreur',
                    'Notifications client'
                ],
                'ordre': 4
            },
            {
                'categorie': categories['gestion'],
                'nom': 'Walee Équipe',
                'slug': 'walee-equipe',
                'description': 'Gestion d\'équipe simplifiée : pointage digital, planning automatique, calcul salaires, performance employés, chat interne.',
                'description_courte': 'Gestion d\'équipe complète',
                'icone': 'users',
                'couleur': '#10B981',
                'types_entreprise': ['tous'],
                'actif_par_defaut': True,
                'gratuit': True,
                'fonctionnalites': [
                    'Pointage digital',
                    'Planning automatique',
                    'Calcul salaires',
                    'Performance employés',
                    'Chat interne'
                ],
                'ordre': 5
            },
            
            # INTELLIGENCE
            {
                'categorie': categories['intelligence'],
                'nom': 'Walee Intelligence',
                'slug': 'walee-intelligence',
                'description': 'Assistant IA personnalisé : prédictions de ventes, recommandations produits, optimisation des prix, analyse des tendances, alertes intelligentes.',
                'description_courte': 'Assistant IA pour votre business',
                'icone': 'brain',
                'couleur': '#8B5CF6',
                'types_entreprise': ['tous'],
                'actif_par_defaut': False,
                'gratuit': False,
                'prix_mensuel': 5000,
                'fonctionnalites': [
                    'Prédictions de ventes',
                    'Recommandations produits',
                    'Optimisation des prix',
                    'Analyse des tendances',
                    'Alertes intelligentes',
                    'Chatbot client'
                ],
                'populaire': True,
                'nouveau': True,
                'ordre': 1
            },
            {
                'categorie': categories['intelligence'],
                'nom': 'Walee Analytics',
                'slug': 'walee-analytics',
                'description': 'Tableaux de bord personnalisés avec graphiques en temps réel, KPIs, comparaisons, prévisions, rapports automatiques.',
                'description_courte': 'Tableaux de bord intelligents',
                'icone': 'bar-chart-2',
                'couleur': '#8B5CF6',
                'types_entreprise': ['tous'],
                'actif_par_defaut': True,
                'gratuit': True,
                'fonctionnalites': [
                    'Graphiques temps réel',
                    'KPIs personnalisés',
                    'Comparaisons',
                    'Prévisions',
                    'Export Excel'
                ],
                'ordre': 2
            },
            
            # COMMUNICATION
            {
                'categorie': categories['communication'],
                'nom': 'Walee Fidélité',
                'slug': 'walee-fidelite',
                'description': 'Programme de fidélité clé en main : points, coupons, récompenses anniversaire, carte digitale, challenges, parrainage, niveaux VIP.',
                'description_courte': 'Programme de fidélité automatisé',
                'icone': 'gift',
                'couleur': '#3B82F6',
                'types_entreprise': ['restaurant', 'supermarche', 'lavage', 'salon', 'boutique'],
                'actif_par_defaut': False,
                'gratuit': True,
                'fonctionnalites': [
                    'Points de fidélité',
                    'Coupons automatiques',
                    'Récompenses anniversaire',
                    'Carte digitale QR',
                    'Challenges',
                    'Parrainage'
                ],
                'populaire': True,
                'ordre': 1
            },
            {
                'categorie': categories['communication'],
                'nom': 'Walee Marketing',
                'slug': 'walee-marketing',
                'description': 'Marketing automation : SMS de masse, messages anniversaire, campagnes ciblées, coupons personnalisés, WhatsApp Business.',
                'description_courte': 'Marketing automation local',
                'icone': 'megaphone',
                'couleur': '#3B82F6',
                'types_entreprise': ['tous'],
                'actif_par_defaut': False,
                'gratuit': False,
                'prix_mensuel': 3000,
                'fonctionnalites': [
                    'SMS de masse',
                    'Messages anniversaire',
                    'Campagnes ciblées',
                    'Coupons personnalisés',
                    'WhatsApp Business'
                ],
                'ordre': 2
            },
            
            # PAIEMENT
            {
                'categorie': categories['paiement'],
                'nom': 'Walee Pay',
                'slug': 'walee-pay',
                'description': 'Solution de paiement tout-en-un : Mobile Money (Wave, Orange, MTN, Moov), cartes bancaires, cash. Paiements en ligne et en boutique.',
                'description_courte': 'Paiements Mobile Money & Cartes',
                'icone': 'credit-card',
                'couleur': '#F59E0B',
                'types_entreprise': ['tous'],
                'actif_par_defaut': True,
                'gratuit': True,
                'necessite_configuration': True,
                'fonctionnalites': [
                    'Wave Mobile Money',
                    'Orange Money',
                    'MTN Mobile Money',
                    'Moov Money',
                    'Cartes bancaires',
                    'Paiement en ligne'
                ],
                'populaire': True,
                'ordre': 1
            },
        ]
        
        for data in integrations_data:
            integration, created = Integration.objects.get_or_create(
                slug=data['slug'],
                defaults=data
            )
            status = 'Creee' if created else 'Existe deja'
            self.stdout.write(f'  {status}: {integration.nom}')
