// Bookstore Main JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function(tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Auto-dismiss alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert:not(.alert-permanent)');
    alerts.forEach(function(alert) {
        setTimeout(function() {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });

    // Quantity input controls
    setupQuantityControls();

    // Add to cart AJAX
    setupAddToCart();

    // Confirm delete
    setupConfirmDelete();

    // Search autocomplete placeholder (can be implemented with API)
    setupSearchInput();
});

// Quantity Controls
function setupQuantityControls() {
    document.querySelectorAll('.quantity-control').forEach(function(control) {
        const input = control.querySelector('input[type="number"]');
        const btnMinus = control.querySelector('.btn-minus');
        const btnPlus = control.querySelector('.btn-plus');

        if (btnMinus) {
            btnMinus.addEventListener('click', function() {
                const min = parseInt(input.min) || 1;
                let value = parseInt(input.value) || 1;
                if (value > min) {
                    input.value = value - 1;
                    input.dispatchEvent(new Event('change'));
                }
            });
        }

        if (btnPlus) {
            btnPlus.addEventListener('click', function() {
                const max = parseInt(input.max) || 999;
                let value = parseInt(input.value) || 1;
                if (value < max) {
                    input.value = value + 1;
                    input.dispatchEvent(new Event('change'));
                }
            });
        }
    });
}

// Add to Cart AJAX
function setupAddToCart() {
    document.querySelectorAll('.add-to-cart-ajax').forEach(function(form) {
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const formData = new FormData(form);
            const url = form.action;

            fetch(url, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    // Update cart count in navbar
                    const cartCount = document.querySelector('.cart-count');
                    if (cartCount) {
                        cartCount.textContent = data.cart_count;
                    }
                    
                    // Show success message
                    showToast('Đã thêm vào giỏ hàng!', 'success');
                } else {
                    showToast(data.message || 'Có lỗi xảy ra!', 'error');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                // Fallback to regular form submit
                form.submit();
            });
        });
    });
}

// Confirm Delete
function setupConfirmDelete() {
    document.querySelectorAll('[data-confirm]').forEach(function(element) {
        element.addEventListener('click', function(e) {
            const message = this.dataset.confirm || 'Bạn có chắc chắn muốn thực hiện hành động này?';
            if (!confirm(message)) {
                e.preventDefault();
                return false;
            }
        });
    });
}

// Search Input Enhancement
function setupSearchInput() {
    const searchInput = document.querySelector('input[name="q"]');
    if (searchInput) {
        // Debounce search input
        let timeout;
        searchInput.addEventListener('input', function() {
            clearTimeout(timeout);
            timeout = setTimeout(function() {
                // Could implement live search here
            }, 300);
        });

        // Clear search on Escape
        searchInput.addEventListener('keydown', function(e) {
            if (e.key === 'Escape') {
                this.value = '';
                this.blur();
            }
        });
    }
}

// Toast Notification
function showToast(message, type = 'info') {
    // Create toast container if not exists
    let container = document.querySelector('.toast-container');
    if (!container) {
        container = document.createElement('div');
        container.className = 'toast-container position-fixed bottom-0 end-0 p-3';
        container.style.zIndex = '9999';
        document.body.appendChild(container);
    }

    // Create toast
    const toast = document.createElement('div');
    toast.className = `toast align-items-center text-white bg-${type === 'success' ? 'success' : type === 'error' ? 'danger' : 'primary'} border-0`;
    toast.setAttribute('role', 'alert');
    toast.innerHTML = `
        <div class="d-flex">
            <div class="toast-body">${message}</div>
            <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
        </div>
    `;

    container.appendChild(toast);

    // Show toast
    const bsToast = new bootstrap.Toast(toast, { delay: 3000 });
    bsToast.show();

    // Remove after hidden
    toast.addEventListener('hidden.bs.toast', function() {
        toast.remove();
    });
}

// Format currency
function formatCurrency(amount) {
    return new Intl.NumberFormat('vi-VN', {
        style: 'currency',
        currency: 'VND',
        minimumFractionDigits: 0
    }).format(amount);
}

// Image lazy loading
if ('loading' in HTMLImageElement.prototype) {
    const images = document.querySelectorAll('img[loading="lazy"]');
    images.forEach(img => {
        img.src = img.dataset.src;
    });
} else {
    // Fallback for browsers that don't support lazy loading
    const script = document.createElement('script');
    script.src = 'https://cdnjs.cloudflare.com/ajax/libs/lozad.js/1.16.0/lozad.min.js';
    script.onload = function() {
        const observer = lozad();
        observer.observe();
    };
    document.body.appendChild(script);
}

// Print order
function printOrder() {
    window.print();
}

// Copy to clipboard
function copyToClipboard(text) {
    navigator.clipboard.writeText(text).then(function() {
        showToast('Đã sao chép!', 'success');
    });
}
