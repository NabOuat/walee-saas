from rest_framework import serializers

from .models import (AvisProduits,BonsCommande,Caisses,CategoriesClients,CategoriesIntegration,
                        CategoriesProduits,Clients,CodesPromo,Commandes,CommandesMarketplace,ConfigMarketplace,DemandesAchat,
                        Devis,EcrituresComptables,Employes,EmployesRoles,Entrepots,Factures,FacturesFournisseurs,Favoris,Fournisseurs
                        ,Integrations,IntegrationsUtilisateur,Inventaires,JournalActivites,JournauxComptables,
                        LignesBonsCommande,LignesCommandes,LignesDemandesAchat,LignesDevis,LignesEcritures,
                        LignesFactures,LignesInventaire,LignesReceptions,Marques,ModesPaiement,
                        MouvementsStock,Notifications,Organisations,Paiements,PaiementsFournisseurs,
                        PaniersAbandonnes,ParametresOrganisation,PlanComptable,PlansAbonnement,PreferencesNotificationsUtilisateur,
                        Produits,ReceptionsMarchandises,Roles,SequencesNumerotation,SessionsCaisse,SessionsUtilisateur,
                        Stocks,Taxes,TransactionsCaisse,TypesNotifications,TypeOrganisations,UnitesMesure,Utilisateurs,UtilisateursOrganisations,
                        UtilisationsCodesPromo,VariantesProduits,Pays)


# --- Modèles d'Authentification (Généralement non nécessaires pour une API métier, mais inclus à titre d'exemple) ---

class AvisProduitsSerializer(serializers.ModelSerializer):
    client_nom = serializers.CharField(source='client.nom_complet', read_only=True)
    produit_nom = serializers.CharField(source='produit.nom', read_only=True) # Assuming 'Produits' model has a 'nom' field

    class Meta:
        model = AvisProduits
        fields = '__all__'
        read_only_fields = ['date_moderation', 'achat_verifie', 'date_creation']


class BonsCommandeSerializer(serializers.ModelSerializer):
    fournisseur_nom = serializers.CharField(source='fournisseur.nom', read_only=True) # Assuming 'Fournisseurs' model has a 'nom' field

    class Meta:
        model = BonsCommande
        fields = '__all__'


class CaissesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Caisses
        fields = '__all__'


class CategoriesClientsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoriesClients
        fields = '__all__'


class CategoriesProduitsSerializer(serializers.ModelSerializer):
    parent_nom = serializers.CharField(source='parent.nom', read_only=True)

    class Meta:
        model = CategoriesProduits
        fields = '__all__'


class ClientsSerializer(serializers.ModelSerializer):
    categorie_nom = serializers.CharField(source='categorie.nom', read_only=True)
    
    class Meta:
        model = Clients
        fields = '__all__' # ou listez les champs spécifiques
        read_only_fields = ['nom_complet', 'nombre_commandes', 'montant_total_achats', 'date_creation', 'date_modification']


class CodesPromoSerializer(serializers.ModelSerializer):
    class Meta:
        model = CodesPromo
        fields = '__all__'


class CommandesSerializer(serializers.ModelSerializer):
    client_info = ClientsSerializer(source='client', read_only=True) # Utilise le serializer Client pour plus de détails
    employe_nom = serializers.CharField(source='employe.nom_complet', read_only=True)

    class Meta:
        model = Commandes
        fields = '__all__'
        read_only_fields = ['montant_paye', 'montant_restant', 'date_creation', 'date_modification']


class ConfigMarketplaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConfigMarketplace
        fields = '__all__'


class DevisSerializer(serializers.ModelSerializer):
    # Pour afficher le nom du client au lieu de son ID
    client_nom = serializers.CharField(source='client.nom_complet', read_only=True) 
    
    class Meta:
        model = Devis
        fields = '__all__'
        read_only_fields = ['commande_id', 'date_conversion', 'date_creation', 'date_modification']


class DemandesAchatSerializer(serializers.ModelSerializer):
    demandeur_nom = serializers.CharField(source='demandeur.nom_complet', read_only=True)

    class Meta:
        model = DemandesAchat
        fields = '__all__'

class EmployesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employes
        fields = '__all__'
        read_only_fields = ['nom_complet', 'date_creation', 'date_modification']

class EntrepotsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Entrepots
        fields = '__all__'
        unique_together = (('organisation', 'code_entrepot'),)

class FacturesSerializer(serializers.ModelSerializer):
    client_nom = serializers.CharField(source='client.nom_complet', read_only=True)

    class Meta:
        model = Factures
        fields = '__all__'
        read_only_fields = ['montant_paye', 'montant_restant', 'date_creation', 'date_modification']


class FacturesFournisseursSerializer(serializers.ModelSerializer):
    fournisseur_nom = serializers.CharField(source='fournisseur.raison_sociale', read_only=True)
    bon_commande_numero = serializers.CharField(source='bon_commande.numero_bon_commande', read_only=True)

    class Meta:
        model = FacturesFournisseurs
        fields = '__all__'
        read_only_fields = ['montant_paye', 'montant_restant', 'date_validation', 'date_creation', 'date_modification']


class FavorisSerializer(serializers.ModelSerializer):
    produit_designation = serializers.CharField(source='produit.designation', read_only=True)
    client_nom = serializers.CharField(source='client.nom_complet', read_only=True)

    class Meta:
        model = Favoris
        fields = '__all__'
        unique_together = (('client', 'produit'),)


class FournisseursSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fournisseurs
        fields = '__all__'
        read_only_fields = ['note_qualite', 'note_delais', 'note_prix', 'nombre_commandes', 'montant_total_achats', 'derniere_commande', 'date_creation', 'date_modification']


class InventairesSerializer(serializers.ModelSerializer):
    entrepot_nom = serializers.CharField(source='entrepot.nom', read_only=True)

    class Meta:
        model = Inventaires
        fields = '__all__'
        read_only_fields = ['nombre_produits_comptes', 'ecarts_positifs_valeur', 'ecarts_negatifs_valeur', 'date_validation']


class JournalActivitesSerializer(serializers.ModelSerializer):
    utilisateur_email = serializers.CharField(source='utilisateur.email', read_only=True)
    employe_nom = serializers.CharField(source='employe.nom_complet', read_only=True)

    class Meta:
        model = JournalActivites
        fields = '__all__'
        read_only_fields = ['date_action']


class JournauxComptablesSerializer(serializers.ModelSerializer):
    class Meta:
        model = JournauxComptables
        fields = '__all__'


class LignesBonsCommandeSerializer(serializers.ModelSerializer):
    produit_designation = serializers.CharField(source='produit.designation', read_only=True) # Supposant 'Produits' a un champ 'designation'

    class Meta:
        model = LignesBonsCommande
        fields = '__all__'
        read_only_fields = ['quantite_restante', 'montant_ht', 'montant_tva', 'montant_ttc']


class LignesCommandesSerializer(serializers.ModelSerializer):
    produit_designation = serializers.CharField(source='produit.designation', read_only=True)

    class Meta:
        model = LignesCommandes
        fields = '__all__'
        read_only_fields = ['quantite_livree', 'montant_ht', 'montant_tva', 'montant_ttc']


class LignesDevisSerializer(serializers.ModelSerializer):
    produit_designation = serializers.CharField(source='produit.designation', read_only=True)

    class Meta:
        model = LignesDevis
        fields = '__all__'
        read_only_fields = ['montant_ht', 'montant_tva', 'montant_ttc']


class LignesDemandesAchatSerializer(serializers.ModelSerializer):
    produit_designation = serializers.CharField(source='produit.designation', read_only=True)

    class Meta:
        model = LignesDemandesAchat
        fields = '__all__'


class LignesEcrituresSerializer(serializers.ModelSerializer):
    # Supposant que 'PlanComptable' a un champ 'numero_compte'
    compte_numero = serializers.CharField(source='compte.numero_compte', read_only=True)

    class Meta:
        model = LignesEcritures
        fields = '__all__'
        read_only_fields = ['date_lettrage']


class LignesFacturesSerializer(serializers.ModelSerializer):
    produit_designation = serializers.CharField(source='produit.designation', read_only=True)

    class Meta:
        model = LignesFactures
        fields = '__all__'
        read_only_fields = ['montant_ht', 'montant_tva', 'montant_ttc']


class LignesInventaireSerializer(serializers.ModelSerializer):
    # Supposant que 'Stocks' a une relation vers 'Produits' pour obtenir la designation
    produit_designation = serializers.CharField(source='stock.produit.designation', read_only=True)

    class Meta:
        model = LignesInventaire
        fields = '__all__'
        read_only_fields = ['ecart', 'valeur_ecart', 'date_comptage']


class LignesReceptionsSerializer(serializers.ModelSerializer):
    produit_designation = serializers.CharField(source='produit.designation', read_only=True)
    ligne_bon_commande_id = serializers.UUIDField(source='ligne_bon_commande.id', read_only=True)

    class Meta:
        model = LignesReceptions
        fields = '__all__'
        read_only_fields = ['quantite_commandee', 'quantite_acceptee', 'quantite_rejetee']


class MarquesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Marques
        fields = '__all__'


class ModesPaiementSerializer(serializers.ModelSerializer):
    class Meta:
        model = ModesPaiement
        fields = '__all__'


class MouvementsStockSerializer(serializers.ModelSerializer):
    entrepot_origine_nom = serializers.CharField(source='entrepot_origine.nom', read_only=True)
    entrepot_destination_nom = serializers.CharField(source='entrepot_destination.nom', read_only=True)
    # Supposant que 'Stocks' a une relation vers 'Produits' pour obtenir la designation
    produit_designation = serializers.CharField(source='stock.produit.designation', read_only=True)

    class Meta:
        model = MouvementsStock
        fields = '__all__'
        read_only_fields = ['quantite_avant', 'quantite_apres', 'valeur_totale', 'date_mouvement']


class NotificationsSerializer(serializers.ModelSerializer):
    # Supposant que 'TypesNotifications' a un champ 'nom'
    type_notification_nom = serializers.CharField(source='type_notification.nom', read_only=True)

    class Meta:
        model = Notifications
        fields = '__all__'


class OrganisationsSerializer(serializers.ModelSerializer):
    proprietaire_email = serializers.CharField(source='utilisateurs.email', read_only=True)
    pays_nom = serializers.CharField(source='pays.nom', read_only=True)
    plan_nom = serializers.CharField(source='plan.nom', read_only=True)
    type_organisation_nom = serializers.CharField(source='type_organisation.nom', read_only=True)

    class Meta:
        model = Organisations
        fields = '__all__'
        read_only_fields = [
            'date_debut_abonnement', 'date_fin_abonnement', 'date_fin_essai',
            'verifie', 'date_verification', 'date_creation', 'date_modification',
            'date_suppression'
        ]


class PaiementsSerializer(serializers.ModelSerializer):
    mode_paiement_nom = serializers.CharField(source='mode_paiement.nom', read_only=True)
    facture_numero = serializers.CharField(source='facture.numero_facture', read_only=True)
    commande_numero = serializers.CharField(source='commande.numero_commande', read_only=True)
    client_nom = serializers.CharField(source='client.nom_commercial', read_only=True)

    class Meta:
        model = Paiements
        fields = '__all__'
        read_only_fields = ['montant_net', 'date_creation', 'date_validation']


class PaiementsFournisseursSerializer(serializers.ModelSerializer):
    mode_paiement_nom = serializers.CharField(source='mode_paiement.nom', read_only=True)
    fournisseur_nom = serializers.CharField(source='fournisseur.raison_sociale', read_only=True)
    facture_fournisseur_numero = serializers.CharField(source='facture_fournisseur.numero_facture_fournisseur', read_only=True)

    class Meta:
        model = PaiementsFournisseurs
        fields = '__all__'
        read_only_fields = ['date_creation']


class PaniersAbandonnesSerializer(serializers.ModelSerializer):
    client_nom = serializers.CharField(source='client.nom_commercial', read_only=True)
    commande_numero = serializers.CharField(source='commande.numero_commande', read_only=True)

    class Meta:
        model = PaniersAbandonnes
        fields = '__all__'
        read_only_fields = ['converti', 'date_creation', 'date_derniere_modification']


class PlanComptableSerializer(serializers.ModelSerializer):
    compte_parent_numero = serializers.CharField(source='compte_parent.numero_compte', read_only=True)

    class Meta:
        model = PlanComptable
        fields = '__all__'
        read_only_fields = ['niveau', 'date_creation']


class PlansAbonnementSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlansAbonnement
        fields = '__all__'
        read_only_fields = ['date_creation']


class ParametresOrganisationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParametresOrganisation
        fields = '__all__'
        read_only_fields = ['date_modification']


class PaysSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pays
        fields = '__all__'
        read_only_fields = ['created_at']


class PreferencesNotificationsUtilisateurSerializer(serializers.ModelSerializer):
    utilisateur_email = serializers.CharField(source='utilisateur.email', read_only=True)
    # Supposant que 'TypesNotifications' a un champ 'nom'
    type_notification_nom = serializers.CharField(source='type_notification.nom', read_only=True)

    class Meta:
        model = PreferencesNotificationsUtilisateur
        fields = '__all__'
        unique_together = (('utilisateur', 'type_notification'),)


class ProduitsSerializer(serializers.ModelSerializer):
    categorie_nom = serializers.CharField(source='categorie.nom', read_only=True)
    marque_nom = serializers.CharField(source='marque.nom', read_only=True)
    unite_mesure_nom = serializers.CharField(source='unite_mesure.nom', read_only=True)

    class Meta:
        model = Produits
        fields = '__all__'
        read_only_fields = ['prix_vente_ttc', 'marge_calculee', 'date_creation', 'date_modification', 'date_suppression']


class ReceptionsMarchandisesSerializer(serializers.ModelSerializer):
    bon_commande_numero = serializers.CharField(source='bon_commande.numero_bon_commande', read_only=True)
    entrepot_nom = serializers.CharField(source='entrepot.nom', read_only=True)
    receptionne_par_nom = serializers.CharField(source='receptionne_par.nom_complet', read_only=True)

    class Meta:
        model = ReceptionsMarchandises
        fields = '__all__'
        read_only_fields = ['date_validation', 'date_creation']


class RolesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Roles
        fields = '__all__'
        read_only_fields = ['systeme', 'date_creation']


class SequencesNumerotationSerializer(serializers.ModelSerializer):
    class Meta:
        model = SequencesNumerotation
        fields = '__all__'
        read_only_fields = ['valeur_actuelle', 'dernier_reset', 'date_creation']


class SessionsCaisseSerializer(serializers.ModelSerializer):
    caisse_nom = serializers.CharField(source='caisse.nom', read_only=True)
    caissier_nom = serializers.CharField(source='caissier.nom_complet', read_only=True)

    class Meta:
        model = SessionsCaisse
        fields = '__all__'
        read_only_fields = [
            'date_fermeture', 'total_ventes_especes', 'total_ventes_carte',
            'total_ventes_mobile', 'total_ventes_autres', 'total_ventes',
            'montant_theorique_especes', 'ecart_especes', 'nombre_ventes',
            'nombre_clients', 'ticket_moyen', 'date_validation'
        ]


class SessionsUtilisateurSerializer(serializers.ModelSerializer):
    utilisateur_email = serializers.CharField(source='utilisateur.email', read_only=True)

    class Meta:
        model = SessionsUtilisateur
        fields = '__all__'
        read_only_fields = ['date_creation', 'derniere_activite']


class StocksSerializer(serializers.ModelSerializer):
    produit_nom = serializers.CharField(source='produit.nom', read_only=True)
    entrepot_nom = serializers.CharField(source='entrepot.nom', read_only=True)

    class Meta:
        model = Stocks
        fields = '__all__'
        read_only_fields = [
            'quantite_disponible', 'quantite_reservee', 'quantite_en_commande',
            'quantite_totale', 'valeur_stock_achat', 'valeur_stock_vente',
            'date_dernier_mouvement', 'date_derniere_entree', 'date_derniere_sortie',
            'date_dernier_inventaire', 'date_modification'
        ]


class TaxesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Taxes
        fields = '__all__'
        read_only_fields = ['date_creation']


class TransactionsCaisseSerializer(serializers.ModelSerializer):
    session_caisse_numero = serializers.CharField(source='session_caisse.numero_session', read_only=True)
    mode_paiement_nom = serializers.CharField(source='mode_paiement.nom', read_only=True)
    facture_numero = serializers.CharField(source='facture.numero_facture', read_only=True)
    commande_numero = serializers.CharField(source='commande.numero_commande', read_only=True)
    effectue_par_nom = serializers.CharField(source='effectue_par.nom_complet', read_only=True)

    class Meta:
        model = TransactionsCaisse
        fields = '__all__'
        read_only_fields = ['date_transaction']


class TypesNotificationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = TypesNotifications
        fields = '__all__'

class TypeOrganisationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = TypeOrganisations
        fields = '__all__'

class UnitesMesureSerializer(serializers.ModelSerializer):
    class Meta:
        model = UnitesMesure
        fields = '__all__'


class UtilisationsCodesPromoSerializer(serializers.ModelSerializer):
    code_promo_code = serializers.CharField(source='code_promo.code', read_only=True)
    commande_numero = serializers.CharField(source='commande.numero_commande', read_only=True)
    client_nom = serializers.CharField(source='client.nom_complet', read_only=True)

    class Meta:
        model = UtilisationsCodesPromo
        fields = '__all__'
        read_only_fields = ['montant_reduction', 'date_utilisation']


class UtilisateursSerializer(serializers.ModelSerializer):
    class Meta:
        model = Utilisateurs
        fields = '__all__'
        # Champs sensibles et calculés en lecture seule
        read_only_fields = [
            'date_verification_email', 'date_creation', 'date_modification',
            'date_suppression', 'derniere_connexion', 'is_superuser', 'is_staff',
            'telephone_verifie', 'date_verification_telephone'
        ]
        # Le mot de passe ne doit être écrit que lors de la création/mise à jour
        extra_kwargs = {
            'password': {'write_only': True, 'required': False}
        }


class UtilisateursOrganisationsSerializer(serializers.ModelSerializer):
    utilisateur_email = serializers.CharField(source='utilisateur.email', read_only=True)
    organisation_nom = serializers.CharField(source='organisation.nom_commercial', read_only=True)
    ajoute_par_email = serializers.CharField(source='ajoute_par.email', read_only=True)

    class Meta:
        model = UtilisateursOrganisations
        fields = '__all__'
        read_only_fields = ['date_ajout']
        unique_together = (('utilisateur', 'organisation'),)


class VariantesProduitsSerializer(serializers.ModelSerializer):
    produit_nom = serializers.CharField(source='produit.nom', read_only=True)

    class Meta:
        model = VariantesProduits
        fields = '__all__'
        read_only_fields = ['prix_vente_ttc', 'date_creation']