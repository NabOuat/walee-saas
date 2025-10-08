/**
 * Validation utilities for Walee forms
 */

const WaleeValidation = {
    
    // Regex patterns
    patterns: {
        email: /^[^\s@]+@[^\s@]+\.[^\s@]+$/,
        phone: /^(\+225|0)[0-9]{10}$/,
        password: /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{8,}$/,
        codeBarre: /^[0-9]{13}$/,
        rccm: /^[A-Z]{2}-[0-9]{4}-[A-Z]{2}-[0-9]{5}$/
    },
    
    // Validate email
    validateEmail(email) {
        if (!email) {
            return { valid: false, message: 'Email requis' };
        }
        if (!this.patterns.email.test(email)) {
            return { valid: false, message: 'Format email invalide' };
        }
        return { valid: true, message: '' };
    },
    
    // Validate phone
    validatePhone(phone) {
        if (!phone) {
            return { valid: false, message: 'Téléphone requis' };
        }
        // Remove spaces and dashes
        const cleaned = phone.replace(/[\s-]/g, '');
        if (!this.patterns.phone.test(cleaned)) {
            return { valid: false, message: 'Format: +225 XX XX XX XX XX ou 07 XX XX XX XX' };
        }
        return { valid: true, message: '' };
    },
    
    // Validate password
    validatePassword(password) {
        if (!password) {
            return { valid: false, message: 'Mot de passe requis' };
        }
        if (password.length < 8) {
            return { valid: false, message: 'Minimum 8 caractères' };
        }
        if (!this.patterns.password.test(password)) {
            return { valid: false, message: 'Doit contenir: majuscule, minuscule, chiffre' };
        }
        return { valid: true, message: '' };
    },
    
    // Validate password confirmation
    validatePasswordConfirm(password, confirm) {
        if (!confirm) {
            return { valid: false, message: 'Confirmation requise' };
        }
        if (password !== confirm) {
            return { valid: false, message: 'Les mots de passe ne correspondent pas' };
        }
        return { valid: true, message: '' };
    },
    
    // Validate required field
    validateRequired(value, fieldName = 'Ce champ') {
        if (!value || value.trim() === '') {
            return { valid: false, message: `${fieldName} est requis` };
        }
        return { valid: true, message: '' };
    },
    
    // Validate barcode
    validateBarcode(code) {
        if (!code) {
            return { valid: false, message: 'Code-barre requis' };
        }
        if (!this.patterns.codeBarre.test(code)) {
            return { valid: false, message: 'Code-barre EAN-13 invalide (13 chiffres)' };
        }
        return { valid: true, message: '' };
    },
    
    // Validate RCCM
    validateRCCM(rccm) {
        if (!rccm) {
            return { valid: true, message: '' }; // Optional
        }
        if (!this.patterns.rccm.test(rccm)) {
            return { valid: false, message: 'Format RCCM invalide (ex: CI-2024-AB-12345)' };
        }
        return { valid: true, message: '' };
    },
    
    // Validate number
    validateNumber(value, min = null, max = null) {
        if (!value && value !== 0) {
            return { valid: false, message: 'Valeur requise' };
        }
        const num = parseFloat(value);
        if (isNaN(num)) {
            return { valid: false, message: 'Doit être un nombre' };
        }
        if (min !== null && num < min) {
            return { valid: false, message: `Minimum: ${min}` };
        }
        if (max !== null && num > max) {
            return { valid: false, message: `Maximum: ${max}` };
        }
        return { valid: true, message: '' };
    },
    
    // Show error message
    showError(inputElement, message) {
        // Remove existing error
        this.clearError(inputElement);
        
        // Add error class
        inputElement.classList.add('border-red-500', 'focus:ring-red-500');
        inputElement.classList.remove('border-gray-300', 'focus:ring-walee-blue');
        
        // Create error message
        const errorDiv = document.createElement('div');
        errorDiv.className = 'text-red-600 text-xs mt-1 flex items-center space-x-1';
        errorDiv.innerHTML = `
            <i data-lucide="alert-circle" class="w-3 h-3"></i>
            <span>${message}</span>
        `;
        errorDiv.setAttribute('data-error', 'true');
        
        // Insert after input
        inputElement.parentElement.insertAdjacentElement('afterend', errorDiv);
        
        // Reinitialize icons
        if (typeof lucide !== 'undefined') {
            lucide.createIcons();
        }
    },
    
    // Clear error message
    clearError(inputElement) {
        // Remove error class
        inputElement.classList.remove('border-red-500', 'focus:ring-red-500');
        inputElement.classList.add('border-gray-300', 'focus:ring-walee-blue');
        
        // Remove error message
        const errorDiv = inputElement.parentElement.parentElement.querySelector('[data-error="true"]');
        if (errorDiv) {
            errorDiv.remove();
        }
    },
    
    // Show success message
    showSuccess(inputElement) {
        this.clearError(inputElement);
        inputElement.classList.add('border-green-500', 'focus:ring-green-500');
        inputElement.classList.remove('border-gray-300', 'focus:ring-walee-blue');
    },
    
    // Validate form
    validateForm(formElement) {
        let isValid = true;
        const inputs = formElement.querySelectorAll('input[required], select[required], textarea[required]');
        
        inputs.forEach(input => {
            const value = input.value.trim();
            const type = input.type;
            
            if (!value) {
                this.showError(input, 'Ce champ est requis');
                isValid = false;
            } else if (type === 'email') {
                const result = this.validateEmail(value);
                if (!result.valid) {
                    this.showError(input, result.message);
                    isValid = false;
                } else {
                    this.showSuccess(input);
                }
            } else if (type === 'tel') {
                const result = this.validatePhone(value);
                if (!result.valid) {
                    this.showError(input, result.message);
                    isValid = false;
                } else {
                    this.showSuccess(input);
                }
            } else if (type === 'password') {
                const result = this.validatePassword(value);
                if (!result.valid) {
                    this.showError(input, result.message);
                    isValid = false;
                } else {
                    this.showSuccess(input);
                }
            } else {
                this.showSuccess(input);
            }
        });
        
        return isValid;
    },
    
    // Real-time validation
    setupRealTimeValidation(formElement) {
        const inputs = formElement.querySelectorAll('input, select, textarea');
        
        inputs.forEach(input => {
            input.addEventListener('blur', () => {
                const value = input.value.trim();
                const type = input.type;
                
                if (!value && input.hasAttribute('required')) {
                    this.showError(input, 'Ce champ est requis');
                } else if (value) {
                    if (type === 'email') {
                        const result = this.validateEmail(value);
                        if (!result.valid) {
                            this.showError(input, result.message);
                        } else {
                            this.showSuccess(input);
                        }
                    } else if (type === 'tel') {
                        const result = this.validatePhone(value);
                        if (!result.valid) {
                            this.showError(input, result.message);
                        } else {
                            this.showSuccess(input);
                        }
                    } else if (type === 'password') {
                        const result = this.validatePassword(value);
                        if (!result.valid) {
                            this.showError(input, result.message);
                        } else {
                            this.showSuccess(input);
                        }
                    } else {
                        this.clearError(input);
                    }
                }
            });
            
            input.addEventListener('input', () => {
                if (input.classList.contains('border-red-500')) {
                    this.clearError(input);
                }
            });
        });
    }
};

// Export for use in other scripts
if (typeof module !== 'undefined' && module.exports) {
    module.exports = WaleeValidation;
}
