function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        document.cookie.split(';').forEach(cookie => {
            const c = cookie.trim();
            if (c.startsWith(name + '=')) {
                cookieValue = decodeURIComponent(c.slice(name.length + 1));
            }
        });
    }
    return cookieValue;
}
const CSRF = getCookie('csrftoken');

function showToast(message, type = 'success') {
    document.querySelectorAll('.qm-toast').forEach(t => t.remove());

    const bg = type === 'success' ? '#22c55e' : type === 'error' ? '#ef4444' : '#f59e0b';
    const icon = type === 'success' ? '✅' : type === 'error' ? '❌' : '⚠️';

    const toast = document.createElement('div');
    toast.className = 'qm-toast';
    toast.style.cssText = `
        position:fixed; bottom:24px; left:50%; transform:translateX(-50%) translateY(80px);
        background:${bg}; color:white; padding:12px 24px; border-radius:50px;
        font-weight:700; font-size:14px; z-index:99999; transition:transform .4s cubic-bezier(.34,1.56,.64,1);
        box-shadow:0 8px 32px rgba(0,0,0,.2); white-space:nowrap; max-width:90vw;
    `;
    toast.innerHTML = `${icon} ${message}`;
    document.body.appendChild(toast);

    requestAnimationFrame(() => {
        toast.style.transform = 'translateX(-50%) translateY(0)';
    });

    setTimeout(() => {
        toast.style.transform = 'translateX(-50%) translateY(80px)';
        setTimeout(() => toast.remove(), 400);
    }, 3000);
}

function updateCartBadge(count, total) {
    const badge = document.getElementById('cartBadge');
    if (badge) {
        badge.textContent = count;
        badge.classList.remove('pulse');
        void badge.offsetWidth;
        badge.classList.add('pulse');
    }
    const cartBtn = document.querySelector('.cart-btn span:last-child');
    if (cartBtn && total !== undefined) {
        cartBtn.textContent = `₹${Math.round(total)}`;
    }
}

function addToCart(productId, btn) {
    if (btn) {
        btn.disabled = true;
        btn.innerHTML = '<span class="spinner-border spinner-border-sm"></span>';
    }

    const form = new FormData();
    form.append('quantity', 1);

    fetch(`/cart/add/${productId}/`, {
        method: 'POST',
        headers: { 'X-CSRFToken': CSRF, 'X-Requested-With': 'XMLHttpRequest' },
        body: form,
    })
    .then(r => r.json())
    .then(data => {
        if (data.success) {
            updateCartBadge(data.cart_count, data.cart_total);
            showToast(data.message || 'Added to cart! 🛒');
            if (btn) {
                const card = btn.closest('.product-card');
                if (card) {
                    btn.outerHTML = `
                        <div class="qty-control" id="qty-${productId}">
                            <button class="qty-btn qty-minus" onclick="updateQtyFromCard(${productId}, -1)">−</button>
                            <span class="qty-value" id="qty-val-${productId}">1</span>
                            <button class="qty-btn qty-plus" onclick="updateQtyFromCard(${productId}, 1)">+</button>
                        </div>`;
                }
            }
        }
    })
    .catch(() => {
        showToast('Error! Please try again.', 'error');
        if (btn) { btn.disabled = false; btn.innerHTML = '<i class="bi bi-plus-lg"></i> Add'; }
    });
}

function updateQtyFromCard(productId, delta) {
    const qtySpan = document.getElementById(`qty-val-${productId}`);
    if (!qtySpan) return;

    let currentQty = parseInt(qtySpan.textContent) || 1;
    let newQty = currentQty + delta;

    if (newQty <= 0) {
        showToast('Item removed from cart', 'warning');
        const qtyControl = document.getElementById(`qty-${productId}`);
        if (qtyControl) {
            qtyControl.outerHTML = `<button class="add-to-cart-btn" onclick="addToCart(${productId}, this)"><i class="bi bi-plus-lg"></i> Add</button>`;
        }
        updateCartBadge(Math.max(0, (parseInt(document.getElementById('cartBadge')?.textContent) || 1) - 1));
        return;
    }

    qtySpan.textContent = newQty;
    const form = new FormData();
    form.append('quantity', delta > 0 ? 1 : -1);
    fetch(`/cart/add/${productId}/`, {
        method: 'POST',
        headers: { 'X-CSRFToken': CSRF, 'X-Requested-With': 'XMLHttpRequest' },
        body: form,
    })
    .then(r => r.json())
    .then(data => { if (data.success) updateCartBadge(data.cart_count, data.cart_total); });
}

function updateCartItem(itemId, delta) {
    const input = document.getElementById(`item-qty-${itemId}`);
    if (!input) return;
    let newQty = parseInt(input.value) + delta;
    if (newQty < 1) newQty = 1;
    input.value = newQty;
    sendCartUpdate(itemId, newQty);
}

function sendCartUpdate(itemId, quantity) {
    const form = new FormData();
    form.append('quantity', quantity);

    fetch(`/cart/update/${itemId}/`, {
        method: 'POST',
        headers: { 'X-CSRFToken': CSRF, 'X-Requested-With': 'XMLHttpRequest' },
        body: form,
    })
    .then(r => r.json())
    .then(data => {
        if (data.success) {
            updateCartBadge(data.cart_count, data.cart_total);
            const itemTotal = document.getElementById(`item-total-${itemId}`);
            if (itemTotal) itemTotal.textContent = `₹${data.item_total}`;
            updateCartSummary(data.subtotal, data.delivery_fee, data.cart_total);
        }
    });
}

function updateCartSummary(subtotal, delivery, total) {
    const els = {
        subtotal: document.getElementById('cart-subtotal'),
        delivery: document.getElementById('cart-delivery'),
        total: document.getElementById('cart-total'),
        freeMsg: document.getElementById('free-delivery-msg'),
    };
    if (els.subtotal) els.subtotal.textContent = `₹${parseFloat(subtotal).toFixed(0)}`;
    if (els.delivery) {
        els.delivery.textContent = parseFloat(delivery) === 0 ? 'FREE' : `₹${parseFloat(delivery).toFixed(0)}`;
        els.delivery.className = parseFloat(delivery) === 0 ? 'fw-700 text-success' : 'fw-700';
    }
    if (els.total) els.total.textContent = `₹${parseFloat(total).toFixed(0)}`;
    if (els.freeMsg) {
        const remaining = 199 - parseFloat(subtotal);
        if (remaining > 0) {
            els.freeMsg.innerHTML = `<i class="bi bi-truck"></i> Add <strong>₹${Math.ceil(remaining)}</strong> more for FREE delivery`;
            els.freeMsg.className = 'free-delivery-msg';
        } else {
            els.freeMsg.innerHTML = `<i class="bi bi-truck-front-fill"></i> 🎉 You've got FREE delivery!`;
            els.freeMsg.className = 'free-delivery-msg success';
        }
    }
}

function removeCartItem(itemId) {
    if (!confirm('Remove this item from cart?')) return;
    const form = new FormData();

    fetch(`/cart/remove/${itemId}/`, {
        method: 'POST',
        headers: { 'X-CSRFToken': CSRF, 'X-Requested-With': 'XMLHttpRequest' },
        body: form,
    })
    .then(r => r.json())
    .then(data => {
        if (data.success) {
            const row = document.getElementById(`cart-item-${itemId}`);
            if (row) {
                row.style.transition = 'opacity .3s, transform .3s';
                row.style.opacity = '0';
                row.style.transform = 'translateX(-20px)';
                setTimeout(() => {
                    row.remove();
                    if (data.cart_count === 0) location.reload();
                }, 300);
            }
            updateCartBadge(data.cart_count, data.cart_total);
            updateCartSummary(data.subtotal, data.delivery_fee, data.cart_total);
            showToast('Item removed from cart');
        }
    });
}

function toggleWishlist(productId, btn) {
    fetch(`/wishlist/toggle/${productId}/`, {
        method: 'POST',
        headers: { 'X-CSRFToken': CSRF, 'X-Requested-With': 'XMLHttpRequest' },
    })
    .then(r => r.json())
    .then(data => {
        if (data.success) {
            const icon = btn.querySelector('i');
            if (data.in_wishlist) {
                icon.className = 'bi bi-heart-fill text-danger';
            } else {
                icon.className = 'bi bi-heart';
            }
            showToast(data.message);
        }
    })
    .catch(() => { window.location.href = '/login/'; });
}

function initSearch() {
    const inputs = document.querySelectorAll('#globalSearch, .search-input');
    inputs.forEach(input => {
        let timer;
        const dropdown = input.parentElement.querySelector('.search-results-dropdown') || document.getElementById('searchDropdown');

        input.addEventListener('input', () => {
            clearTimeout(timer);
            const query = input.value.trim();
            if (query.length < 2) {
                if (dropdown) dropdown.innerHTML = '';
                return;
            }
            timer = setTimeout(() => {
                fetch(`/api/search/?q=${encodeURIComponent(query)}`)
                .then(r => r.json())
                .then(data => {
                    if (!dropdown) return;
                    if (data.results.length === 0) {
                        dropdown.innerHTML = '<div class="search-no-result">No results found</div>';
                    } else {
                        dropdown.innerHTML = data.results.map(p => `
                            <a href="/products/${p.slug}/" class="search-result-item">
                                <div class="search-result-name">${p.name}</div>
                                <div class="search-result-meta">
                                    <span class="text-muted small">${p.category}</span>
                                    <span class="fw-700 text-success">₹${p.price}</span>
                                </div>
                            </a>
                        `).join('');
                    }
                    dropdown.style.display = 'block';
                });
            }, 300);
        });

        input.addEventListener('keydown', e => {
            if (e.key === 'Enter' && input.value.trim()) {
                window.location.href = `/products/?q=${encodeURIComponent(input.value.trim())}`;
            }
        });

        document.addEventListener('click', e => {
            if (!input.contains(e.target) && dropdown && !dropdown.contains(e.target)) {
                dropdown.style.display = 'none';
            }
        });
    });
}

function initToasts() {
    document.querySelectorAll('.toast').forEach(el => {
        const toast = new bootstrap.Toast(el, { delay: 4000 });
        toast.show();
    });
}

function initNavbar() {
    window.addEventListener('scroll', () => {
        const nav = document.getElementById('mainNav');
        if (nav) nav.classList.toggle('scrolled', window.scrollY > 10);
    });
}

function initDetailQty() {
    const minusBtn = document.getElementById('detailMinus');
    const plusBtn = document.getElementById('detailPlus');
    const qtyInput = document.getElementById('detailQty');
    if (!qtyInput) return;

    minusBtn?.addEventListener('click', () => {
        let v = parseInt(qtyInput.value);
        if (v > 1) qtyInput.value = v - 1;
    });
    plusBtn?.addEventListener('click', () => {
        let v = parseInt(qtyInput.value);
        qtyInput.value = v + 1;
    });
}

function initImageZoom() {
    const mainImg = document.getElementById('mainProductImg');
    if (!mainImg) return;
    mainImg.addEventListener('mousemove', e => {
        const rect = mainImg.getBoundingClientRect();
        const x = ((e.clientX - rect.left) / rect.width) * 100;
        const y = ((e.clientY - rect.top) / rect.height) * 100;
        mainImg.style.transformOrigin = `${x}% ${y}%`;
        mainImg.style.transform = 'scale(1.4)';
    });
    mainImg.addEventListener('mouseleave', () => {
        mainImg.style.transform = 'scale(1)';
    });
}

function initScrollAnimations() {
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
                observer.unobserve(entry.target);
            }
        });
    }, { threshold: 0.1 });

    document.querySelectorAll('.product-card, .category-card, .why-icon').forEach(el => {
        el.classList.add('fade-in-up');
        observer.observe(el);
    });
}

document.addEventListener('DOMContentLoaded', () => {
    initSearch();
    initToasts();
    initNavbar();
    initDetailQty();
    initImageZoom();
    initScrollAnimations();
});

function togglePassword(fieldId, btn) {
    const field = document.getElementById(fieldId);
    if (!field) return;
    if (field.type === 'password') {
        field.type = 'text';
        btn.innerHTML = '<i class="bi bi-eye-slash"></i>';
    } else {
        field.type = 'password';
        btn.innerHTML = '<i class="bi bi-eye"></i>';
    }
}
