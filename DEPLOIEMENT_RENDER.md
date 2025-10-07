# 🚀 Guide de Déploiement sur Render

## 📋 Prérequis

- Un compte GitHub
- Un compte Render (gratuit) : https://render.com
- Git installé sur votre machine

## 📦 Étape 1 : Préparer le projet

### 1.1 Vérifier les fichiers de configuration

Assurez-vous que ces fichiers existent :
- ✅ `requirements.txt` - Dépendances Python
- ✅ `build.sh` - Script de build
- ✅ `render.yaml` - Configuration Render
- ✅ `.gitignore` - Fichiers à ignorer

### 1.2 Initialiser Git (si pas déjà fait)

```bash
git init
git add .
git commit -m "Initial commit - Walee SaaS"
```

### 1.3 Créer un dépôt GitHub

1. Allez sur https://github.com/new
2. Créez un nouveau dépôt nommé `walee-saas`
3. Ne cochez PAS "Initialize with README"
4. Cliquez sur "Create repository"

### 1.4 Pousser le code sur GitHub

```bash
git remote add origin https://github.com/VOTRE_USERNAME/walee-saas.git
git branch -M main
git push -u origin main
```

## 🌐 Étape 2 : Déployer sur Render

### 2.1 Créer un compte Render

1. Allez sur https://render.com
2. Cliquez sur "Get Started for Free"
3. Connectez-vous avec GitHub

### 2.2 Créer un nouveau Web Service

1. Dans le dashboard Render, cliquez sur "New +"
2. Sélectionnez "Web Service"
3. Connectez votre dépôt GitHub `walee-saas`
4. Cliquez sur "Connect"

### 2.3 Configurer le Web Service

Remplissez les informations suivantes :

**Informations de base :**
- **Name:** `walee` (ou le nom de votre choix)
- **Region:** `Frankfurt (EU Central)` (le plus proche de l'Afrique)
- **Branch:** `main`
- **Root Directory:** (laisser vide)

**Build & Deploy :**
- **Runtime:** `Python 3`
- **Build Command:** `./build.sh`
- **Start Command:** `gunicorn walee.wsgi:application`

**Plan :**
- Sélectionnez **Free** (gratuit)

### 2.4 Configurer les variables d'environnement

Dans la section "Environment", ajoutez ces variables :

| Clé | Valeur |
|-----|--------|
| `PYTHON_VERSION` | `3.11.0` |
| `SECRET_KEY` | (Générer une clé secrète - voir ci-dessous) |
| `DEBUG` | `False` |
| `ALLOWED_HOSTS` | `.onrender.com` |

**Pour générer une SECRET_KEY :**
```python
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### 2.5 Créer la base de données PostgreSQL

1. Dans le dashboard Render, cliquez sur "New +"
2. Sélectionnez "PostgreSQL"
3. Configurez :
   - **Name:** `walee-db`
   - **Database:** `walee`
   - **User:** `walee`
   - **Region:** `Frankfurt (EU Central)` (même région que le web service)
   - **Plan:** `Free`
4. Cliquez sur "Create Database"

### 2.6 Lier la base de données au Web Service

1. Copiez l'URL de connexion PostgreSQL (Internal Database URL)
2. Retournez dans votre Web Service
3. Ajoutez une nouvelle variable d'environnement :
   - **Clé:** `DATABASE_URL`
   - **Valeur:** (Collez l'URL PostgreSQL)

### 2.7 Déployer

1. Cliquez sur "Create Web Service"
2. Render va automatiquement :
   - Cloner votre dépôt
   - Installer les dépendances
   - Exécuter les migrations
   - Collecter les fichiers statiques
   - Démarrer l'application

## ✅ Étape 3 : Vérification

### 3.1 Vérifier le déploiement

1. Attendez que le build soit terminé (environ 2-5 minutes)
2. Votre application sera disponible à : `https://walee.onrender.com`

### 3.2 Créer un superutilisateur

Pour accéder à l'admin Django :

1. Dans Render, allez dans votre Web Service
2. Cliquez sur "Shell" dans le menu de gauche
3. Exécutez :
```bash
python manage.py createsuperuser
```

### 3.3 Accéder à l'application

- **Site web :** `https://walee.onrender.com`
- **Admin Django :** `https://walee.onrender.com/admin`

## 🔄 Étape 4 : Mises à jour futures

Pour déployer des modifications :

```bash
git add .
git commit -m "Description des modifications"
git push origin main
```

Render redéploiera automatiquement votre application ! 🎉

## 🐛 Dépannage

### Erreur de build

Si le build échoue :
1. Vérifiez les logs dans Render
2. Assurez-vous que `build.sh` est exécutable :
   ```bash
   chmod +x build.sh
   git add build.sh
   git commit -m "Make build.sh executable"
   git push
   ```

### Erreur de base de données

Si les migrations échouent :
1. Vérifiez que `DATABASE_URL` est correctement configuré
2. Vérifiez que la base de données PostgreSQL est active
3. Relancez le déploiement

### Fichiers statiques manquants

Si les CSS/JS ne chargent pas :
1. Vérifiez que WhiteNoise est installé
2. Vérifiez `STATIC_ROOT` dans `settings.py`
3. Relancez `python manage.py collectstatic`

## 📊 Limites du plan gratuit

**Web Service gratuit :**
- ✅ 750 heures/mois
- ✅ SSL automatique
- ⚠️ Se met en veille après 15 min d'inactivité
- ⚠️ Redémarre en ~30 secondes à la première requête

**PostgreSQL gratuit :**
- ✅ 1 GB de stockage
- ✅ Expire après 90 jours (sauvegarder vos données !)

## 🚀 Passer en production (Plan payant)

Pour un site en production :
- **Starter Plan** : $7/mois
  - Pas de mise en veille
  - Plus de ressources
  - Base de données permanente

## 📝 Checklist finale

- [ ] Code poussé sur GitHub
- [ ] Web Service créé sur Render
- [ ] Base de données PostgreSQL créée
- [ ] Variables d'environnement configurées
- [ ] Build réussi
- [ ] Site accessible
- [ ] Superutilisateur créé
- [ ] Admin Django accessible

## 🎉 Félicitations !

Votre application Walee est maintenant déployée et accessible en ligne ! 🚀

---

**Support :** Pour toute question, consultez la documentation Render : https://render.com/docs
