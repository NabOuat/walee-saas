/**
 * Main JavaScript for Walee
 * Handles interactions and animations
 */

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', function() {
    
    // Initialize Lucide icons
    if (typeof lucide !== 'undefined') {
        lucide.createIcons();
    }
    
    // Smooth scroll for anchor links
    initSmoothScroll();
    
    // Form validation
    initFormValidation();
    
    // Toast notifications
    initToastNotifications();
    
    // Lazy loading images
    initLazyLoading();
    
    // Page transition effects
    initPageTransitions();
});

/**
 * Smooth scroll for anchor links
 */
function initSmoothScroll() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            const href = this.getAttribute('href');
            if (href !== '#' && href !== '#!') {
                e.preventDefault();
                const target = document.querySelector(href);
                if (target) {
                    target.scrollIntoView({
                        behavior: 'smooth',
                        block: 'start'
                    });
                }
            }
        });
    });
}

/**
 * Form validation
 */
function initFormValidation() {
    const forms = document.querySelectorAll('form[data-validate]');
    
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            if (!validateForm(this)) {
                e.preventDefault();
            }
        });
        
        // Real-time validation
        const inputs = form.querySelectorAll('input, textarea, select');
        inputs.forEach(input => {
            input.addEventListener('blur', function() {
                validateField(this);
            });
        });
    });
}

function validateForm(form) {
    let isValid = true;
    const inputs = form.querySelectorAll('input[required], textarea[required], select[required]');
    
    inputs.forEach(input => {
        if (!validateField(input)) {
            isValid = false;
        }
    });
    
    return isValid;
}

function validateField(field) {
    const value = field.value.trim();
    const type = field.type;
    let isValid = true;
    let errorMessage = '';
    
    // Required validation
    if (field.hasAttribute('required') && !value) {
        isValid = false;
        errorMessage = 'Ce champ est requis';
    }
    
    // Email validation
    if (type === 'email' && value) {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailRegex.test(value)) {
            isValid = false;
            errorMessage = 'Email invalide';
        }
    }
    
    // Phone validation
    if (type === 'tel' && value) {
        const phoneRegex = /^[\d\s\+\-\(\)]+$/;
        if (!phoneRegex.test(value)) {
            isValid = false;
            errorMessage = 'Numéro de téléphone invalide';
        }
    }
    
    // Password validation
    if (type === 'password' && value && field.hasAttribute('data-min-length')) {
        const minLength = parseInt(field.getAttribute('data-min-length'));
        if (value.length < minLength) {
            isValid = false;
            errorMessage = `Le mot de passe doit contenir au moins ${minLength} caractères`;
        }
    }
    
    // Password confirmation
    if (field.hasAttribute('data-confirm')) {
        const confirmField = document.querySelector(field.getAttribute('data-confirm'));
        if (confirmField && value !== confirmField.value) {
            isValid = false;
            errorMessage = 'Les mots de passe ne correspondent pas';
        }
    }
    
    // Display error
    showFieldError(field, isValid, errorMessage);
    
    return isValid;
}

function showFieldError(field, isValid, message) {
    // Remove existing error
    const existingError = field.parentElement.querySelector('.field-error');
    if (existingError) {
        existingError.remove();
    }
    
    if (!isValid) {
        field.classList.add('border-red-500');
        field.classList.remove('border-gray-300');
        
        const errorDiv = document.createElement('div');
        errorDiv.className = 'field-error text-red-500 text-sm mt-1';
        errorDiv.textContent = message;
        field.parentElement.appendChild(errorDiv);
    } else {
        field.classList.remove('border-red-500');
        field.classList.add('border-gray-300');
    }
}

/**
 * Toast notifications
 */
function initToastNotifications() {
    window.showToast = function(message, type = 'info') {
        const toast = document.createElement('div');
        toast.className = `fixed top-4 right-4 z-50 px-6 py-4 rounded-xl shadow-2xl transform transition-all duration-300 translate-x-full`;
        
        const colors = {
            success: 'bg-green-500 text-white',
            error: 'bg-red-500 text-white',
            warning: 'bg-yellow-500 text-white',
            info: 'bg-blue-500 text-white'
        };
        
        toast.className += ` ${colors[type] || colors.info}`;
        toast.innerHTML = `
            <div class="flex items-center space-x-3">
                <i data-lucide="${getToastIcon(type)}" class="w-5 h-5"></i>
                <span class="font-medium">${message}</span>
            </div>
        `;
        
        document.body.appendChild(toast);
        
        // Animate in
        setTimeout(() => {
            toast.classList.remove('translate-x-full');
        }, 100);
        
        // Reinitialize icons
        if (typeof lucide !== 'undefined') {
            lucide.createIcons();
        }
        
        // Remove after 3 seconds
        setTimeout(() => {
            toast.classList.add('translate-x-full');
            setTimeout(() => {
                toast.remove();
            }, 300);
        }, 3000);
    };
}

function getToastIcon(type) {
    const icons = {
        success: 'check-circle',
        error: 'x-circle',
        warning: 'alert-triangle',
        info: 'info'
    };
    return icons[type] || icons.info;
}

/**
 * Lazy loading images
 */
function initLazyLoading() {
    const images = document.querySelectorAll('img[data-src]');
    
    const imageObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                img.src = img.dataset.src;
                img.removeAttribute('data-src');
                observer.unobserve(img);
            }
        });
    });
    
    images.forEach(img => imageObserver.observe(img));
}

/**
 * Page transition effects
 */
function initPageTransitions() {
    // Add fade-in animation to main content
    const mainContent = document.querySelector('main, .page-content');
    if (mainContent) {
        mainContent.classList.add('animate-fade-in');
    }
}

/**
 * Copy to clipboard
 */
window.copyToClipboard = function(text) {
    navigator.clipboard.writeText(text).then(() => {
        showToast('Copié dans le presse-papier', 'success');
    }).catch(() => {
        showToast('Erreur lors de la copie', 'error');
    });
};

/**
 * Format currency
 */
window.formatCurrency = function(amount, currency = 'XOF') {
    return new Intl.NumberFormat('fr-FR', {
        style: 'currency',
        currency: currency,
        minimumFractionDigits: 0
    }).format(amount);
};

/**
 * Format date
 */
window.formatDate = function(date, format = 'short') {
    const options = {
        short: { year: 'numeric', month: 'short', day: 'numeric' },
        long: { year: 'numeric', month: 'long', day: 'numeric', hour: '2-digit', minute: '2-digit' },
        time: { hour: '2-digit', minute: '2-digit' }
    };
    
    return new Intl.DateTimeFormat('fr-FR', options[format] || options.short).format(new Date(date));
};

/**
 * Debounce function
 */
window.debounce = function(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
};

/**
 * Loading state
 */
window.setLoading = function(element, isLoading) {
    if (isLoading) {
        element.disabled = true;
        element.dataset.originalText = element.innerHTML;
        element.innerHTML = `
            <div class="flex items-center justify-center space-x-2">
                <div class="spinner w-5 h-5 border-2"></div>
                <span>Chargement...</span>
            </div>
        `;
    } else {
        element.disabled = false;
        element.innerHTML = element.dataset.originalText;
    }
};

// Export for use in other scripts
window.WaleeUtils = {
    showToast,
    copyToClipboard,
    formatCurrency,
    formatDate,
    debounce,
    setLoading
};
