# 🎉 GUIDE D'UTILISATION - TOASTS & LOADING

## ✅ **SYSTÈME INSTALLÉ**

Les composants Toast et Loading sont maintenant disponibles **globalement** dans toutes les pages dashboard !

---

## 🍞 **1. TOASTS (Notifications)**

### **Utilisation simple**

```javascript
// Succès
showToast('Vente enregistrée avec succès !', 'success');

// Erreur
showToast('Impossible de sauvegarder', 'error');

// Info
showToast('Nouvelle mise à jour disponible', 'info');

// Warning
showToast('Stock faible pour ce produit', 'warning');
```

---

### **Utilisation avancée**

```javascript
// Avec titre personnalisé
showToast('Facture créée', 'success', 'Opération réussie');

// Avec durée personnalisée (en ms)
showToast('Message important', 'warning', null, 5000); // 5 secondes

// Via événement custom
window.dispatchEvent(new CustomEvent('toast', {
    detail: {
        message: 'Produit ajouté au panier',
        type: 'success',
        title: 'Panier',
        duration: 3000
    }
}));
```

---

### **Types de toasts disponibles**

| Type | Couleur | Icône | Usage |
|------|---------|-------|-------|
| `success` | Vert | ✓ | Opération réussie |
| `error` | Rouge | ✗ | Erreur |
| `info` | Bleu | ℹ | Information |
| `warning` | Orange | ⚠ | Attention |

---

### **Exemples d'intégration**

#### **Dans un formulaire**
```javascript
createFacture() {
    // Validation
    if (!this.clientId) {
        showToast('Veuillez sélectionner un client', 'error');
        return;
    }
    
    // Traitement...
    
    // Succès
    showToast('Facture créée avec succès !', 'success');
    this.showModal = false;
}
```

#### **Dans une suppression**
```javascript
deleteItem(item) {
    if (confirm('Supprimer cet élément ?')) {
        // Suppression...
        showToast(`${item.nom} supprimé`, 'success', 'Suppression');
    }
}
```

#### **Dans une action asynchrone**
```javascript
async saveData() {
    try {
        // API call...
        showToast('Données sauvegardées', 'success');
    } catch (error) {
        showToast('Erreur lors de la sauvegarde', 'error');
    }
}
```

---

## ⏳ **2. LOADING STATES**

### **Loading global (overlay)**

```javascript
// Afficher
showLoading('Chargement des données...');

// Masquer
hideLoading();
```

---

### **Exemple complet**

```javascript
async validerVente() {
    // Afficher loading
    showLoading('Enregistrement de la vente...');
    
    try {
        // Simulation API call
        await new Promise(resolve => setTimeout(resolve, 2000));
        
        // Masquer loading
        hideLoading();
        
        // Afficher succès
        showToast('Vente enregistrée avec succès !', 'success');
        
        // Reset
        this.panier = [];
    } catch (error) {
        hideLoading();
        showToast('Erreur lors de l\'enregistrement', 'error');
    }
}
```

---

### **Loading sur bouton (inline)**

```html
<button @click="handleSubmit()" 
        :disabled="loading"
        class="px-6 py-3 bg-blue-600 text-white rounded-lg disabled:opacity-50">
    
    <!-- Texte normal -->
    <span x-show="!loading" class="flex items-center space-x-2">
        <i data-lucide="check"></i>
        <span>Valider</span>
    </span>
    
    <!-- État loading -->
    <span x-show="loading" class="flex items-center space-x-2">
        <svg class="animate-spin h-5 w-5" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
        </svg>
        <span>Chargement...</span>
    </span>
</button>
```

```javascript
data() {
    return {
        loading: false
    }
},

async handleSubmit() {
    this.loading = true;
    
    try {
        // Traitement...
        await someAsyncOperation();
        showToast('Succès !', 'success');
    } catch (error) {
        showToast('Erreur', 'error');
    } finally {
        this.loading = false;
    }
}
```

---

### **Skeleton Loader (chargement de contenu)**

```html
<!-- Pendant le chargement -->
<div x-show="loading" class="space-y-4">
    <div class="animate-pulse">
        <!-- Titre -->
        <div class="h-4 bg-gray-200 dark:bg-gray-700 rounded w-3/4 mb-4"></div>
        <!-- Sous-titre -->
        <div class="h-4 bg-gray-200 dark:bg-gray-700 rounded w-1/2 mb-4"></div>
        <!-- Paragraphe -->
        <div class="h-4 bg-gray-200 dark:bg-gray-700 rounded w-full mb-2"></div>
        <div class="h-4 bg-gray-200 dark:bg-gray-700 rounded w-5/6"></div>
    </div>
</div>

<!-- Contenu réel -->
<div x-show="!loading">
    <!-- Votre contenu -->
</div>
```

---

## 🎯 **EXEMPLES D'INTÉGRATION COMPLÈTE**

### **Page Caisse - Validation vente**

```javascript
async validerVente() {
    if (this.panier.length === 0) {
        showToast('Le panier est vide', 'warning');
        return;
    }
    
    showLoading('Enregistrement de la vente...');
    
    try {
        // Simulation API
        await new Promise(resolve => setTimeout(resolve, 1500));
        
        const total = this.getTotal() * 1.18;
        const nbArticles = this.panier.reduce((sum, item) => sum + item.quantite, 0);
        
        hideLoading();
        
        showToast(
            `Vente de ${this.formatMoney(total)} enregistrée`,
            'success',
            'Vente validée'
        );
        
        // Reset
        this.panier = [];
        this.clientId = '';
        this.modePaiement = 'Espèces';
        
    } catch (error) {
        hideLoading();
        showToast('Erreur lors de l\'enregistrement', 'error');
    }
}
```

---

### **Page Comptable - Création facture**

```javascript
async createFacture() {
    // Validation
    if (!this.formData.client) {
        showToast('Veuillez sélectionner un client', 'error', 'Validation');
        return;
    }
    
    if (!this.formData.montant || this.formData.montant <= 0) {
        showToast('Le montant doit être supérieur à 0', 'error', 'Validation');
        return;
    }
    
    showLoading('Création de la facture...');
    
    try {
        // API call
        await new Promise(resolve => setTimeout(resolve, 1000));
        
        hideLoading();
        
        showToast(
            'Facture créée et envoyée au client',
            'success',
            'Facture créée'
        );
        
        this.showFactureModal = false;
        this.resetForm();
        
    } catch (error) {
        hideLoading();
        showToast('Impossible de créer la facture', 'error');
    }
}
```

---

### **Page Stock - Alerte stock faible**

```javascript
checkStock(produit) {
    if (produit.stock < 10) {
        showToast(
            `Stock faible pour ${produit.nom} (${produit.stock} restants)`,
            'warning',
            'Alerte Stock'
        );
    }
}
```

---

## 🎨 **PERSONNALISATION**

### **Modifier la durée par défaut**

Dans `toast.html`, ligne 58 :
```javascript
duration: config.duration || 3000  // Changer 3000 (3s)
```

### **Modifier la position**

Dans `toast.html`, ligne 3 :
```html
class="fixed top-4 right-4 z-[9999]"
<!-- Changer top-4 right-4 pour autre position -->
<!-- Exemples: bottom-4 left-4, top-4 left-1/2 -translate-x-1/2 -->
```

### **Ajouter un son**

```javascript
showToast(message, type) {
    // Jouer un son
    const audio = new Audio('/static/sounds/notification.mp3');
    audio.play();
    
    // Afficher toast
    window.showToast(message, type);
}
```

---

## 📊 **BONNES PRATIQUES**

### **✅ À FAIRE**

```javascript
// Messages clairs et concis
showToast('Produit ajouté au panier', 'success');

// Feedback immédiat
button.onclick = () => {
    showToast('Action en cours...', 'info');
};

// Erreurs explicites
showToast('Email invalide', 'error');
```

### **❌ À ÉVITER**

```javascript
// Messages trop longs
showToast('Votre produit a été ajouté au panier avec succès et vous pouvez maintenant...', 'success');

// Trop de toasts en même temps
showToast('Message 1', 'info');
showToast('Message 2', 'info');
showToast('Message 3', 'info'); // Spam !

// Loading sans hideLoading()
showLoading();
// Oubli de hideLoading() = écran bloqué !
```

---

## 🐛 **TROUBLESHOOTING**

### **Les toasts ne s'affichent pas**

1. Vérifier que `base_dashboard.html` inclut bien les composants
2. Vérifier la console pour erreurs JavaScript
3. Vérifier que Alpine.js est chargé

### **Les icônes ne s'affichent pas**

```javascript
// Recharger les icônes après affichage
this.$nextTick(() => lucide.createIcons());
```

### **Loading ne se cache pas**

```javascript
// Toujours utiliser try/finally
try {
    showLoading();
    // ...
} finally {
    hideLoading(); // Toujours exécuté
}
```

---

## 🎉 **C'EST PRÊT !**

Le système Toast + Loading est maintenant installé et prêt à l'emploi dans **toutes les pages dashboard** !

**Prochaines étapes** :
1. Remplacer les `alert()` restants par `showToast()`
2. Ajouter `showLoading()` sur les actions longues
3. Ajouter loading states sur les boutons

**Temps d'intégration par page** : 5-10 minutes ⚡
