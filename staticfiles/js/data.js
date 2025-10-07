/**
 * Données statiques pour Walee
 * Pays, devises, types d'activités
 */

// Liste des pays (focus Afrique + principaux pays)
const PAYS = [
    // Afrique de l'Ouest
    { code: 'BJ', nom: 'Bénin', region: 'Afrique de l\'Ouest' },
    { code: 'BF', nom: 'Burkina Faso', region: 'Afrique de l\'Ouest' },
    { code: 'CI', nom: 'Côte d\'Ivoire', region: 'Afrique de l\'Ouest' },
    { code: 'GH', nom: 'Ghana', region: 'Afrique de l\'Ouest' },
    { code: 'GN', nom: 'Guinée', region: 'Afrique de l\'Ouest' },
    { code: 'GW', nom: 'Guinée-Bissau', region: 'Afrique de l\'Ouest' },
    { code: 'LR', nom: 'Liberia', region: 'Afrique de l\'Ouest' },
    { code: 'ML', nom: 'Mali', region: 'Afrique de l\'Ouest' },
    { code: 'NE', nom: 'Niger', region: 'Afrique de l\'Ouest' },
    { code: 'NG', nom: 'Nigeria', region: 'Afrique de l\'Ouest' },
    { code: 'SN', nom: 'Sénégal', region: 'Afrique de l\'Ouest' },
    { code: 'SL', nom: 'Sierra Leone', region: 'Afrique de l\'Ouest' },
    { code: 'TG', nom: 'Togo', region: 'Afrique de l\'Ouest' },
    
    // Afrique Centrale
    { code: 'CM', nom: 'Cameroun', region: 'Afrique Centrale' },
    { code: 'CF', nom: 'République Centrafricaine', region: 'Afrique Centrale' },
    { code: 'TD', nom: 'Tchad', region: 'Afrique Centrale' },
    { code: 'CG', nom: 'Congo', region: 'Afrique Centrale' },
    { code: 'CD', nom: 'RD Congo', region: 'Afrique Centrale' },
    { code: 'GA', nom: 'Gabon', region: 'Afrique Centrale' },
    { code: 'GQ', nom: 'Guinée Équatoriale', region: 'Afrique Centrale' },
    
    // Afrique de l'Est
    { code: 'BI', nom: 'Burundi', region: 'Afrique de l\'Est' },
    { code: 'KM', nom: 'Comores', region: 'Afrique de l\'Est' },
    { code: 'DJ', nom: 'Djibouti', region: 'Afrique de l\'Est' },
    { code: 'ER', nom: 'Érythrée', region: 'Afrique de l\'Est' },
    { code: 'ET', nom: 'Éthiopie', region: 'Afrique de l\'Est' },
    { code: 'KE', nom: 'Kenya', region: 'Afrique de l\'Est' },
    { code: 'MG', nom: 'Madagascar', region: 'Afrique de l\'Est' },
    { code: 'MW', nom: 'Malawi', region: 'Afrique de l\'Est' },
    { code: 'MU', nom: 'Maurice', region: 'Afrique de l\'Est' },
    { code: 'MZ', nom: 'Mozambique', region: 'Afrique de l\'Est' },
    { code: 'RW', nom: 'Rwanda', region: 'Afrique de l\'Est' },
    { code: 'SC', nom: 'Seychelles', region: 'Afrique de l\'Est' },
    { code: 'SO', nom: 'Somalie', region: 'Afrique de l\'Est' },
    { code: 'SS', nom: 'Soudan du Sud', region: 'Afrique de l\'Est' },
    { code: 'TZ', nom: 'Tanzanie', region: 'Afrique de l\'Est' },
    { code: 'UG', nom: 'Ouganda', region: 'Afrique de l\'Est' },
    { code: 'ZM', nom: 'Zambie', region: 'Afrique de l\'Est' },
    { code: 'ZW', nom: 'Zimbabwe', region: 'Afrique de l\'Est' },
    
    // Afrique du Nord
    { code: 'DZ', nom: 'Algérie', region: 'Afrique du Nord' },
    { code: 'EG', nom: 'Égypte', region: 'Afrique du Nord' },
    { code: 'LY', nom: 'Libye', region: 'Afrique du Nord' },
    { code: 'MA', nom: 'Maroc', region: 'Afrique du Nord' },
    { code: 'SD', nom: 'Soudan', region: 'Afrique du Nord' },
    { code: 'TN', nom: 'Tunisie', region: 'Afrique du Nord' },
    
    // Afrique Australe
    { code: 'AO', nom: 'Angola', region: 'Afrique Australe' },
    { code: 'BW', nom: 'Botswana', region: 'Afrique Australe' },
    { code: 'LS', nom: 'Lesotho', region: 'Afrique Australe' },
    { code: 'NA', nom: 'Namibie', region: 'Afrique Australe' },
    { code: 'ZA', nom: 'Afrique du Sud', region: 'Afrique Australe' },
    { code: 'SZ', nom: 'Eswatini', region: 'Afrique Australe' },
    
    // Autres pays importants
    { code: 'FR', nom: 'France', region: 'Europe' },
    { code: 'US', nom: 'États-Unis', region: 'Amérique' },
    { code: 'GB', nom: 'Royaume-Uni', region: 'Europe' },
    { code: 'CA', nom: 'Canada', region: 'Amérique' },
];

// Liste des devises
const DEVISES = [
    // Devises africaines principales
    { code: 'XOF', nom: 'Franc CFA (BCEAO)', symbole: 'FCFA', pays: ['CI', 'SN', 'BF', 'ML', 'NE', 'TG', 'BJ', 'GW'] },
    { code: 'XAF', nom: 'Franc CFA (BEAC)', symbole: 'FCFA', pays: ['CM', 'CF', 'TD', 'CG', 'GA', 'GQ'] },
    { code: 'NGN', nom: 'Naira nigérian', symbole: '₦', pays: ['NG'] },
    { code: 'GHS', nom: 'Cedi ghanéen', symbole: 'GH₵', pays: ['GH'] },
    { code: 'KES', nom: 'Shilling kényan', symbole: 'KSh', pays: ['KE'] },
    { code: 'ZAR', nom: 'Rand sud-africain', symbole: 'R', pays: ['ZA'] },
    { code: 'EGP', nom: 'Livre égyptienne', symbole: 'E£', pays: ['EG'] },
    { code: 'MAD', nom: 'Dirham marocain', symbole: 'DH', pays: ['MA'] },
    { code: 'TND', nom: 'Dinar tunisien', symbole: 'DT', pays: ['TN'] },
    { code: 'DZD', nom: 'Dinar algérien', symbole: 'DA', pays: ['DZ'] },
    { code: 'ETB', nom: 'Birr éthiopien', symbole: 'Br', pays: ['ET'] },
    { code: 'TZS', nom: 'Shilling tanzanien', symbole: 'TSh', pays: ['TZ'] },
    { code: 'UGX', nom: 'Shilling ougandais', symbole: 'USh', pays: ['UG'] },
    { code: 'RWF', nom: 'Franc rwandais', symbole: 'FRw', pays: ['RW'] },
    { code: 'MUR', nom: 'Roupie mauricienne', symbole: '₨', pays: ['MU'] },
    
    // Devises internationales
    { code: 'EUR', nom: 'Euro', symbole: '€', pays: ['FR'] },
    { code: 'USD', nom: 'Dollar américain', symbole: '$', pays: ['US'] },
    { code: 'GBP', nom: 'Livre sterling', symbole: '£', pays: ['GB'] },
    { code: 'CAD', nom: 'Dollar canadien', symbole: 'C$', pays: ['CA'] },
];

// Types d'activités
const TYPES_ACTIVITES = [
    { value: 'commerce_detail', label: 'Commerce de détail' },
    { value: 'commerce_gros', label: 'Commerce de gros' },
    { value: 'restauration', label: 'Restauration' },
    { value: 'hotellerie', label: 'Hôtellerie' },
    { value: 'services', label: 'Services' },
    { value: 'electronique', label: 'Électronique' },
    { value: 'textile', label: 'Textile et habillement' },
    { value: 'alimentation', label: 'Alimentation' },
    { value: 'construction', label: 'Construction' },
    { value: 'transport', label: 'Transport' },
    { value: 'sante', label: 'Santé' },
    { value: 'education', label: 'Éducation' },
    { value: 'agriculture', label: 'Agriculture' },
    { value: 'immobilier', label: 'Immobilier' },
    { value: 'technologie', label: 'Technologie' },
    { value: 'autre', label: 'Autre (à préciser)' },
];

// Rôles d'employés
const ROLES_EMPLOYES = [
    { value: 'administrateur', label: 'Administrateur', color: 'purple' },
    { value: 'gerant', label: 'Gérant', color: 'blue' },
    { value: 'caissier', label: 'Caissier', color: 'green' },
    { value: 'gestionnaire_stock', label: 'Gestionnaire de stock', color: 'orange' },
    { value: 'vendeur', label: 'Vendeur', color: 'indigo' },
    { value: 'comptable', label: 'Comptable', color: 'pink' },
    { value: 'livreur', label: 'Livreur', color: 'yellow' },
];

// Export pour utilisation
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { PAYS, DEVISES, TYPES_ACTIVITES, ROLES_EMPLOYES };
}
