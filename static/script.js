/* ========================================
   FOOD DELIVERY PREDICTOR - INTERACTIVE JS
   Professional Animations & Effects
   ======================================== */

// PAGE LOAD ANIMATION
document.addEventListener('DOMContentLoaded', function() {
    // Fade in page
    document.body.style.animation = 'fadeIn 0.8s ease-in';
    
    // Initialize all interactive elements
    initializeForm();
    initializeButtons();
    initializeNavigation();
    initializeInputEffects();
});

// FADE IN ANIMATION
const style = document.createElement('style');
style.textContent = `
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    @keyframes slideIn {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    @keyframes pulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.05); }
    }
    @keyframes shimmer {
        0% { background-position: -1000px 0; }
        100% { background-position: 1000px 0; }
    }
`;
document.head.appendChild(style);

/* ========================================
   FORM HANDLING
   ======================================== */

function initializeForm() {
    const form = document.querySelector('.prediction-form');
    if (!form) return;

    form.addEventListener('submit', function(e) {
        e.preventDefault();
        
        // Validate inputs
        if (!validateForm()) {
            showNotification('Please fill all fields correctly', 'error');
            return;
        }

        // Button animation
        const submitBtn = form.querySelector('.glow-btn');
        submitBtn.style.pointerEvents = 'none';
        submitBtn.innerHTML = '<span class="btn-loader">⏳ Processing...</span>';
        
        // Simulate processing with loader animation
        let dots = 0;
        const loaderInterval = setInterval(() => {
            dots = (dots + 1) % 4;
            submitBtn.innerHTML = '<span class="btn-loader">⏳ Processing' + '.'.repeat(dots) + '</span>';
        }, 300);

        // Submit form after animation
        setTimeout(() => {
            clearInterval(loaderInterval);
            form.submit();
        }, 800);
    });
}

function validateForm() {
    const inputs = document.querySelectorAll('.form-input, .form-select');
    let isValid = true;

    inputs.forEach(input => {
        if (!input.value) {
            isValid = false;
            input.style.borderColor = '#ef4444';
            input.style.animation = 'shake 0.5s ease-in-out';
        } else {
            input.style.borderColor = 'rgba(255, 255, 255, 0.2)';
        }
    });

    return isValid;
}

// Add shake animation
const shakeStyle = document.createElement('style');
shakeStyle.textContent = `
    @keyframes shake {
        0%, 100% { transform: translateX(0); }
        25% { transform: translateX(-10px); }
        75% { transform: translateX(10px); }
    }
`;
document.head.appendChild(shakeStyle);

/* ========================================
   BUTTON INTERACTIONS
   ======================================== */

function initializeButtons() {
    const buttons = document.querySelectorAll('.glow-btn, .btn-glow');
    
    buttons.forEach(btn => {
        // Hover effect
        btn.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-3px) scale(1.05)';
        });

        btn.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0) scale(1)';
        });

        // Click ripple effect
        btn.addEventListener('click', function(e) {
            const rect = this.getBoundingClientRect();
            const ripple = document.createElement('span');
            ripple.style.position = 'absolute';
            ripple.style.borderRadius = '50%';
            ripple.style.background = 'rgba(255, 255, 255, 0.5)';
            ripple.style.width = '20px';
            ripple.style.height = '20px';
            ripple.style.left = (e.clientX - rect.left - 10) + 'px';
            ripple.style.top = (e.clientY - rect.top - 10) + 'px';
            ripple.style.animation = 'ripple 0.6s ease-out';
            ripple.style.pointerEvents = 'none';
            
            this.style.position = 'relative';
            this.style.overflow = 'hidden';
            this.appendChild(ripple);

            setTimeout(() => ripple.remove(), 600);
        });
    });

    // Add ripple animation
    const rippleStyle = document.createElement('style');
    rippleStyle.textContent = `
        @keyframes ripple {
            from {
                width: 20px;
                height: 20px;
                opacity: 0.8;
            }
            to {
                width: 300px;
                height: 300px;
                opacity: 0;
            }
        }
    `;
    document.head.appendChild(rippleStyle);
}

/* ========================================
   INPUT FIELD EFFECTS
   ======================================== */

function initializeInputEffects() {
    const inputs = document.querySelectorAll('.form-input, .form-select');

    inputs.forEach(input => {
        // Focus animation
        input.addEventListener('focus', function() {
            this.parentElement.style.transform = 'scale(1.02)';
            this.style.background = 'rgba(255, 255, 255, 0.12)';
            this.style.borderColor = '#ff6b6b';
            this.style.boxShadow = '0 0 20px rgba(255, 107, 107, 0.3)';
        });

        input.addEventListener('blur', function() {
            this.parentElement.style.transform = 'scale(1)';
            this.style.background = 'rgba(255, 255, 255, 0.08)';
            this.style.borderColor = 'rgba(255, 255, 255, 0.2)';
            this.style.boxShadow = 'none';
        });

        // Input validation feedback
        input.addEventListener('input', function() {
            if (this.value) {
                this.style.borderColor = 'rgba(255, 230, 109, 0.5)';
            }
        });
    });
}

/* ========================================
   NAVIGATION EFFECTS
   ======================================== */

function initializeNavigation() {
    const navLinks = document.querySelectorAll('.nav-link');

    navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            // Remove active class from all links
            navLinks.forEach(l => l.classList.remove('active'));
            // Add active class to clicked link
            this.classList.add('active');
        });
    });

    // Set active link based on current page
    const currentPage = window.location.pathname;
    navLinks.forEach(link => {
        if (link.getAttribute('href') === currentPage) {
            link.classList.add('active');
        }
    });
}

/* ========================================
   NOTIFICATION SYSTEM
   ======================================== */

function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 1rem 1.5rem;
        background: ${type === 'error' ? '#ef4444' : '#22c55e'};
        color: white;
        border-radius: 10px;
        font-weight: 600;
        z-index: 2000;
        animation: slideIn 0.3s ease-out;
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.2);
    `;
    notification.textContent = message;

    document.body.appendChild(notification);

    // Auto remove
    setTimeout(() => {
        notification.style.animation = 'slideOut 0.3s ease-out forwards';
        setTimeout(() => notification.remove(), 300);
    }, 3000);
}

/* ========================================
   TABLE ANIMATIONS (HISTORY PAGE)
   ======================================== */

function animateTableRows() {
    const rows = document.querySelectorAll('.history-table tbody tr');
    rows.forEach((row, index) => {
        row.style.animation = `slideInRow 0.5s ease-out ${index * 0.05}s both`;
    });
}

document.addEventListener('DOMContentLoaded', animateTableRows);

/* ========================================
   FLOATING PARTICLES
   ======================================== */

function createFloatingParticles() {
    const canvas = document.createElement('canvas');
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
    canvas.style.cssText = `
        position: fixed;
        top: 0;
        left: 0;
        z-index: -1;
        pointer-events: none;
    `;

    // Only create if we have a canvas-capable browser
    if (canvas.getContext) {
        // Particles initialization (optional enhancement)
    }
}

/* ========================================
   SMOOTH SCROLLING
   ======================================== */

document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function(e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});

/* ========================================
   PERFORMANCE & OPTIMIZATION
   ======================================== */

// Debounce function for resize events
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Handle window resize
window.addEventListener('resize', debounce(function() {
    // Adjust canvas size or other responsive elements
}, 250));

/* ========================================
   DARK MODE TOGGLE (OPTIONAL)
   ======================================== */

function initializeDarkMode() {
    const prefersDark = window.matchMedia('(prefers-color-scheme: dark)');
    if (prefersDark.matches) {
        document.body.classList.add('dark-mode');
    }
}

initializeDarkMode();

/* ========================================
   SUCCESS ANIMATIONS
   ======================================== */

// Confetti effect on prediction success (optional)
function launchConfetti() {
    const confettiPieces = 50;
    const container = document.querySelector('.result-card') || document.body;

    for (let i = 0; i < confettiPieces; i++) {
        const confetti = document.createElement('div');
        confetti.innerHTML = ['🎉', '✨', '⭐', '🌟', '💫'][Math.floor(Math.random() * 5)];
        confetti.style.cssText = `
            position: fixed;
            left: ${Math.random() * 100}%;
            top: -10px;
            font-size: 1.5rem;
            animation: fall ${2 + Math.random() * 2}s linear forwards;
            pointer-events: none;
            z-index: 1000;
        `;
        document.body.appendChild(confetti);

        setTimeout(() => confetti.remove(), 5000);
    }
}

// Add fall animation
const fallStyle = document.createElement('style');
fallStyle.textContent = `
    @keyframes fall {
        to {
            transform: translateY(100vh) rotate(360deg);
            opacity: 0;
        }
    }
    @keyframes slideOut {
        to {
            transform: translateX(400px);
            opacity: 0;
        }
    }
`;
document.head.appendChild(fallStyle);

// Trigger confetti on result page load
if (document.querySelector('.result-card')) {
    window.addEventListener('load', launchConfetti);
}