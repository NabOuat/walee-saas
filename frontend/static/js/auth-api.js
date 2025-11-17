/**
 * API d'authentification Walee
 * Gestion de l'inscription, connexion et OTP
 */

const API_BASE = 'http://localhost:8000/api/auth/';

/**
 * Inscription - Étape 1 : Envoyer OTP + données de base
 * @param {string} email - Email de l'utilisateur
 * @param {string} nom_complet - Nom complet de l'utilisateur
 * @param {string} telephone - Téléphone (optionnel)
 * @param {string} password - Mot de passe (optionnel mais recommandé)
 * @returns {Promise} Réponse de l'API
 */
async function inscription(email, nom_complet, telephone = null, password = null) {
    try {
        const body = { nom_complet };
        
        if (email) {
            body.email = email;
        }
        if (telephone) {
            body.telephone = telephone;
        }

        // Si un mot de passe est fourni, l'envoyer également au backend
        if (password) {
            body.password = password;
        }
        console.log('Body envoyé à l\'API:', body);
        const response = await fetch(`${API_BASE}register/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(body)
        });
        
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Erreur inscription:', error);
        return {
            success: false,
            message: 'Erreur de connexion au serveur'
        };
    }
}

/**
 * Connexion classique avec email/téléphone + mot de passe
 * @param {string} email - Email de l'utilisateur
 * @param {string} password - Mot de passe
 * @param {string} telephone - Téléphone (optionnel)
 * @param {string} loginMethod - Methode de connexion ('email' ou 'phone')
 * @returns {Promise} Réponse de l'API avec tokens
 */
async function connexion(email = null, password, telephone = null,loginMethod ) {
    try {
        const body = { password:password,
            loginMethod:loginMethod
         };
        if (email) {
            body.email = email;
        }
        if (telephone) {
            body.telephone = telephone ;
        }
        
        
        const response = await fetch(`${API_BASE}login/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(body)
        });
        
        const data = await response.json();
        
        console.log('Réponse login:', data);
        
        // Stocker les tokens si connexion réussie
        if (data.success) {
            // Le backend retourne les tokens directement dans data, pas dans data.data
            console.log('Stockage du token:', data.access_token);
            
            // Stocker dans localStorage ET cookies pour plus de fiabilité
            try {
                localStorage.setItem('access_token', data.access_token);
                localStorage.setItem('refresh_token', data.refresh_token);
                localStorage.setItem('user', JSON.stringify(data.user));
                console.log('Token stocké dans localStorage');
            } catch (e) {
                console.warn('localStorage indisponible:', e);
            }
            
            // Aussi stocker dans un cookie (persiste mieux entre les pages)
            try {
                document.cookie = `access_token=${data.access_token}; path=/; max-age=3600`;
                document.cookie = `refresh_token=${data.refresh_token}; path=/; max-age=3600`;
                console.log('Token stocké dans cookies');
            } catch (e) {
                console.warn('Cookies indisponibles:', e);
            }
            
            console.log('Vérification localStorage:', localStorage.getItem('access_token'));
            console.log('Vérification cookies:', document.cookie);
        }
        return data;
    } catch (error) {
        return {
            success: false,
            message: error || 'Erreur de connexion au serveur'
        };
    }
}

/**
 * Vérification OTP - Étape 2
 * @param {string} email - Email de l'utilisateur
 * @param {string} code - Code OTP à 6 chiffres
 * @param {string} telephone - Téléphone (optionnel)
 * @returns {Promise} Réponse de l'API avec tokens
 */
async function verifierOTP(email, code, telephone = null) {
    try {
        const body = { code };
        
        if (email) {
            body.email = email;
        }
        if (telephone) {
            body.telephone = telephone;
        }
        
        const response = await fetch(`${API_BASE}verify-otp/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(body)
        });
        
        const data = await response.json();
        
        // Si succès, stocker les tokens
        if (data.success && data.data) {
            localStorage.setItem('access_token', data.data.access_token);
            localStorage.setItem('refresh_token', data.data.refresh_token);
            localStorage.setItem('user', JSON.stringify(data.data.utilisateur));
            localStorage.setItem('session_id', data.data.session_id);
        }
        
        return data;
    } catch (error) {
        console.error('Erreur vérification OTP:', error);
        return {
            success: false,
            message: 'Erreur de connexion au serveur'
        };
    }
}

/**
 * Renvoyer un code OTP
 * @param {string} email - Email de l'utilisateur
 * @param {string} motif - Motif (inscription, connexion, verification, reset_password)
 * @param {string} telephone - Téléphone (optionnel)
 * @returns {Promise} Réponse de l'API
 */
async function renvoyerOTP(email = null, motif = 'connexion', telephone = null) {
    try {
        const body = { motif };
        
        if (email) {
            body.email = email;
        }
        if (telephone) {
            body.telephone = telephone;
        }
        
        const response = await fetch(`${API_BASE}resend-otp/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(body)
        });
        
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Erreur renvoi OTP:', error);
        return {
            success: false,
            message: 'Erreur de connexion au serveur'
        };
    }
}

/**
 * Déconnexion
 * @returns {Promise} Réponse de l'API
 */
async function deconnexion() {
    try {
        const token = localStorage.getItem('access_token');
        
        if (!token) {
            // Pas de token, juste nettoyer le localStorage
            nettoyerSession();
            return { success: true };
        }
        
        const response = await fetch(`${API_BASE}logout/`, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json'
            }
        });
        
        const data = await response.json();
        
        // Nettoyer le localStorage
        nettoyerSession();
        
        return data;
    } catch (error) {
        console.error('Erreur déconnexion:', error);
        // Nettoyer quand même
        nettoyerSession();
        return {
            success: false,
            message: 'Erreur de connexion au serveur'
        };
    }
}

/**
 * Récupérer le profil utilisateur
 * @returns {Promise} Profil utilisateur
 */
async function getProfile() {
    try {
        // Chercher le token dans localStorage d'abord, puis dans les cookies
        let token = localStorage.getItem('access_token');
        
        if (!token) {
            // Chercher dans les cookies
            const cookies = document.cookie.split(';');
            for (let cookie of cookies) {
                const [name, value] = cookie.trim().split('=');
                if (name === 'access_token') {
                    token = value;
                    break;
                }
            }
        }
        
        console.log('getProfile - Token trouvé:', !!token);
        console.log('getProfile - localStorage token:', !!localStorage.getItem('access_token'));
        console.log('getProfile - cookies:', document.cookie);
        
        if (!token) {
            return {
                success: false,
                message: 'Non authentifié'
            };
        }
        
        const response = await fetch(`${API_BASE}profile/`, {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json'
            }
        });
        
        if (response.status === 401) {
            // Token expiré
            nettoyerSession();
            window.location.href = '/login/';
            return;
        }
        
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Erreur récupération profil:', error);
        return {
            success: false,
            message: 'Erreur de connexion au serveur'
        };
    }
}

/**
 * Mettre à jour le profil utilisateur
 * @param {Object} updates - Données à mettre à jour
 * @returns {Promise} Profil mis à jour
 */
async function updateProfile(updates) {
    try {
        const token = localStorage.getItem('access_token');
        
        if (!token) {
            return {
                success: false,
                message: 'Non authentifié'
            };
        }
        
        const response = await fetch(`${API_BASE}profile/`, {
            method: 'PATCH',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(updates)
        });
        
        const data = await response.json();
        
        // Mettre à jour le localStorage si succès
        if (response.ok) {
            localStorage.setItem('user', JSON.stringify(data));
        }
        
        return data;
    } catch (error) {
        console.error('Erreur mise à jour profil:', error);
        return {
            success: false,
            message: 'Erreur de connexion au serveur'
        };
    }
}

/**
 * Vérifier si l'utilisateur est authentifié
 * @returns {boolean} True si authentifié
 */
function estAuthentifie() {
    const token = localStorage.getItem('access_token');
    const user = localStorage.getItem('user');
    return !!(token && user);
}

/**
 * Récupérer l'utilisateur depuis le localStorage
 * @returns {Object|null} Utilisateur ou null
 */
function getUtilisateur() {
    const userStr = localStorage.getItem('user');
    if (userStr) {
        try {
            return JSON.parse(userStr);
        } catch (e) {
            return null;
        }
    }
    return null;
}

/**
 * Nettoyer la session (localStorage)
 */
function nettoyerSession() {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    localStorage.removeItem('user');
    localStorage.removeItem('session_id');
}

/**
 * Rediriger vers le dashboard si authentifié
 */
function redirectSiAuthentifie() {
    if (estAuthentifie()) {
        window.location.href = '/dashboard/';
    }
}

/**
 * Rediriger vers login si non authentifié
 */
function redirectSiNonAuthentifie() {
    if (!estAuthentifie()) {
        window.location.href = '/login/';
    }
}

/**
 * Afficher un message toast
 * @param {string} message - Message à afficher
 * @param {string} type - Type (success, error, info, warning)
 */
function afficherToast(message, type = 'info') {
    // Créer l'élément toast
    const toast = document.createElement('div');
    toast.className = `fixed top-4 right-4 z-50 px-6 py-4 rounded-xl shadow-2xl animate-slide-down max-w-md`;
    
    // Couleurs selon le type
    const colors = {
        success: 'bg-green-500 text-white',
        error: 'bg-red-500 text-white',
        info: 'bg-blue-500 text-white',
        warning: 'bg-yellow-500 text-white'
    };
    
    toast.className += ` ${colors[type] || colors.info}`;
    
    // Icône selon le type
    const icons = {
        success: 'check-circle',
        error: 'x-circle',
        info: 'info',
        warning: 'alert-triangle'
    };
    
    toast.innerHTML = `
        <div class="flex items-center space-x-3">
            <i data-lucide="${icons[type] || icons.info}" class="w-6 h-6"></i>
            <p class="font-medium">${message}</p>
        </div>
    `;
    
    document.body.appendChild(toast);
    
    // Réinitialiser les icônes
    if (typeof lucide !== 'undefined') {
        lucide.createIcons();
    }
    
    // Supprimer après 5 secondes
    setTimeout(() => {
        toast.classList.add('animate-fade-out');
        setTimeout(() => {
            toast.remove();
        }, 300);
    }, 5000);
}

// Export pour utilisation dans d'autres scripts
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        inscription,
        connexion,
        verifierOTP,
        renvoyerOTP,
        deconnexion,
        getProfile,
        updateProfile,
        estAuthentifie,
        getUtilisateur,
        nettoyerSession,
        redirectSiAuthentifie,
        redirectSiNonAuthentifie,
        afficherToast
    };
}
