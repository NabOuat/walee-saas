# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.

# python manage.py inspectdb > backend/walee/models.py

from django.db import models


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AvisProduits(models.Model):
    id = models.UUIDField(primary_key=True)
    organisation = models.ForeignKey('Organisations', models.DO_NOTHING)
    produit = models.ForeignKey('Produits', models.DO_NOTHING)
    client = models.ForeignKey('Clients', models.DO_NOTHING, blank=True, null=True)
    commande = models.ForeignKey('Commandes', models.DO_NOTHING, blank=True, null=True)
    note = models.IntegerField()
    titre = models.TextField(blank=True, null=True)
    commentaire = models.TextField(blank=True, null=True)
    statut = models.CharField(max_length=50, blank=True, null=True)
    modere_par = models.ForeignKey('Utilisateurs', models.DO_NOTHING, db_column='modere_par', blank=True, null=True)
    date_moderation = models.DateTimeField(blank=True, null=True)
    raison_rejet = models.TextField(blank=True, null=True)
    achat_verifie = models.BooleanField(blank=True, null=True)
    recommande = models.BooleanField(blank=True, null=True)
    photos_urls = models.TextField(blank=True, null=True)  # This field type is a guess.
    date_creation = models.DateTimeField(blank=True, null=True)
    date_modification = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'avis_produits'
        unique_together = (('client', 'produit', 'commande'),)


class BonsCommande(models.Model):
    id = models.UUIDField(primary_key=True)
    organisation = models.ForeignKey('Organisations', models.DO_NOTHING)
    numero_bon_commande = models.CharField(max_length=50)
    fournisseur = models.ForeignKey('Fournisseurs', models.DO_NOTHING)
    demande_achat = models.ForeignKey('DemandesAchat', models.DO_NOTHING, blank=True, null=True)
    date_commande = models.DateField()
    date_livraison_prevue = models.DateField(blank=True, null=True)
    date_livraison_reelle = models.DateField(blank=True, null=True)
    statut = models.CharField(max_length=50, blank=True, null=True)
    montant_ht = models.DecimalField(max_digits=14, decimal_places=2, blank=True, null=True)
    montant_tva = models.DecimalField(max_digits=14, decimal_places=2, blank=True, null=True)
    montant_ttc = models.DecimalField(max_digits=14, decimal_places=2, blank=True, null=True)
    entrepot_livraison = models.ForeignKey('Entrepots', models.DO_NOTHING, blank=True, null=True)
    adresse_livraison = models.JSONField(blank=True, null=True)
    conditions_paiement = models.TextField(blank=True, null=True)
    delai_paiement_jours = models.IntegerField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    cree_par = models.ForeignKey('Utilisateurs', models.DO_NOTHING, db_column='cree_par', blank=True, null=True)
    date_creation = models.DateTimeField(blank=True, null=True)
    date_modification = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'bons_commande'
        unique_together = (('organisation', 'numero_bon_commande'),)


class Caisses(models.Model):
    id = models.UUIDField(primary_key=True)
    organisation = models.ForeignKey('Organisations', models.DO_NOTHING)
    entrepot = models.ForeignKey('Entrepots', models.DO_NOTHING, blank=True, null=True)
    code_caisse = models.CharField(max_length=50)
    nom = models.CharField(max_length=100)
    type = models.CharField(max_length=50, blank=True, null=True)
    emplacement = models.TextField(blank=True, null=True)
    imprimante_ticket = models.CharField(max_length=200, blank=True, null=True)
    tiroir_caisse_connecte = models.BooleanField(blank=True, null=True)
    scanner_connecte = models.BooleanField(blank=True, null=True)
    modes_paiement_autorises = models.TextField(blank=True, null=True)  # This field type is a guess.
    ouverture_automatique = models.BooleanField(blank=True, null=True)
    fermeture_automatique = models.BooleanField(blank=True, null=True)
    montant_fond_caisse = models.DecimalField(max_digits=14, decimal_places=2, blank=True, null=True)
    actif = models.BooleanField(blank=True, null=True)
    date_creation = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'caisses'
        unique_together = (('organisation', 'code_caisse'),)
        db_table_comment = 'Points de vente physiques ou virtuels'


class CategoriesClients(models.Model):
    id = models.UUIDField(primary_key=True)
    organisation = models.ForeignKey('Organisations', models.DO_NOTHING)
    nom = models.CharField(max_length=100)
    code = models.CharField(max_length=50, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    remise_defaut = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    couleur = models.CharField(max_length=7, blank=True, null=True)
    actif = models.BooleanField(blank=True, null=True)
    date_creation = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'categories_clients'
        unique_together = (('organisation', 'code'),)


class CategoriesIntegration(models.Model):
    id = models.UUIDField(primary_key=True)
    nom = models.CharField(max_length=100)
    slug = models.CharField(unique=True, max_length=50)
    description = models.TextField()
    icone = models.CharField(max_length=50)
    couleur = models.CharField(max_length=20)
    ordre = models.IntegerField()
    date_creation = models.DateTimeField()
    date_modification = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'categories_integration'


class CategoriesProduits(models.Model):
    id = models.UUIDField(primary_key=True)
    organisation = models.ForeignKey('Organisations', models.DO_NOTHING)
    parent = models.ForeignKey('self', models.DO_NOTHING, blank=True, null=True)
    nom = models.CharField(max_length=200)
    code = models.CharField(max_length=50, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    image_url = models.TextField(blank=True, null=True)
    visible_marketplace = models.BooleanField(blank=True, null=True)
    ordre_affichage = models.IntegerField(blank=True, null=True)
    actif = models.BooleanField(blank=True, null=True)
    date_creation = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'categories_produits'
        unique_together = (('organisation', 'code'),)


class Clients(models.Model):
    id = models.UUIDField(primary_key=True)
    organisation = models.ForeignKey('Organisations', models.DO_NOTHING)
    code_client = models.CharField(max_length=50)
    type_client = models.CharField(max_length=50, blank=True, null=True)
    categorie = models.ForeignKey(CategoriesClients, models.DO_NOTHING, blank=True, null=True)
    civilite = models.CharField(max_length=10, blank=True, null=True)
    nom = models.TextField(blank=True, null=True)
    prenom = models.TextField(blank=True, null=True)
    nom_complet = models.TextField(blank=True, null=True)
    date_naissance = models.DateField(blank=True, null=True)
    raison_sociale = models.TextField(blank=True, null=True)
    numero_identification = models.TextField(blank=True, null=True)
    numero_tva = models.TextField(blank=True, null=True)
    email = models.TextField(blank=True, null=True)
    telephone_principal = models.TextField(blank=True, null=True)
    telephone_secondaire = models.TextField(blank=True, null=True)
    site_web = models.TextField(blank=True, null=True)
    adresse_facturation = models.JSONField(blank=True, null=True)
    adresse_livraison = models.JSONField(blank=True, null=True)
    source_acquisition = models.CharField(max_length=100, blank=True, null=True)
    represente_par = models.TextField(blank=True, null=True)
    conditions_paiement = models.CharField(max_length=100, blank=True, null=True)
    plafond_credit = models.DecimalField(max_digits=14, decimal_places=2, blank=True, null=True)
    remise_permanente = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    tags = models.TextField(blank=True, null=True)  # This field type is a guess.
    actif = models.BooleanField(blank=True, null=True)
    blackliste = models.BooleanField(blank=True, null=True)
    raison_blacklist = models.TextField(blank=True, null=True)
    nombre_commandes = models.IntegerField(blank=True, null=True)
    montant_total_achats = models.DecimalField(max_digits=14, decimal_places=2, blank=True, null=True)
    montant_credit_restant = models.DecimalField(max_digits=14, decimal_places=2, blank=True, null=True)
    derniere_commande = models.DateTimeField(blank=True, null=True)
    cree_par = models.ForeignKey('Utilisateurs', models.DO_NOTHING, db_column='cree_par', blank=True, null=True)
    date_creation = models.DateTimeField(blank=True, null=True)
    date_modification = models.DateTimeField(blank=True, null=True)
    date_suppression = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'clients'
        unique_together = (('organisation', 'code_client'),)
        db_table_comment = 'Clients des organisations (B2C et B2B)'


class Codepostal(models.Model):
    id = models.BigAutoField(primary_key=True)
    code = models.CharField()
    created_at = models.DateTimeField()
    pays = models.ForeignKey('Pays', models.DO_NOTHING, db_column='pays', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'codePostal'
        db_table_comment = 'Code Postal en fonction de chaque pays'


class CodesOtp(models.Model):
    id = models.UUIDField(primary_key=True)
    utilisateur = models.ForeignKey('Utilisateurs', models.DO_NOTHING)
    type = models.CharField(max_length=20)
    email = models.CharField(max_length=255, blank=True, null=True)
    telephone = models.CharField(max_length=20, blank=True, null=True)
    code = models.CharField(max_length=6)
    motif = models.CharField(max_length=50)
    utilise = models.BooleanField(blank=True, null=True)
    date_utilisation = models.DateTimeField(blank=True, null=True)
    tentatives = models.IntegerField(blank=True, null=True)
    max_tentatives = models.IntegerField(blank=True, null=True)
    date_creation = models.DateTimeField(blank=True, null=True)
    date_expiration = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'codes_otp'


class CodesPromo(models.Model):
    id = models.UUIDField(primary_key=True)
    organisation = models.ForeignKey('Organisations', models.DO_NOTHING)
    code = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)
    type_reduction = models.CharField(max_length=50)
    valeur_reduction = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    montant_minimum = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    montant_maximum = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    categories_autorisees = models.TextField(blank=True, null=True)  # This field type is a guess.
    produits_autorises = models.TextField(blank=True, null=True)  # This field type is a guess.
    clients_autorises = models.TextField(blank=True, null=True)  # This field type is a guess.
    premiere_commande_uniquement = models.BooleanField(blank=True, null=True)
    nombre_utilisations_max = models.IntegerField(blank=True, null=True)
    nombre_utilisations_par_client = models.IntegerField(blank=True, null=True)
    nombre_utilisations_actuelles = models.IntegerField(blank=True, null=True)
    date_debut = models.DateTimeField()
    date_fin = models.DateTimeField()
    actif = models.BooleanField(blank=True, null=True)
    cree_par = models.ForeignKey('Utilisateurs', models.DO_NOTHING, db_column='cree_par', blank=True, null=True)
    date_creation = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'codes_promo'
        unique_together = (('organisation', 'code'),)


class Commandes(models.Model):
    id = models.UUIDField(primary_key=True)
    organisation = models.ForeignKey('Organisations', models.DO_NOTHING)
    numero_commande = models.CharField(max_length=50)
    reference_client = models.TextField(blank=True, null=True)
    client = models.ForeignKey(Clients, models.DO_NOTHING, blank=True, null=True)
    employe = models.ForeignKey('Employes', models.DO_NOTHING, blank=True, null=True)
    date_commande = models.DateField()
    date_livraison_prevue = models.DateField(blank=True, null=True)
    date_livraison_reelle = models.DateField(blank=True, null=True)
    statut = models.CharField(max_length=50, blank=True, null=True)
    statut_paiement = models.CharField(max_length=50, blank=True, null=True)
    origine = models.CharField(max_length=50, blank=True, null=True)
    devis = models.ForeignKey('Devis', models.DO_NOTHING, blank=True, null=True)
    montant_ht = models.DecimalField(max_digits=14, decimal_places=2, blank=True, null=True)
    montant_tva = models.DecimalField(max_digits=14, decimal_places=2, blank=True, null=True)
    montant_ttc = models.DecimalField(max_digits=14, decimal_places=2, blank=True, null=True)
    remise_globale = models.DecimalField(max_digits=14, decimal_places=2, blank=True, null=True)
    frais_livraison = models.DecimalField(max_digits=14, decimal_places=2, blank=True, null=True)
    montant_paye = models.DecimalField(max_digits=14, decimal_places=2, blank=True, null=True)
    montant_restant = models.DecimalField(max_digits=14, decimal_places=2, blank=True, null=True)
    adresse_livraison = models.JSONField(blank=True, null=True)
    methode_livraison = models.CharField(max_length=100, blank=True, null=True)
    numero_suivi = models.TextField(blank=True, null=True)
    transporteur = models.TextField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    notes_internes = models.TextField(blank=True, null=True)
    cree_par = models.ForeignKey('Utilisateurs', models.DO_NOTHING, db_column='cree_par', blank=True, null=True)
    date_creation = models.DateTimeField(blank=True, null=True)
    date_modification = models.DateTimeField(blank=True, null=True)
    date_suppression = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'commandes'
        unique_together = (('organisation', 'numero_commande'),)


class CommandesMarketplace(models.Model):
    id = models.UUIDField(primary_key=True)
    commande = models.ForeignKey(Commandes, models.DO_NOTHING)
    organisation = models.ForeignKey('Organisations', models.DO_NOTHING)
    email_client = models.TextField()
    nom_client = models.TextField()
    telephone_client = models.TextField()
    adresse_livraison = models.JSONField()
    instructions_livraison = models.TextField(blank=True, null=True)
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    user_agent = models.TextField(blank=True, null=True)
    email_envoye = models.BooleanField(blank=True, null=True)
    sms_envoye = models.BooleanField(blank=True, null=True)
    date_creation = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'commandes_marketplace'


class ConfigMarketplace(models.Model):
    organisation = models.OneToOneField('Organisations', models.DO_NOTHING, primary_key=True)
    theme_couleur = models.CharField(max_length=7, blank=True, null=True)
    logo_boutique_url = models.TextField(blank=True, null=True)
    banniere_accueil_url = models.TextField(blank=True, null=True)
    favicon_url = models.TextField(blank=True, null=True)
    slogan = models.TextField(blank=True, null=True)
    description_courte = models.TextField(blank=True, null=True)
    description_longue = models.TextField(blank=True, null=True)
    email_boutique = models.TextField(blank=True, null=True)
    telephone_boutique = models.TextField(blank=True, null=True)
    whatsapp = models.TextField(blank=True, null=True)
    facebook_url = models.TextField(blank=True, null=True)
    instagram_url = models.TextField(blank=True, null=True)
    twitter_url = models.TextField(blank=True, null=True)
    livraison_activee = models.BooleanField(blank=True, null=True)
    frais_livraison_fixes = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    livraison_gratuite_seuil = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    zones_livraison = models.JSONField(blank=True, null=True)
    paiement_en_ligne = models.BooleanField(blank=True, null=True)
    paiement_livraison = models.BooleanField(blank=True, null=True)
    avis_clients_actifs = models.BooleanField(blank=True, null=True)
    notation_activee = models.BooleanField(blank=True, null=True)
    stock_visible = models.BooleanField(blank=True, null=True)
    meta_titre = models.TextField(blank=True, null=True)
    meta_description = models.TextField(blank=True, null=True)
    meta_keywords = models.TextField(blank=True, null=True)  # This field type is a guess.
    google_analytics_id = models.TextField(blank=True, null=True)
    facebook_pixel_id = models.TextField(blank=True, null=True)
    boutique_active = models.BooleanField(blank=True, null=True)
    mode_maintenance = models.BooleanField(blank=True, null=True)
    message_maintenance = models.TextField(blank=True, null=True)
    date_modification = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'config_marketplace'
        db_table_comment = 'Configuration de la boutique en ligne par organisation'


class DemandesAchat(models.Model):
    id = models.UUIDField(primary_key=True)
    organisation = models.ForeignKey('Organisations', models.DO_NOTHING)
    numero_demande = models.CharField(max_length=50)
    demandeur = models.ForeignKey('Employes', models.DO_NOTHING)
    departement = models.CharField(max_length=100, blank=True, null=True)
    date_demande = models.DateField()
    date_besoin = models.DateField(blank=True, null=True)
    statut = models.CharField(max_length=50, blank=True, null=True)
    motif = models.TextField(blank=True, null=True)
    justification = models.TextField(blank=True, null=True)
    montant_estime = models.DecimalField(max_digits=14, decimal_places=2, blank=True, null=True)
    approuve_par = models.ForeignKey('Utilisateurs', models.DO_NOTHING, db_column='approuve_par', blank=True, null=True)
    date_approbation = models.DateTimeField(blank=True, null=True)
    commentaire_approbation = models.TextField(blank=True, null=True)
    bon_commande_id = models.UUIDField(blank=True, null=True)
    cree_par = models.ForeignKey('Utilisateurs', models.DO_NOTHING, db_column='cree_par', related_name='demandesachat_cree_par_set', blank=True, null=True)
    date_creation = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'demandes_achat'
        unique_together = (('organisation', 'numero_demande'),)


class DetailsTransactionsCaisse(models.Model):
    id = models.UUIDField(primary_key=True)
    transaction_caisse = models.ForeignKey('TransactionsCaisse', models.DO_NOTHING)
    produit = models.ForeignKey('Produits', models.DO_NOTHING, blank=True, null=True)
    variante = models.ForeignKey('VariantesProduits', models.DO_NOTHING, blank=True, null=True)
    designation = models.TextField()
    quantite = models.DecimalField(max_digits=10, decimal_places=3)
    prix_unitaire = models.DecimalField(max_digits=14, decimal_places=2)
    montant_total = models.DecimalField(max_digits=14, decimal_places=2)
    ordre_affichage = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'details_transactions_caisse'


class Devis(models.Model):
    id = models.UUIDField(primary_key=True)
    organisation = models.ForeignKey('Organisations', models.DO_NOTHING)
    numero_devis = models.CharField(max_length=50)
    reference_client = models.TextField(blank=True, null=True)
    client = models.ForeignKey(Clients, models.DO_NOTHING, blank=True, null=True)
    employe = models.ForeignKey('Employes', models.DO_NOTHING, blank=True, null=True)
    date_devis = models.DateField()
    date_validite = models.DateField()
    statut = models.CharField(max_length=50, blank=True, null=True)
    montant_ht = models.DecimalField(max_digits=14, decimal_places=2, blank=True, null=True)
    montant_tva = models.DecimalField(max_digits=14, decimal_places=2, blank=True, null=True)
    montant_ttc = models.DecimalField(max_digits=14, decimal_places=2, blank=True, null=True)
    remise_globale = models.DecimalField(max_digits=14, decimal_places=2, blank=True, null=True)
    remise_globale_pct = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    conditions_paiement = models.TextField(blank=True, null=True)
    delai_livraison = models.TextField(blank=True, null=True)
    validite_jours = models.IntegerField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    notes_internes = models.TextField(blank=True, null=True)
    converti_en_commande = models.BooleanField(blank=True, null=True)
    commande_id = models.UUIDField(blank=True, null=True)
    date_conversion = models.DateTimeField(blank=True, null=True)
    cree_par = models.ForeignKey('Utilisateurs', models.DO_NOTHING, db_column='cree_par', blank=True, null=True)
    date_creation = models.DateTimeField(blank=True, null=True)
    date_modification = models.DateTimeField(blank=True, null=True)
    date_suppression = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'devis'
        unique_together = (('organisation', 'numero_devis'),)


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class EcrituresComptables(models.Model):
    id = models.UUIDField(primary_key=True)
    organisation = models.ForeignKey('Organisations', models.DO_NOTHING)
    journal = models.ForeignKey('JournauxComptables', models.DO_NOTHING)
    numero_piece = models.CharField(max_length=50)
    date_ecriture = models.DateField()
    date_valeur = models.DateField(blank=True, null=True)
    libelle = models.TextField()
    document_type = models.CharField(max_length=50, blank=True, null=True)
    document_id = models.UUIDField(blank=True, null=True)
    statut = models.CharField(max_length=50, blank=True, null=True)
    saisie_par = models.ForeignKey('Utilisateurs', models.DO_NOTHING, db_column='saisie_par', blank=True, null=True)
    date_saisie = models.DateTimeField(blank=True, null=True)
    valide_par = models.ForeignKey('Utilisateurs', models.DO_NOTHING, db_column='valide_par', related_name='ecriturescomptables_valide_par_set', blank=True, null=True)
    date_validation = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ecritures_comptables'
        unique_together = (('organisation', 'journal', 'numero_piece'),)


class Employes(models.Model):
    id = models.UUIDField(primary_key=True)
    organisation = models.ForeignKey('Organisations', models.DO_NOTHING)
    code_employe = models.CharField(max_length=50, db_comment="Identifiant unique préfixé par l'acronyme de l'organisation")
    nom = models.TextField()
    prenom = models.TextField()
    nom_complet = models.TextField(blank=True, null=True)
    email = models.TextField(blank=True, null=True)
    telephone = models.TextField(blank=True, null=True)
    date_naissance = models.DateField(blank=True, null=True)
    lieu_naissance = models.TextField(blank=True, null=True)
    sexe = models.CharField(max_length=1, blank=True, null=True)
    numero_piece_identite = models.TextField(blank=True, null=True)
    type_piece_identite = models.CharField(max_length=50, blank=True, null=True)
    adresse_ligne1 = models.TextField(blank=True, null=True)
    adresse_ligne2 = models.TextField(blank=True, null=True)
    ville = models.CharField(max_length=100, blank=True, null=True)
    code_postal = models.CharField(max_length=20, blank=True, null=True)
    poste = models.CharField(max_length=100, blank=True, null=True)
    departement = models.CharField(max_length=100, blank=True, null=True)
    type_contrat = models.CharField(max_length=50, blank=True, null=True)
    date_embauche = models.DateField(blank=True, null=True)
    date_fin_contrat = models.DateField(blank=True, null=True)
    utilisateur = models.ForeignKey('Utilisateurs', models.DO_NOTHING, blank=True, null=True)
    acces_caisse = models.BooleanField(blank=True, null=True)
    acces_stock = models.BooleanField(blank=True, null=True)
    acces_ventes = models.BooleanField(blank=True, null=True)
    acces_rapports = models.BooleanField(blank=True, null=True)
    code_pin = models.CharField(max_length=6, blank=True, null=True)
    salaire_base = models.DecimalField(max_digits=14, decimal_places=2, blank=True, null=True)
    devise_salaire = models.CharField(max_length=5, blank=True, null=True)
    photo_url = models.TextField(blank=True, null=True)
    documents = models.JSONField(blank=True, null=True)
    statut = models.CharField(max_length=50, blank=True, null=True)
    actif = models.BooleanField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    cree_par = models.ForeignKey('Utilisateurs', models.DO_NOTHING, db_column='cree_par', related_name='employes_cree_par_set', blank=True, null=True)
    date_creation = models.DateTimeField(blank=True, null=True)
    date_modification = models.DateTimeField(blank=True, null=True)
    date_suppression = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'employes'
        unique_together = (('organisation', 'code_employe'),)
        db_table_comment = 'Employés des organisations avec codes préfixés (ex: ACME-EMP-0001)'


class EmployesRoles(models.Model):
    employe = models.OneToOneField(Employes, models.DO_NOTHING, primary_key=True)  # The composite primary key (employe_id, role_id) found, that is not supported. The first column is selected.
    role = models.ForeignKey('Roles', models.DO_NOTHING)
    date_attribution = models.DateTimeField(blank=True, null=True)
    attribue_par = models.ForeignKey('Utilisateurs', models.DO_NOTHING, db_column='attribue_par', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'employes_roles'
        unique_together = (('employe', 'role'),)


class Entrepots(models.Model):
    id = models.UUIDField(primary_key=True)
    organisation = models.ForeignKey('Organisations', models.DO_NOTHING)
    code_entrepot = models.CharField(max_length=50)
    nom = models.CharField(max_length=200)
    type = models.CharField(max_length=50, blank=True, null=True)
    adresse_ligne1 = models.TextField(blank=True, null=True)
    adresse_ligne2 = models.TextField(blank=True, null=True)
    ville = models.CharField(max_length=100, blank=True, null=True)
    code_postal = models.CharField(max_length=20, blank=True, null=True)
    responsable = models.ForeignKey(Employes, models.DO_NOTHING, blank=True, null=True)
    telephone = models.TextField(blank=True, null=True)
    superficie_m2 = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    capacite_stockage = models.TextField(blank=True, null=True)
    actif = models.BooleanField(blank=True, null=True)
    date_creation = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'entrepots'
        unique_together = (('organisation', 'code_entrepot'),)


class Factures(models.Model):
    id = models.UUIDField(primary_key=True)
    organisation = models.ForeignKey('Organisations', models.DO_NOTHING)
    numero_facture = models.CharField(max_length=50)
    numero_facture_complet = models.CharField(max_length=100, blank=True, null=True)
    type_facture = models.CharField(max_length=50, blank=True, null=True)
    client = models.ForeignKey(Clients, models.DO_NOTHING, blank=True, null=True)
    commande = models.ForeignKey(Commandes, models.DO_NOTHING, blank=True, null=True)
    date_facture = models.DateField()
    date_echeance = models.DateField()
    date_paiement = models.DateField(blank=True, null=True)
    statut = models.CharField(max_length=50, blank=True, null=True)
    montant_ht = models.DecimalField(max_digits=14, decimal_places=2, blank=True, null=True)
    montant_tva = models.DecimalField(max_digits=14, decimal_places=2, blank=True, null=True)
    montant_ttc = models.DecimalField(max_digits=14, decimal_places=2, blank=True, null=True)
    remise_globale = models.DecimalField(max_digits=14, decimal_places=2, blank=True, null=True)
    montant_paye = models.DecimalField(max_digits=14, decimal_places=2, blank=True, null=True)
    montant_restant = models.DecimalField(max_digits=14, decimal_places=2, blank=True, null=True)
    conditions_paiement = models.TextField(blank=True, null=True)
    facture_origine = models.ForeignKey('self', models.DO_NOTHING, blank=True, null=True)
    motif_avoir = models.TextField(blank=True, null=True)
    fichier_pdf_url = models.TextField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    mentions_legales = models.TextField(blank=True, null=True)
    cree_par = models.ForeignKey('Utilisateurs', models.DO_NOTHING, db_column='cree_par', blank=True, null=True)
    date_creation = models.DateTimeField(blank=True, null=True)
    date_modification = models.DateTimeField(blank=True, null=True)
    date_envoi = models.DateTimeField(blank=True, null=True)
    date_suppression = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'factures'
        unique_together = (('organisation', 'numero_facture'),)
        db_table_comment = 'Factures de vente avec numérotation automatique'


class FacturesFournisseurs(models.Model):
    id = models.UUIDField(primary_key=True)
    organisation = models.ForeignKey('Organisations', models.DO_NOTHING)
    numero_facture_fournisseur = models.CharField(max_length=100)
    numero_facture_interne = models.CharField(max_length=50, blank=True, null=True)
    fournisseur = models.ForeignKey('Fournisseurs', models.DO_NOTHING)
    bon_commande = models.ForeignKey(BonsCommande, models.DO_NOTHING, blank=True, null=True)
    date_facture = models.DateField()
    date_echeance = models.DateField()
    date_paiement = models.DateField(blank=True, null=True)
    statut = models.CharField(max_length=50, blank=True, null=True)
    montant_ht = models.DecimalField(max_digits=14, decimal_places=2)
    montant_tva = models.DecimalField(max_digits=14, decimal_places=2)
    montant_ttc = models.DecimalField(max_digits=14, decimal_places=2)
    montant_paye = models.DecimalField(max_digits=14, decimal_places=2, blank=True, null=True)
    montant_restant = models.DecimalField(max_digits=14, decimal_places=2, blank=True, null=True)
    fichier_pdf_url = models.TextField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    enregistre_par = models.ForeignKey('Utilisateurs', models.DO_NOTHING, db_column='enregistre_par', blank=True, null=True)
    valide_par = models.ForeignKey('Utilisateurs', models.DO_NOTHING, db_column='valide_par', related_name='facturesfournisseurs_valide_par_set', blank=True, null=True)
    date_validation = models.DateTimeField(blank=True, null=True)
    date_creation = models.DateTimeField(blank=True, null=True)
    date_modification = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'factures_fournisseurs'
        unique_together = (('organisation', 'numero_facture_fournisseur'),)


class Favoris(models.Model):
    id = models.UUIDField(primary_key=True)
    client = models.ForeignKey(Clients, models.DO_NOTHING)
    produit = models.ForeignKey('Produits', models.DO_NOTHING)
    date_ajout = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'favoris'
        unique_together = (('client', 'produit'),)


class Fournisseurs(models.Model):
    id = models.UUIDField(primary_key=True)
    organisation = models.ForeignKey('Organisations', models.DO_NOTHING)
    code_fournisseur = models.CharField(max_length=50)
    raison_sociale = models.TextField()
    nom_commercial = models.TextField(blank=True, null=True)
    numero_identification = models.TextField(blank=True, null=True)
    numero_tva = models.TextField(blank=True, null=True)
    email = models.TextField(blank=True, null=True)
    telephone_principal = models.TextField(blank=True, null=True)
    telephone_secondaire = models.TextField(blank=True, null=True)
    site_web = models.TextField(blank=True, null=True)
    personne_contact = models.TextField(blank=True, null=True)
    adresse = models.JSONField(blank=True, null=True)
    delai_livraison_jours = models.IntegerField(blank=True, null=True)
    conditions_paiement = models.CharField(max_length=100, blank=True, null=True)
    devise = models.CharField(max_length=5, blank=True, null=True)
    note_qualite = models.DecimalField(max_digits=3, decimal_places=2, blank=True, null=True)
    note_delais = models.DecimalField(max_digits=3, decimal_places=2, blank=True, null=True)
    note_prix = models.DecimalField(max_digits=3, decimal_places=2, blank=True, null=True)
    nombre_commandes = models.IntegerField(blank=True, null=True)
    montant_total_achats = models.DecimalField(max_digits=14, decimal_places=2, blank=True, null=True)
    derniere_commande = models.DateTimeField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    actif = models.BooleanField(blank=True, null=True)
    cree_par = models.ForeignKey('Utilisateurs', models.DO_NOTHING, db_column='cree_par', blank=True, null=True)
    date_creation = models.DateTimeField(blank=True, null=True)
    date_modification = models.DateTimeField(blank=True, null=True)
    date_suppression = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'fournisseurs'
        unique_together = (('organisation', 'code_fournisseur'),)


class Integrations(models.Model):
    id = models.UUIDField(primary_key=True)
    nom = models.CharField(max_length=100)
    slug = models.CharField(unique=True, max_length=50)
    description = models.TextField()
    description_courte = models.CharField(max_length=200)
    icone = models.CharField(max_length=50)
    couleur = models.CharField(max_length=20)
    image = models.CharField(max_length=200, blank=True, null=True)
    types_entreprise = models.JSONField()
    actif_par_defaut = models.BooleanField()
    gratuit = models.BooleanField()
    prix_mensuel = models.DecimalField(max_digits=10, decimal_places=2)
    fonctionnalites = models.JSONField()
    necessite_configuration = models.BooleanField()
    documentation_url = models.CharField(max_length=200)
    video_demo_url = models.CharField(max_length=200)
    ordre = models.IntegerField()
    populaire = models.BooleanField()
    nouveau = models.BooleanField()
    date_creation = models.DateTimeField()
    date_modification = models.DateTimeField()
    categorie = models.ForeignKey(CategoriesIntegration, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'integrations'


class IntegrationsUtilisateur(models.Model):
    id = models.UUIDField(primary_key=True)
    actif = models.BooleanField()
    configuration = models.JSONField()
    api_key = models.CharField(max_length=500)
    api_secret = models.CharField(max_length=500)
    webhook_url = models.CharField(max_length=200)
    nombre_utilisations = models.IntegerField()
    derniere_utilisation = models.DateTimeField(blank=True, null=True)
    date_activation = models.DateTimeField()
    date_desactivation = models.DateTimeField(blank=True, null=True)
    date_modification = models.DateTimeField()
    integration = models.ForeignKey(Integrations, models.DO_NOTHING)
    utilisateur = models.ForeignKey('Utilisateurs', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'integrations_utilisateur'
        unique_together = (('utilisateur', 'integration'),)


class Inventaires(models.Model):
    id = models.UUIDField(primary_key=True)
    organisation = models.ForeignKey('Organisations', models.DO_NOTHING)
    entrepot = models.ForeignKey(Entrepots, models.DO_NOTHING)
    numero_inventaire = models.CharField(max_length=50)
    date_debut = models.DateField()
    date_fin = models.DateField(blank=True, null=True)
    statut = models.CharField(max_length=50, blank=True, null=True)
    responsable = models.ForeignKey(Employes, models.DO_NOTHING, blank=True, null=True)
    equipe_ids = models.TextField(blank=True, null=True)  # This field type is a guess.
    nombre_produits_comptes = models.IntegerField(blank=True, null=True)
    ecarts_positifs_valeur = models.DecimalField(max_digits=14, decimal_places=2, blank=True, null=True)
    ecarts_negatifs_valeur = models.DecimalField(max_digits=14, decimal_places=2, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    cree_par = models.ForeignKey('Utilisateurs', models.DO_NOTHING, db_column='cree_par', blank=True, null=True)
    date_creation = models.DateTimeField(blank=True, null=True)
    date_validation = models.DateTimeField(blank=True, null=True)
    valide_par = models.ForeignKey('Utilisateurs', models.DO_NOTHING, db_column='valide_par', related_name='inventaires_valide_par_set', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'inventaires'
        unique_together = (('organisation', 'numero_inventaire'),)


class JournalActivites(models.Model):
    id = models.UUIDField(primary_key=True)
    organisation = models.ForeignKey('Organisations', models.DO_NOTHING, blank=True, null=True)
    utilisateur = models.ForeignKey('Utilisateurs', models.DO_NOTHING, blank=True, null=True)
    employe = models.ForeignKey(Employes, models.DO_NOTHING, blank=True, null=True)
    action = models.CharField(max_length=100)
    entite = models.CharField(max_length=100)
    entite_id = models.UUIDField(blank=True, null=True)
    description = models.TextField()
    donnees_avant = models.JSONField(blank=True, null=True)
    donnees_apres = models.JSONField(blank=True, null=True)
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    user_agent = models.TextField(blank=True, null=True)
    date_action = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'journal_activites'


class JournauxComptables(models.Model):
    id = models.UUIDField(primary_key=True)
    organisation = models.ForeignKey('Organisations', models.DO_NOTHING)
    code_journal = models.CharField(max_length=10)
    libelle = models.CharField(max_length=100)
    type_journal = models.CharField(max_length=50)
    actif = models.BooleanField(blank=True, null=True)
    date_creation = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'journaux_comptables'
        unique_together = (('organisation', 'code_journal'),)


class LignesBonsCommande(models.Model):
    id = models.UUIDField(primary_key=True)
    bon_commande = models.ForeignKey(BonsCommande, models.DO_NOTHING)
    produit = models.ForeignKey('Produits', models.DO_NOTHING, blank=True, null=True)
    variante = models.ForeignKey('VariantesProduits', models.DO_NOTHING, blank=True, null=True)
    designation = models.TextField()
    description = models.TextField(blank=True, null=True)
    quantite_commandee = models.DecimalField(max_digits=10, decimal_places=3)
    quantite_recue = models.DecimalField(max_digits=10, decimal_places=3, blank=True, null=True)
    quantite_restante = models.DecimalField(max_digits=10, decimal_places=3, blank=True, null=True)
    prix_unitaire_ht = models.DecimalField(max_digits=14, decimal_places=2)
    taux_tva = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    montant_ht = models.DecimalField(max_digits=14, decimal_places=2, blank=True, null=True)
    montant_tva = models.DecimalField(max_digits=14, decimal_places=2, blank=True, null=True)
    montant_ttc = models.DecimalField(max_digits=14, decimal_places=2, blank=True, null=True)
    ordre_affichage = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'lignes_bons_commande'


class LignesCommandes(models.Model):
    id = models.UUIDField(primary_key=True)
    commande = models.ForeignKey(Commandes, models.DO_NOTHING)
    produit = models.ForeignKey('Produits', models.DO_NOTHING, blank=True, null=True)
    variante = models.ForeignKey('VariantesProduits', models.DO_NOTHING, blank=True, null=True)
    designation = models.TextField()
    description = models.TextField(blank=True, null=True)
    quantite = models.DecimalField(max_digits=10, decimal_places=3)
    quantite_livree = models.DecimalField(max_digits=10, decimal_places=3, blank=True, null=True)
    prix_unitaire_ht = models.DecimalField(max_digits=14, decimal_places=2)
    taux_tva = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    remise_pct = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    remise_montant = models.DecimalField(max_digits=14, decimal_places=2, blank=True, null=True)
    montant_ht = models.DecimalField(max_digits=14, decimal_places=2, blank=True, null=True)
    montant_tva = models.DecimalField(max_digits=14, decimal_places=2, blank=True, null=True)
    montant_ttc = models.DecimalField(max_digits=14, decimal_places=2, blank=True, null=True)
    stock_reserve = models.BooleanField(blank=True, null=True)
    entrepot = models.ForeignKey(Entrepots, models.DO_NOTHING, blank=True, null=True)
    ordre_affichage = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'lignes_commandes'


class LignesDemandesAchat(models.Model):
    id = models.UUIDField(primary_key=True)
    demande_achat = models.ForeignKey(DemandesAchat, models.DO_NOTHING)
    produit = models.ForeignKey('Produits', models.DO_NOTHING, blank=True, null=True)
    designation = models.TextField()
    quantite = models.DecimalField(max_digits=10, decimal_places=3)
    prix_unitaire_estime = models.DecimalField(max_digits=14, decimal_places=2, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'lignes_demandes_achat'


class LignesDevis(models.Model):
    id = models.UUIDField(primary_key=True)
    devis = models.ForeignKey(Devis, models.DO_NOTHING)
    produit = models.ForeignKey('Produits', models.DO_NOTHING, blank=True, null=True)
    variante = models.ForeignKey('VariantesProduits', models.DO_NOTHING, blank=True, null=True)
    designation = models.TextField()
    description = models.TextField(blank=True, null=True)
    quantite = models.DecimalField(max_digits=10, decimal_places=3)
    prix_unitaire_ht = models.DecimalField(max_digits=14, decimal_places=2)
    taux_tva = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    remise_pct = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    remise_montant = models.DecimalField(max_digits=14, decimal_places=2, blank=True, null=True)
    montant_ht = models.DecimalField(max_digits=14, decimal_places=2, blank=True, null=True)
    montant_tva = models.DecimalField(max_digits=14, decimal_places=2, blank=True, null=True)
    montant_ttc = models.DecimalField(max_digits=14, decimal_places=2, blank=True, null=True)
    ordre_affichage = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'lignes_devis'


class LignesEcritures(models.Model):
    id = models.UUIDField(primary_key=True)
    ecriture = models.ForeignKey(EcrituresComptables, models.DO_NOTHING)
    compte = models.ForeignKey('PlanComptable', models.DO_NOTHING)
    libelle = models.TextField(blank=True, null=True)
    montant_debit = models.DecimalField(max_digits=14, decimal_places=2, blank=True, null=True)
    montant_credit = models.DecimalField(max_digits=14, decimal_places=2, blank=True, null=True)
    lettre = models.BooleanField(blank=True, null=True)
    code_lettrage = models.CharField(max_length=10, blank=True, null=True)
    date_lettrage = models.DateField(blank=True, null=True)
    ordre_affichage = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'lignes_ecritures'


class LignesFactures(models.Model):
    id = models.UUIDField(primary_key=True)
    facture = models.ForeignKey(Factures, models.DO_NOTHING)
    produit = models.ForeignKey('Produits', models.DO_NOTHING, blank=True, null=True)
    variante = models.ForeignKey('VariantesProduits', models.DO_NOTHING, blank=True, null=True)
    designation = models.TextField()
    description = models.TextField(blank=True, null=True)
    quantite = models.DecimalField(max_digits=10, decimal_places=3)
    prix_unitaire_ht = models.DecimalField(max_digits=14, decimal_places=2)
    taux_tva = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    remise_pct = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    remise_montant = models.DecimalField(max_digits=14, decimal_places=2, blank=True, null=True)
    montant_ht = models.DecimalField(max_digits=14, decimal_places=2, blank=True, null=True)
    montant_tva = models.DecimalField(max_digits=14, decimal_places=2, blank=True, null=True)
    montant_ttc = models.DecimalField(max_digits=14, decimal_places=2, blank=True, null=True)
    ordre_affichage = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'lignes_factures'


class LignesInventaire(models.Model):
    id = models.UUIDField(primary_key=True)
    inventaire = models.ForeignKey(Inventaires, models.DO_NOTHING)
    stock = models.ForeignKey('Stocks', models.DO_NOTHING)
    quantite_theorique = models.DecimalField(max_digits=12, decimal_places=3, blank=True, null=True)
    quantite_comptee = models.DecimalField(max_digits=12, decimal_places=3, blank=True, null=True)
    ecart = models.DecimalField(max_digits=12, decimal_places=3, blank=True, null=True)
    valeur_ecart = models.DecimalField(max_digits=14, decimal_places=2, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    compte_par = models.ForeignKey(Employes, models.DO_NOTHING, db_column='compte_par', blank=True, null=True)
    date_comptage = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'lignes_inventaire'


class LignesReceptions(models.Model):
    id = models.UUIDField(primary_key=True)
    reception = models.ForeignKey('ReceptionsMarchandises', models.DO_NOTHING)
    ligne_bon_commande = models.ForeignKey(LignesBonsCommande, models.DO_NOTHING, blank=True, null=True)
    produit = models.ForeignKey('Produits', models.DO_NOTHING, blank=True, null=True)
    variante = models.ForeignKey('VariantesProduits', models.DO_NOTHING, blank=True, null=True)
    designation = models.TextField()
    quantite_commandee = models.DecimalField(max_digits=10, decimal_places=3, blank=True, null=True)
    quantite_recue = models.DecimalField(max_digits=10, decimal_places=3)
    quantite_acceptee = models.DecimalField(max_digits=10, decimal_places=3, blank=True, null=True)
    quantite_rejetee = models.DecimalField(max_digits=10, decimal_places=3, blank=True, null=True)
    motif_rejet = models.TextField(blank=True, null=True)
    numero_lot = models.TextField(blank=True, null=True)
    date_peremption = models.DateField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'lignes_receptions'


class Marques(models.Model):
    id = models.UUIDField(primary_key=True)
    organisation = models.ForeignKey('Organisations', models.DO_NOTHING)
    nom = models.CharField(max_length=100)
    code = models.CharField(max_length=50, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    logo_url = models.TextField(blank=True, null=True)
    site_web = models.TextField(blank=True, null=True)
    actif = models.BooleanField(blank=True, null=True)
    date_creation = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'marques'
        unique_together = (('organisation', 'code'),)


class ModesPaiement(models.Model):
    id = models.UUIDField(primary_key=True)
    organisation = models.ForeignKey('Organisations', models.DO_NOTHING, blank=True, null=True)
    nom = models.CharField(max_length=100)
    code = models.CharField(max_length=50)
    type = models.CharField(max_length=50)
    compte_comptable_id = models.UUIDField(blank=True, null=True)
    commission_pct = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    frais_fixes = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    operateur = models.CharField(max_length=50, blank=True, null=True)
    numero_compte = models.TextField(blank=True, null=True)
    terminal_id = models.TextField(blank=True, null=True)
    actif = models.BooleanField(blank=True, null=True)
    ordre_affichage = models.IntegerField(blank=True, null=True)
    date_creation = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'modes_paiement'


class MouvementsStock(models.Model):
    id = models.UUIDField(primary_key=True)
    organisation = models.ForeignKey('Organisations', models.DO_NOTHING)
    stock = models.ForeignKey('Stocks', models.DO_NOTHING)
    entrepot_origine = models.ForeignKey(Entrepots, models.DO_NOTHING, blank=True, null=True)
    entrepot_destination = models.ForeignKey(Entrepots, models.DO_NOTHING, related_name='mouvementsstock_entrepot_destination_set', blank=True, null=True)
    type_mouvement = models.CharField(max_length=50)
    motif = models.TextField(blank=True, null=True)
    quantite = models.DecimalField(max_digits=12, decimal_places=3)
    quantite_avant = models.DecimalField(max_digits=12, decimal_places=3, blank=True, null=True)
    quantite_apres = models.DecimalField(max_digits=12, decimal_places=3, blank=True, null=True)
    cout_unitaire = models.DecimalField(max_digits=14, decimal_places=2, blank=True, null=True)
    valeur_totale = models.DecimalField(max_digits=14, decimal_places=2, blank=True, null=True)
    document_type = models.CharField(max_length=50, blank=True, null=True)
    document_id = models.UUIDField(blank=True, null=True)
    numero_document = models.TextField(blank=True, null=True)
    numero_lot = models.TextField(blank=True, null=True)
    date_peremption = models.DateField(blank=True, null=True)
    numero_serie = models.TextField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    effectue_par = models.ForeignKey('Utilisateurs', models.DO_NOTHING, db_column='effectue_par', blank=True, null=True)
    date_mouvement = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'mouvements_stock'


class Notifications(models.Model):
    id = models.UUIDField(primary_key=True)
    organisation = models.ForeignKey('Organisations', models.DO_NOTHING)
    type_notification = models.ForeignKey('TypesNotifications', models.DO_NOTHING, blank=True, null=True)
    destinataire = models.ForeignKey('Utilisateurs', models.DO_NOTHING, blank=True, null=True)
    destinataire_email = models.TextField(blank=True, null=True)
    destinataire_telephone = models.TextField(blank=True, null=True)
    titre = models.TextField()
    message = models.TextField()
    canal = models.CharField(max_length=50)
    lien_action = models.TextField(blank=True, null=True)
    donnees_json = models.JSONField(blank=True, null=True)
    statut = models.CharField(max_length=50, blank=True, null=True)
    date_envoi = models.DateTimeField(blank=True, null=True)
    date_lecture = models.DateTimeField(blank=True, null=True)
    erreur_message = models.TextField(blank=True, null=True)
    date_creation = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'notifications'


class Organisations(models.Model):
    id = models.UUIDField(primary_key=True)
    proprietaire = models.ForeignKey('Utilisateurs', models.DO_NOTHING)
    nom_commercial = models.TextField()
    raison_sociale = models.TextField(blank=True, null=True)
    acronyme = models.CharField(max_length=10, db_comment='Utilisé pour préfixer les identifiants des sous-comptes (ex: ACME-001)')
    sigle = models.CharField(max_length=20, blank=True, null=True)
    numero_identification = models.TextField(blank=True, null=True)
    numero_tva = models.TextField(blank=True, null=True)
    code_naf = models.CharField(max_length=10, blank=True, null=True)
    forme_juridique = models.CharField(max_length=100, blank=True, null=True)
    adresse_ligne1 = models.TextField(blank=True, null=True)
    adresse_ligne2 = models.TextField(blank=True, null=True)
    ville = models.CharField(max_length=100, blank=True, null=True)
    code_postal = models.CharField(blank=True, null=True)
    region = models.CharField(max_length=100, blank=True, null=True)
    pays = models.ForeignKey('Pays', models.DO_NOTHING, db_column='pays', blank=True, null=True)
    email_contact = models.TextField(blank=True, null=True)
    telephone_principal = models.TextField(blank=True, null=True)
    telephone_secondaire = models.TextField(blank=True, null=True)
    site_web = models.TextField(blank=True, null=True)
    devise = models.CharField(max_length=5, blank=True, null=True)
    fuseau_horaire = models.CharField(max_length=50, blank=True, null=True)
    langue_defaut = models.CharField(max_length=5, blank=True, null=True)
    plan = models.ForeignKey('PlansAbonnement', models.DO_NOTHING, blank=True, null=True)
    statut_abonnement = models.CharField(max_length=50, blank=True, null=True)
    date_debut_abonnement = models.DateField(blank=True, null=True)
    date_fin_abonnement = models.DateField(blank=True, null=True)
    date_fin_essai = models.DateField(blank=True, null=True)
    logo_url = models.TextField(blank=True, null=True)
    couleur_principale = models.CharField(max_length=7, blank=True, null=True)
    couleur_secondaire = models.CharField(max_length=7, blank=True, null=True)
    marketplace_actif = models.BooleanField(blank=True, null=True)
    marketplace_slug = models.CharField(unique=True, max_length=100, blank=True, null=True, db_comment="URL unique pour la boutique en ligne de l'entreprise")
    marketplace_description = models.TextField(blank=True, null=True)
    marketplace_banniere_url = models.TextField(blank=True, null=True)
    parametres_facturation = models.JSONField(blank=True, null=True)
    parametres_caisse = models.JSONField(blank=True, null=True)
    parametres_stock = models.JSONField(blank=True, null=True)
    parametres_comptabilite = models.JSONField(blank=True, null=True)
    actif = models.BooleanField(blank=True, null=True)
    verifie = models.BooleanField(blank=True, null=True)
    date_verification = models.DateTimeField(blank=True, null=True)
    date_creation = models.DateTimeField(blank=True, null=True)
    date_modification = models.DateTimeField(blank=True, null=True)
    date_suppression = models.DateTimeField(blank=True, null=True)
    type_organisation = models.ForeignKey('TypeOrganisations', models.DO_NOTHING, db_column='type_organisation', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'organisations'
        db_table_comment = 'Entreprises clientes du SaaS, chacune isolée par organisation_id'


class Paiements(models.Model):
    id = models.UUIDField(primary_key=True)
    organisation = models.ForeignKey(Organisations, models.DO_NOTHING)
    numero_paiement = models.CharField(max_length=50)
    facture = models.ForeignKey(Factures, models.DO_NOTHING, blank=True, null=True)
    commande = models.ForeignKey(Commandes, models.DO_NOTHING, blank=True, null=True)
    client = models.ForeignKey(Clients, models.DO_NOTHING, blank=True, null=True)
    mode_paiement = models.ForeignKey(ModesPaiement, models.DO_NOTHING)
    montant = models.DecimalField(max_digits=14, decimal_places=2)
    devise = models.CharField(max_length=5, blank=True, null=True)
    date_paiement = models.DateField()
    date_valeur = models.DateField(blank=True, null=True)
    statut = models.CharField(max_length=50, blank=True, null=True)
    reference_transaction = models.TextField(blank=True, null=True)
    reference_interne = models.TextField(blank=True, null=True)
    numero_cheque = models.TextField(blank=True, null=True)
    numero_autorisation = models.TextField(blank=True, null=True)
    banque = models.TextField(blank=True, null=True)
    numero_compte = models.TextField(blank=True, null=True)
    frais_transaction = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    montant_net = models.DecimalField(max_digits=14, decimal_places=2, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    caisse_session_id = models.UUIDField(blank=True, null=True)
    enregistre_par = models.ForeignKey('Utilisateurs', models.DO_NOTHING, db_column='enregistre_par', blank=True, null=True)
    date_creation = models.DateTimeField(blank=True, null=True)
    date_validation = models.DateTimeField(blank=True, null=True)
    valide_par = models.ForeignKey('Utilisateurs', models.DO_NOTHING, db_column='valide_par', related_name='paiements_valide_par_set', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'paiements'
        unique_together = (('organisation', 'numero_paiement'),)


class PaiementsFournisseurs(models.Model):
    id = models.UUIDField(primary_key=True)
    organisation = models.ForeignKey(Organisations, models.DO_NOTHING)
    numero_paiement = models.CharField(max_length=50)
    fournisseur = models.ForeignKey(Fournisseurs, models.DO_NOTHING)
    facture_fournisseur = models.ForeignKey(FacturesFournisseurs, models.DO_NOTHING, blank=True, null=True)
    mode_paiement = models.ForeignKey(ModesPaiement, models.DO_NOTHING)
    montant = models.DecimalField(max_digits=14, decimal_places=2)
    date_paiement = models.DateField()
    date_valeur = models.DateField(blank=True, null=True)
    statut = models.CharField(max_length=50, blank=True, null=True)
    reference_transaction = models.TextField(blank=True, null=True)
    numero_cheque = models.TextField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    effectue_par = models.ForeignKey('Utilisateurs', models.DO_NOTHING, db_column='effectue_par', blank=True, null=True)
    date_creation = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'paiements_fournisseurs'
        unique_together = (('organisation', 'numero_paiement'),)


class PaniersAbandonnes(models.Model):
    id = models.UUIDField(primary_key=True)
    organisation = models.ForeignKey(Organisations, models.DO_NOTHING)
    client = models.ForeignKey(Clients, models.DO_NOTHING, blank=True, null=True)
    email_visiteur = models.TextField(blank=True, null=True)
    contenu = models.JSONField()
    montant_total = models.DecimalField(max_digits=14, decimal_places=2, blank=True, null=True)
    session_id = models.TextField(blank=True, null=True)
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    email_relance_envoye = models.BooleanField(blank=True, null=True)
    date_relance = models.DateTimeField(blank=True, null=True)
    converti = models.BooleanField(blank=True, null=True)
    commande = models.ForeignKey(Commandes, models.DO_NOTHING, blank=True, null=True)
    date_creation = models.DateTimeField(blank=True, null=True)
    date_derniere_modification = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'paniers_abandonnes'


class ParametresOrganisation(models.Model):
    organisation = models.OneToOneField(Organisations, models.DO_NOTHING, primary_key=True)
    mentions_legales_facture = models.TextField(blank=True, null=True)
    conditions_generales_vente = models.TextField(blank=True, null=True)
    pied_page_facture = models.TextField(blank=True, null=True)
    logo_facture_url = models.TextField(blank=True, null=True)
    format_facture = models.CharField(max_length=20, blank=True, null=True)
    delai_paiement_defaut_jours = models.IntegerField(blank=True, null=True)
    relances_actives = models.BooleanField(blank=True, null=True)
    relance_1_jours = models.IntegerField(blank=True, null=True)
    relance_2_jours = models.IntegerField(blank=True, null=True)
    relance_3_jours = models.IntegerField(blank=True, null=True)
    email_expediteur = models.TextField(blank=True, null=True)
    signature_email = models.TextField(blank=True, null=True)
    alerte_stock_actif = models.BooleanField(blank=True, null=True)
    gestion_lot_serie = models.BooleanField(blank=True, null=True)
    gestion_peremption = models.BooleanField(blank=True, null=True)
    impression_automatique_ticket = models.BooleanField(blank=True, null=True)
    ouverture_tiroir_auto = models.BooleanField(blank=True, null=True)
    exercice_comptable_debut = models.DateField(blank=True, null=True)
    exercice_comptable_fin = models.DateField(blank=True, null=True)
    notifications_email = models.BooleanField(blank=True, null=True)
    notifications_sms = models.BooleanField(blank=True, null=True)
    date_modification = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'parametres_organisation'


class Pays(models.Model):
    id = models.BigAutoField(primary_key=True)
    nom = models.CharField(unique=True)
    created_at = models.DateTimeField()
    indicatif = models.CharField(unique=True)
    drapeau_url = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'pays'
        db_table_comment = 'Countries of the world'


class PlanComptable(models.Model):
    id = models.UUIDField(primary_key=True)
    organisation = models.ForeignKey(Organisations, models.DO_NOTHING)
    numero_compte = models.CharField(max_length=20)
    intitule_compte = models.TextField()
    type_compte = models.CharField(max_length=50)
    compte_parent = models.ForeignKey('self', models.DO_NOTHING, blank=True, null=True)
    niveau = models.IntegerField(blank=True, null=True)
    imputable = models.BooleanField(blank=True, null=True)
    lettrable = models.BooleanField(blank=True, null=True)
    actif = models.BooleanField(blank=True, null=True)
    date_creation = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'plan_comptable'
        unique_together = (('organisation', 'numero_compte'),)


class PlansAbonnement(models.Model):
    id = models.UUIDField(primary_key=True)
    nom = models.CharField(unique=True, max_length=100)
    code = models.CharField(unique=True, max_length=50)
    description = models.TextField(blank=True, null=True)
    prix_mensuel = models.DecimalField(max_digits=12, decimal_places=2)
    prix_annuel = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    devise = models.CharField(max_length=5, blank=True, null=True)
    nombre_max_employes = models.IntegerField(blank=True, null=True)
    nombre_max_articles = models.IntegerField(blank=True, null=True)
    nombre_max_factures_mois = models.IntegerField(blank=True, null=True)
    espace_stockage_mo = models.IntegerField(blank=True, null=True)
    marketplace_actif = models.BooleanField(blank=True, null=True)
    api_acces = models.BooleanField(blank=True, null=True)
    support_niveau = models.CharField(max_length=50, blank=True, null=True)
    fonctionnalites = models.JSONField(blank=True, null=True)
    actif = models.BooleanField(blank=True, null=True)
    ordre_affichage = models.IntegerField(blank=True, null=True)
    date_creation = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'plans_abonnement'


class PreferencesNotificationsUtilisateur(models.Model):
    utilisateur = models.OneToOneField('Utilisateurs', models.DO_NOTHING, primary_key=True)  # The composite primary key (utilisateur_id, type_notification_id) found, that is not supported. The first column is selected.
    type_notification = models.ForeignKey('TypesNotifications', models.DO_NOTHING)
    email_actif = models.BooleanField(blank=True, null=True)
    sms_actif = models.BooleanField(blank=True, null=True)
    push_actif = models.BooleanField(blank=True, null=True)
    in_app_actif = models.BooleanField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'preferences_notifications_utilisateur'
        unique_together = (('utilisateur', 'type_notification'),)


class Produits(models.Model):
    id = models.UUIDField(primary_key=True)
    organisation = models.ForeignKey(Organisations, models.DO_NOTHING)
    code_produit = models.CharField(max_length=100)
    code_barre = models.CharField(max_length=100, blank=True, null=True)
    reference_fournisseur = models.TextField(blank=True, null=True)
    nom = models.TextField()
    nom_court = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    description_longue = models.TextField(blank=True, null=True)
    categorie = models.ForeignKey(CategoriesProduits, models.DO_NOTHING, blank=True, null=True)
    marque = models.ForeignKey(Marques, models.DO_NOTHING, blank=True, null=True)
    type_produit = models.CharField(max_length=50, blank=True, null=True)
    image_principale_url = models.TextField(blank=True, null=True)
    images_urls = models.TextField(blank=True, null=True)  # This field type is a guess.
    video_url = models.TextField(blank=True, null=True)
    prix_achat_ht = models.DecimalField(max_digits=14, decimal_places=2, blank=True, null=True)
    prix_vente_ht = models.DecimalField(max_digits=14, decimal_places=2)
    prix_vente_ttc = models.DecimalField(max_digits=14, decimal_places=2, blank=True, null=True)
    marge_calculee = models.DecimalField(max_digits=14, decimal_places=2, blank=True, null=True)
    taux_tva = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    unite_mesure = models.ForeignKey('UnitesMesure', models.DO_NOTHING, blank=True, null=True)
    contenance = models.DecimalField(max_digits=10, decimal_places=3, blank=True, null=True)
    gere_stock = models.BooleanField(blank=True, null=True)
    stock_alerte = models.IntegerField(blank=True, null=True)
    stock_minimum = models.IntegerField(blank=True, null=True)
    stock_maximum = models.IntegerField(blank=True, null=True)
    poids = models.DecimalField(max_digits=10, decimal_places=3, blank=True, null=True)
    longueur = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    largeur = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    hauteur = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    attributs = models.JSONField(blank=True, null=True)
    publie_marketplace = models.BooleanField(blank=True, null=True)
    meta_titre = models.TextField(blank=True, null=True)
    meta_description = models.TextField(blank=True, null=True)
    tags_marketplace = models.TextField(blank=True, null=True)  # This field type is a guess.
    actif = models.BooleanField(blank=True, null=True)
    en_vedette = models.BooleanField(blank=True, null=True)
    notes_internes = models.TextField(blank=True, null=True)
    cree_par = models.ForeignKey('Utilisateurs', models.DO_NOTHING, db_column='cree_par', blank=True, null=True)
    date_creation = models.DateTimeField(blank=True, null=True)
    date_modification = models.DateTimeField(blank=True, null=True)
    date_suppression = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'produits'
        unique_together = (('organisation', 'code_produit'),)
        db_table_comment = 'Catalogue produits avec support marketplace'


class ReceptionsMarchandises(models.Model):
    id = models.UUIDField(primary_key=True)
    organisation = models.ForeignKey(Organisations, models.DO_NOTHING)
    bon_commande = models.ForeignKey(BonsCommande, models.DO_NOTHING)
    numero_reception = models.CharField(max_length=50)
    date_reception = models.DateField()
    entrepot = models.ForeignKey(Entrepots, models.DO_NOTHING)
    numero_bl_fournisseur = models.TextField(blank=True, null=True)
    statut = models.CharField(max_length=50, blank=True, null=True)
    reception_complete = models.BooleanField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    anomalies = models.TextField(blank=True, null=True)
    receptionne_par = models.ForeignKey(Employes, models.DO_NOTHING, db_column='receptionne_par', blank=True, null=True)
    valide_par = models.ForeignKey('Utilisateurs', models.DO_NOTHING, db_column='valide_par', blank=True, null=True)
    date_validation = models.DateTimeField(blank=True, null=True)
    date_creation = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'receptions_marchandises'
        unique_together = (('organisation', 'numero_reception'),)


class Roles(models.Model):
    id = models.UUIDField(primary_key=True)
    organisation = models.ForeignKey(Organisations, models.DO_NOTHING)
    nom = models.CharField(max_length=100)
    code = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)
    systeme = models.BooleanField(blank=True, null=True)
    permissions = models.JSONField(blank=True, null=True)
    actif = models.BooleanField(blank=True, null=True)
    date_creation = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'roles'
        unique_together = (('organisation', 'code'),)


class SequencesNumerotation(models.Model):
    id = models.UUIDField(primary_key=True)
    organisation = models.ForeignKey(Organisations, models.DO_NOTHING)
    type_document = models.CharField(max_length=50)
    prefixe = models.CharField(max_length=20, blank=True, null=True)
    separateur = models.CharField(max_length=5, blank=True, null=True)
    format_numero = models.CharField(max_length=100, blank=True, null=True)
    valeur_actuelle = models.BigIntegerField(blank=True, null=True)
    increment = models.IntegerField(blank=True, null=True)
    reinitialiser_annuellement = models.BooleanField(blank=True, null=True)
    reinitialiser_mensuellement = models.BooleanField(blank=True, null=True)
    dernier_reset = models.DateTimeField(blank=True, null=True)
    actif = models.BooleanField(blank=True, null=True)
    date_creation = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sequences_numerotation'
        unique_together = (('organisation', 'type_document'),)


class SessionsCaisse(models.Model):
    id = models.UUIDField(primary_key=True)
    organisation = models.ForeignKey(Organisations, models.DO_NOTHING)
    caisse = models.ForeignKey(Caisses, models.DO_NOTHING)
    numero_session = models.CharField(max_length=50)
    caissier = models.ForeignKey(Employes, models.DO_NOTHING)
    date_ouverture = models.DateTimeField()
    date_fermeture = models.DateTimeField(blank=True, null=True)
    statut = models.CharField(max_length=50, blank=True, null=True)
    fond_caisse_ouverture = models.DecimalField(max_digits=14, decimal_places=2, blank=True, null=True)
    fond_caisse_fermeture = models.DecimalField(max_digits=14, decimal_places=2, blank=True, null=True)
    total_ventes_especes = models.DecimalField(max_digits=14, decimal_places=2, blank=True, null=True)
    total_ventes_carte = models.DecimalField(max_digits=14, decimal_places=2, blank=True, null=True)
    total_ventes_mobile = models.DecimalField(max_digits=14, decimal_places=2, blank=True, null=True)
    total_ventes_autres = models.DecimalField(max_digits=14, decimal_places=2, blank=True, null=True)
    total_ventes = models.DecimalField(max_digits=14, decimal_places=2, blank=True, null=True)
    total_entrees_especes = models.DecimalField(max_digits=14, decimal_places=2, blank=True, null=True)
    total_sorties_especes = models.DecimalField(max_digits=14, decimal_places=2, blank=True, null=True)
    montant_theorique_especes = models.DecimalField(max_digits=14, decimal_places=2, blank=True, null=True)
    montant_reel_especes = models.DecimalField(max_digits=14, decimal_places=2, blank=True, null=True)
    montant_reel_carte = models.DecimalField(max_digits=14, decimal_places=2, blank=True, null=True)
    montant_reel_mobile = models.DecimalField(max_digits=14, decimal_places=2, blank=True, null=True)
    ecart_especes = models.DecimalField(max_digits=14, decimal_places=2, blank=True, null=True)
    ecart_explique = models.TextField(blank=True, null=True)
    nombre_ventes = models.IntegerField(blank=True, null=True)
    nombre_clients = models.IntegerField(blank=True, null=True)
    ticket_moyen = models.DecimalField(max_digits=14, decimal_places=2, blank=True, null=True)
    notes_ouverture = models.TextField(blank=True, null=True)
    notes_fermeture = models.TextField(blank=True, null=True)
    ouvert_par = models.ForeignKey('Utilisateurs', models.DO_NOTHING, db_column='ouvert_par', blank=True, null=True)
    ferme_par = models.ForeignKey('Utilisateurs', models.DO_NOTHING, db_column='ferme_par', related_name='sessionscaisse_ferme_par_set', blank=True, null=True)
    valide_par = models.ForeignKey('Utilisateurs', models.DO_NOTHING, db_column='valide_par', related_name='sessionscaisse_valide_par_set', blank=True, null=True)
    date_validation = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sessions_caisse'
        unique_together = (('organisation', 'numero_session'),)
        db_table_comment = "Sessions d'ouverture/fermeture de caisse avec rapprochement"


class SessionsUtilisateur(models.Model):
    id = models.UUIDField(primary_key=True)
    utilisateur = models.ForeignKey('Utilisateurs', models.DO_NOTHING)
    token = models.TextField()
    refresh_token = models.TextField(blank=True, null=True)
    ip_address = models.CharField(max_length=45, blank=True, null=True)
    user_agent = models.TextField(blank=True, null=True)
    date_creation = models.DateTimeField(blank=True, null=True)
    date_expiration = models.DateTimeField()
    derniere_activite = models.DateTimeField(blank=True, null=True)
    active = models.BooleanField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sessions_utilisateur'


class Stocks(models.Model):
    id = models.UUIDField(primary_key=True)
    organisation = models.ForeignKey(Organisations, models.DO_NOTHING)
    entrepot = models.ForeignKey(Entrepots, models.DO_NOTHING)
    produit = models.ForeignKey(Produits, models.DO_NOTHING)
    variante = models.ForeignKey('VariantesProduits', models.DO_NOTHING, blank=True, null=True)
    quantite_disponible = models.DecimalField(max_digits=12, decimal_places=3, blank=True, null=True)
    quantite_reservee = models.DecimalField(max_digits=12, decimal_places=3, blank=True, null=True)
    quantite_en_commande = models.DecimalField(max_digits=12, decimal_places=3, blank=True, null=True)
    quantite_totale = models.DecimalField(max_digits=12, decimal_places=3, blank=True, null=True)
    emplacement = models.CharField(max_length=100, blank=True, null=True)
    valeur_stock_achat = models.DecimalField(max_digits=14, decimal_places=2, blank=True, null=True)
    valeur_stock_vente = models.DecimalField(max_digits=14, decimal_places=2, blank=True, null=True)
    date_dernier_mouvement = models.DateTimeField(blank=True, null=True)
    date_derniere_entree = models.DateTimeField(blank=True, null=True)
    date_derniere_sortie = models.DateTimeField(blank=True, null=True)
    date_dernier_inventaire = models.DateTimeField(blank=True, null=True)
    date_modification = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'stocks'
        unique_together = (('entrepot', 'produit', 'variante'), ('entrepot', 'produit'),)
        db_table_comment = 'Gestion du stock par entrepôt et variante'


class Taxes(models.Model):
    id = models.UUIDField(primary_key=True)
    organisation = models.ForeignKey(Organisations, models.DO_NOTHING, blank=True, null=True)
    nom = models.CharField(max_length=100)
    code = models.CharField(max_length=20)
    taux = models.DecimalField(max_digits=5, decimal_places=2)
    type = models.CharField(max_length=50, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    actif = models.BooleanField(blank=True, null=True)
    par_defaut = models.BooleanField(blank=True, null=True)
    date_creation = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'taxes'


class TransactionsCaisse(models.Model):
    id = models.UUIDField(primary_key=True)
    organisation = models.ForeignKey(Organisations, models.DO_NOTHING)
    session_caisse = models.ForeignKey(SessionsCaisse, models.DO_NOTHING)
    numero_transaction = models.CharField(max_length=50)
    type_transaction = models.CharField(max_length=50)
    montant = models.DecimalField(max_digits=14, decimal_places=2)
    mode_paiement = models.ForeignKey(ModesPaiement, models.DO_NOTHING, blank=True, null=True)
    facture = models.ForeignKey(Factures, models.DO_NOTHING, blank=True, null=True)
    paiement = models.ForeignKey(Paiements, models.DO_NOTHING, blank=True, null=True)
    commande = models.ForeignKey(Commandes, models.DO_NOTHING, blank=True, null=True)
    motif = models.TextField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    numero_recu = models.CharField(max_length=50, blank=True, null=True)
    recu_imprime = models.BooleanField(blank=True, null=True)
    date_transaction = models.DateTimeField(blank=True, null=True)
    effectue_par = models.ForeignKey(Employes, models.DO_NOTHING, db_column='effectue_par', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'transactions_caisse'
        unique_together = (('organisation', 'numero_transaction'),)
        db_table_comment = 'Toutes les transactions de caisse (ventes, entrées, sorties)'


class TypeOrganisations(models.Model):
    id = models.BigAutoField(primary_key=True)
    description = models.CharField(unique=True)
    created_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'type_organisations'
        db_table_comment = "Liste des differents types d'organisations pour à l'avenir creer des interfaces adaptés à chaque organisation"


class TypesNotifications(models.Model):
    id = models.UUIDField(primary_key=True)
    code = models.CharField(unique=True, max_length=50)
    nom = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    canal_email = models.BooleanField(blank=True, null=True)
    canal_sms = models.BooleanField(blank=True, null=True)
    canal_push = models.BooleanField(blank=True, null=True)
    canal_in_app = models.BooleanField(blank=True, null=True)
    actif = models.BooleanField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'types_notifications'


class UnitesMesure(models.Model):
    id = models.UUIDField(primary_key=True)
    organisation = models.ForeignKey(Organisations, models.DO_NOTHING, blank=True, null=True)
    nom = models.CharField(max_length=50)
    symbole = models.CharField(max_length=10)
    type = models.CharField(max_length=50, blank=True, null=True)
    actif = models.BooleanField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'unites_mesure'


class Utilisateurs(models.Model):
    id = models.UUIDField(primary_key=True)
    email = models.TextField(unique=True, blank=True, null=True)
    nom_complet = models.TextField()
    telephone = models.TextField(blank=True, null=True)
    avatar_url = models.TextField(blank=True, null=True)
    langue = models.CharField(max_length=5, blank=True, null=True)
    fuseau_horaire = models.CharField(max_length=50, blank=True, null=True)
    actif = models.BooleanField(blank=True, null=True)
    email_verifie = models.BooleanField(blank=True, null=True)
    date_verification_email = models.DateTimeField(blank=True, null=True)
    preferences = models.JSONField(blank=True, null=True, db_comment='Préférences utilisateur: notifications, thème, etc.')
    date_creation = models.DateTimeField(blank=True, null=True)
    date_modification = models.DateTimeField(blank=True, null=True)
    date_suppression = models.DateTimeField(blank=True, null=True)
    password = models.CharField(max_length=128, blank=True, null=True)
    derniere_connexion = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField(blank=True, null=True)
    is_staff = models.BooleanField(blank=True, null=True)
    telephone_verifie = models.BooleanField(blank=True, null=True)
    date_verification_telephone = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'utilisateurs'
        db_table_comment = 'Utilisateurs principaux pouvant gérer plusieurs organisations'


class UtilisateursOrganisations(models.Model):
    id = models.UUIDField(primary_key=True)
    utilisateur = models.ForeignKey(Utilisateurs, models.DO_NOTHING)
    organisation = models.ForeignKey(Organisations, models.DO_NOTHING)
    role = models.CharField(max_length=50)
    est_principal = models.BooleanField(blank=True, null=True)
    date_ajout = models.DateTimeField(blank=True, null=True)
    ajoute_par = models.ForeignKey(Utilisateurs, models.DO_NOTHING, db_column='ajoute_par', related_name='utilisateursorganisations_ajoute_par_set', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'utilisateurs_organisations'
        unique_together = (('utilisateur', 'organisation'),)
        db_table_comment = 'Association N-N: un utilisateur peut gérer plusieurs organisations'


class UtilisationsCodesPromo(models.Model):
    id = models.UUIDField(primary_key=True)
    code_promo = models.ForeignKey(CodesPromo, models.DO_NOTHING)
    commande = models.ForeignKey(Commandes, models.DO_NOTHING)
    client = models.ForeignKey(Clients, models.DO_NOTHING, blank=True, null=True)
    montant_reduction = models.DecimalField(max_digits=10, decimal_places=2)
    date_utilisation = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'utilisations_codes_promo'


class VariantesProduits(models.Model):
    id = models.UUIDField(primary_key=True)
    produit = models.ForeignKey(Produits, models.DO_NOTHING)
    organisation = models.ForeignKey(Organisations, models.DO_NOTHING)
    code_variante = models.CharField(max_length=100)
    nom_variante = models.CharField(max_length=200, blank=True, null=True)
    attributs = models.JSONField()
    prix_achat_ht = models.DecimalField(max_digits=14, decimal_places=2, blank=True, null=True)
    prix_vente_ht = models.DecimalField(max_digits=14, decimal_places=2, blank=True, null=True)
    prix_vente_ttc = models.DecimalField(max_digits=14, decimal_places=2, blank=True, null=True)
    code_barre = models.CharField(max_length=100, blank=True, null=True)
    reference_fournisseur = models.TextField(blank=True, null=True)
    image_url = models.TextField(blank=True, null=True)
    stock_alerte = models.IntegerField(blank=True, null=True)
    actif = models.BooleanField(blank=True, null=True)
    date_creation = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'variantes_produits'
        unique_together = (('organisation', 'code_variante'),)
