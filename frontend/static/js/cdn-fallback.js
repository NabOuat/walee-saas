/**
 * CDN Fallback Handler
 * Détecte si les CDN sont chargés et fournit des fallbacks
 */

(function() {
    'use strict';
    
    // Check if Tailwind CSS is loaded
    function checkTailwind() {
        return typeof tailwind !== 'undefined';
    }
    
    // Check if Alpine.js is loaded
    function checkAlpine() {
        return typeof Alpine !== 'undefined';
    }
    
    // Check if Lucide is loaded
    function checkLucide() {
        return typeof lucide !== 'undefined';
    }
    
    // Check if Chart.js is loaded
    function checkChart() {
        return typeof Chart !== 'undefined';
    }
    
    // Show warning banner
    function showOfflineWarning() {
        const banner = document.createElement('div');
        banner.className = 'fixed top-0 left-0 right-0 z-50 bg-yellow-500 text-white px-4 py-3 text-center text-sm font-medium';
        banner.innerHTML = `
            <div class="flex items-center justify-center space-x-2">
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"/>
                </svg>
                <span>Mode hors ligne - Certaines fonctionnalités peuvent être limitées</span>
            </div>
        `;
        document.body.prepend(banner);
    }
    
    // Check all CDNs
    function checkCDNs() {
        const checks = {
            tailwind: checkTailwind(),
            alpine: checkAlpine(),
            lucide: checkLucide(),
            chart: checkChart()
        };
        
        const allLoaded = Object.values(checks).every(v => v);
        
        if (!allLoaded) {
            console.warn('⚠️ Certains CDN ne sont pas chargés:', checks);
            
            // Show warning if offline
            if (!navigator.onLine) {
                showOfflineWarning();
            }
        } else {
            console.log('✅ Tous les CDN sont chargés');
        }
        
        return checks;
    }
    
    // Network status monitoring
    window.addEventListener('online', () => {
        console.log('✅ Connexion rétablie');
        const banner = document.querySelector('.fixed.top-0.bg-yellow-500');
        if (banner) {
            banner.remove();
        }
        // Reload page to get CDN resources
        setTimeout(() => {
            location.reload();
        }, 1000);
    });
    
    window.addEventListener('offline', () => {
        console.warn('⚠️ Connexion perdue');
        showOfflineWarning();
    });
    
    // Check on load
    window.addEventListener('load', () => {
        setTimeout(() => {
            checkCDNs();
        }, 1000);
    });
    
    // Graceful degradation for icons
    if (!checkLucide()) {
        console.warn('⚠️ Lucide icons non disponible - Utilisation de fallback');
        // Create simple icon fallback
        window.lucide = {
            createIcons: function() {
                console.log('Using icon fallback');
            }
        };
    }
    
})();
