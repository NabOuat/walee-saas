// PWA Installation Handler

// Enregistrer le Service Worker
if ('serviceWorker' in navigator) {
    window.addEventListener('load', () => {
        navigator.serviceWorker.register('/static/js/service-worker.js')
            .then((registration) => {
                console.log('Service Worker enregistré:', registration.scope);
            })
            .catch((error) => {
                console.log('Erreur Service Worker:', error);
            });
    });
}

// Gérer l'installation PWA
let deferredPrompt;
let installButton;

window.addEventListener('beforeinstallprompt', (e) => {
    // Empêcher l'affichage automatique
    e.preventDefault();
    deferredPrompt = e;
    
    // Afficher le bouton d'installation personnalisé
    showInstallPromotion();
});

function showInstallPromotion() {
    // Créer le bouton d'installation
    const installBanner = document.createElement('div');
    installBanner.id = 'pwa-install-banner';
    installBanner.className = 'fixed bottom-4 right-4 bg-white dark:bg-gray-800 rounded-xl shadow-2xl p-4 max-w-sm z-50 border-2 border-blue-500';
    installBanner.innerHTML = `
        <div class="flex items-start space-x-3">
            <div class="w-12 h-12 bg-blue-100 dark:bg-blue-900 rounded-xl flex items-center justify-center flex-shrink-0">
                <svg class="w-6 h-6 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4"></path>
                </svg>
            </div>
            <div class="flex-1">
                <h3 class="font-bold text-gray-900 dark:text-white mb-1">Installer Walee</h3>
                <p class="text-sm text-gray-600 dark:text-gray-400 mb-3">
                    Installez l'application pour un accès rapide et hors ligne
                </p>
                <div class="flex space-x-2">
                    <button id="pwa-install-btn" class="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition text-sm font-semibold">
                        Installer
                    </button>
                    <button id="pwa-dismiss-btn" class="px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700 transition text-sm">
                        Plus tard
                    </button>
                </div>
            </div>
            <button id="pwa-close-btn" class="text-gray-400 hover:text-gray-600">
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
                </svg>
            </button>
        </div>
    `;
    
    document.body.appendChild(installBanner);
    
    // Gérer les clics
    document.getElementById('pwa-install-btn').addEventListener('click', installPWA);
    document.getElementById('pwa-dismiss-btn').addEventListener('click', dismissInstall);
    document.getElementById('pwa-close-btn').addEventListener('click', dismissInstall);
}

async function installPWA() {
    if (!deferredPrompt) return;
    
    // Afficher le prompt d'installation
    deferredPrompt.prompt();
    
    // Attendre la réponse
    const { outcome } = await deferredPrompt.userChoice;
    
    if (outcome === 'accepted') {
        console.log('PWA installée');
        showToast('Application installée avec succès !', 'success', 'Installation');
    } else {
        console.log('Installation refusée');
    }
    
    // Nettoyer
    deferredPrompt = null;
    dismissInstall();
}

function dismissInstall() {
    const banner = document.getElementById('pwa-install-banner');
    if (banner) {
        banner.remove();
    }
    
    // Sauvegarder la préférence
    localStorage.setItem('pwa-install-dismissed', Date.now());
}

// Vérifier si déjà installé
window.addEventListener('appinstalled', () => {
    console.log('PWA installée');
    showToast('Application installée !', 'success');
    dismissInstall();
});

// Vérifier le mode standalone (déjà installé)
if (window.matchMedia('(display-mode: standalone)').matches) {
    console.log('Application lancée en mode standalone');
}

// Gérer les mises à jour du Service Worker
if ('serviceWorker' in navigator) {
    navigator.serviceWorker.addEventListener('controllerchange', () => {
        // Nouvelle version disponible
        showToast('Nouvelle version disponible ! Rechargez la page.', 'info', 'Mise à jour', 10000);
    });
}

// Détecter le statut en ligne/hors ligne
window.addEventListener('online', () => {
    showToast('Connexion rétablie', 'success', 'En ligne');
});

window.addEventListener('offline', () => {
    showToast('Vous êtes hors ligne', 'warning', 'Hors ligne');
});

// Vérifier si on doit afficher le prompt (pas affiché depuis 7 jours)
const lastDismissed = localStorage.getItem('pwa-install-dismissed');
if (lastDismissed) {
    const daysSince = (Date.now() - parseInt(lastDismissed)) / (1000 * 60 * 60 * 24);
    if (daysSince < 7) {
        // Ne pas afficher si refusé il y a moins de 7 jours
        deferredPrompt = null;
    }
}
