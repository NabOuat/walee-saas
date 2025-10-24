# 🔗 Module Intégrations Walee

Module de gestion des intégrations modulaires pour les entreprises.

## 📁 Structure

```
integrations/
├── __init__.py           # Exports du module
├── models.py             # Modèles de données
├── views.py              # Vues API REST
├── serializers.py        # Serializers DRF
├── urls.py               # Routes API
└── README.md             # Ce fichier
```

## 📦 Modèles

### CategorieIntegration
Catégories d'intégrations (Gestion, Intelligence, Communication, Paiement)

### Integration
Intégrations disponibles dans Walee (10 intégrations natives)

### IntegrationUtilisateur
Intégrations activées par utilisateur avec configuration

## 🔌 API Endpoints

- `GET /api/integrations/` - Liste toutes les intégrations
- `GET /api/integrations/categories/` - Liste les catégories
- `GET /api/integrations/mes-integrations/` - Mes intégrations
- `POST /api/integrations/activer/<slug>/` - Activer
- `POST /api/integrations/desactiver/<slug>/` - Désactiver
- `PUT /api/integrations/configurer/<slug>/` - Configurer

## 🚀 Utilisation

```python
from accounts.integrations import (
    CategorieIntegration,
    Integration,
    IntegrationUtilisateur
)

# Récupérer toutes les intégrations
integrations = Integration.objects.all()

# Activer une intégration pour un utilisateur
integration = Integration.objects.get(slug='walee-intelligence')
IntegrationUtilisateur.objects.create(
    utilisateur=user,
    integration=integration,
    actif=True
)
```

## 📊 Intégrations disponibles

1. **Walee Réservations** - Gestion réservations
2. **Walee Stock** - Gestion stock intelligente
3. **Walee Caisse** - Caisse rapide
4. **Walee Livraison** - Livraison avec suivi
5. **Walee Équipe** - Gestion d'équipe
6. **Walee Intelligence** - Assistant IA (Premium)
7. **Walee Analytics** - Tableaux de bord
8. **Walee Fidélité** - Programme de fidélité
9. **Walee Marketing** - Marketing automation (Premium)
10. **Walee Pay** - Paiements Mobile Money

## 🔧 Initialisation

```bash
python manage.py init_integrations
```
