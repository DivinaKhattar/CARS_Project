// CARS - Research Management System JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Initialize all components
    initializeTooltips();
    initializeFileUploads();
    initializeCalculations();
    initializeFormValidation();
    
    console.log('CARS Application initialized');
});

// Initialize Bootstrap tooltips
function initializeTooltips() {
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

// File upload handling
function initializeFileUploads() {
    const fileInputs = document.querySelectorAll('input[type="file"]');
    
    fileInputs.forEach(function(input) {
        input.addEventListener('change', function(e) {
            const file = e.target.files[0];
            if (file) {
                // Validate file type
                if (file.type !== 'application/pdf') {
                    alert('Please select a PDF file only.');
                    e.target.value = '';
                    return;
                }
                
                // Validate file size (10MB max)
                if (file.size > 10 * 1024 * 1024) {
                    alert('File size must be less than 10MB.');
                    e.target.value = '';
                    return;
                }
                
                // Show file name
                const fileName = file.name;
                const label = e.target.closest('.mb-3').querySelector('label');
                if (label) {
                    label.innerHTML = label.innerHTML.split(' - ')[0] + ' - ' + fileName;
                }
            }
        });
    });
}

// Auto calculations for summary offer
function initializeCalculations() {
    const personnelInput = document.getElementById('personnel_cost');
    const equipmentInput = document.getElementById('equipment_cost');
    const otherInput = document.getElementById('other_cost');
    
    if (personnelInput && equipmentInput && otherInput) {
        [personnelInput, equipmentInput, otherInput].forEach(function(input) {
            input.addEventListener('input', calculateTotals);
        });
        
        // Calculate on page load if values exist
        calculateTotals();
    }
}

function calculateTotals() {
    const personnel = parseFloat(document.getElementById('personnel_cost').value) || 0;
    const equipment = parseFloat(document.getElementById('equipment_cost').value) || 0;
    const other = parseFloat(document.getElementById('other_cost').value) || 0;
    
    const subtotal = personnel + equipment + other;
    const gst = subtotal * 0.18;
    const total = subtotal + gst;
    
    // Update display elements if they exist
    updateDisplayElement('subtotal-display', subtotal.toFixed(2));
    updateDisplayElement('gst-display', gst.toFixed(2));
    updateDisplayElement('total-display', total.toFixed(2));
}

function updateDisplayElement(id, value) {
    const element = document.getElementById(id);
    if (element) {
        element.textContent = '₹ ' + value;
    }
}

// Form validation enhancement
function initializeFormValidation() {
    const forms = document.querySelectorAll('form');
    
    forms.forEach(function(form) {
        form.addEventListener('submit', function(e) {
            // Add loading state to submit button
            const submitBtn = form.querySelector('button[type="submit"]');
            if (submitBtn) {
                submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Saving...';
                submitBtn.disabled = true;
            }
        });
        
        // Real-time validation
        const inputs = form.querySelectorAll('input, textarea, select');
        inputs.forEach(function(input) {
            input.addEventListener('blur', function() {
                validateField(input);
            });
        });
    });
}

function validateField(field) {
    const value = field.value.trim();
    const isRequired = field.hasAttribute('required');
    
    // Remove existing validation classes
    field.classList.remove('is-valid', 'is-invalid');
    
    if (isRequired && !value) {
        field.classList.add('is-invalid');
        showFieldError(field, 'This field is required');
    } else if (value) {
        field.classList.add('is-valid');
        hideFieldError(field);
    }
    
    // Specific validation rules
    if (field.type === 'email' && value) {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailRegex.test(value)) {
            field.classList.remove('is-valid');
            field.classList.add('is-invalid');
            showFieldError(field, 'Please enter a valid email address');
        }
    }
    
    if (field.type === 'number' && value) {
        if (isNaN(value) || parseFloat(value) < 0) {
            field.classList.remove('is-valid');
            field.classList.add('is-invalid');
            showFieldError(field, 'Please enter a valid positive number');
        }
    }
}

function showFieldError(field, message) {
    hideFieldError(field); // Remove existing error
    
    const errorDiv = document.createElement('div');
    errorDiv.className = 'invalid-feedback';
    errorDiv.textContent = message;
    
    field.parentNode.appendChild(errorDiv);
}

function hideFieldError(field) {
    const existingError = field.parentNode.querySelector('.invalid-feedback');
    if (existingError) {
        existingError.remove();
    }
}

// Utility functions
function showAlert(message, type = 'info') {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-dismissible fade show`;
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    // Insert at the top of the main container
    const main = document.querySelector('main');
    if (main) {
        main.insertBefore(alertDiv, main.firstChild);
        
        // Auto-dismiss after 5 seconds
        setTimeout(function() {
            if (alertDiv.parentNode) {
                alertDiv.remove();
            }
        }, 5000);
    }
}

function formatCurrency(amount) {
    return new Intl.NumberFormat('en-IN', {
        style: 'currency',
        currency: 'INR'
    }).format(amount);
}

function formatDate(date) {
    return new Intl.DateTimeFormat('en-IN', {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
    }).format(new Date(date));
}

// Export functions for global access
window.CARSApp = {
    showAlert,
    formatCurrency,
    formatDate,
    calculateTotals,
    validateField
};