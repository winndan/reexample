// ===== DOM Elements =====
const filtersSidebar = document.getElementById('filtersSidebar');
const filterToggleBtn = document.getElementById('filterToggleBtn');
const filtersClose = document.getElementById('filtersClose');
const filtersForm = document.getElementById('filtersForm');
const resetFilters = document.getElementById('resetFilters');
const viewBtns = document.querySelectorAll('.view-btn');
const propertyGrid = document.getElementById('propertyGrid');
const favoriteBtns = document.querySelectorAll('.favorite-btn');
const sortSelect = document.getElementById('sortSelect');
const pageNumbers = document.querySelectorAll('.page-number');
const paginationBtns = document.querySelectorAll('.pagination-btn');

// ===== Filters Sidebar Toggle =====
const overlay = document.createElement('div');
overlay.className = 'filters-overlay';
document.body.appendChild(overlay);

function openFilters() {
    if (!filtersSidebar) return;
    filtersSidebar.classList.add('active');
    overlay.classList.add('active');
    document.body.style.overflow = 'hidden';
}

function closeFilters() {
    if (!filtersSidebar) return;
    filtersSidebar.classList.remove('active');
    overlay.classList.remove('active');
    document.body.style.overflow = '';
}

if (filterToggleBtn) {
    filterToggleBtn.addEventListener('click', openFilters);
}

if (filtersClose) {
    filtersClose.addEventListener('click', closeFilters);
}

overlay.addEventListener('click', closeFilters);

document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
        closeFilters();
    }
});

// ===== View Toggle (Grid/List) =====
viewBtns.forEach(btn => {
    btn.addEventListener('click', () => {
        viewBtns.forEach(b => b.classList.remove('active'));
        btn.classList.add('active');

        const view = btn.dataset.view;
        if (view === 'list') {
            propertyGrid.classList.add('list-view');
        } else {
            propertyGrid.classList.remove('list-view');
        }
    });
});

// ===== Favorite Button Toggle =====
favoriteBtns.forEach(btn => {
    btn.addEventListener('click', (e) => {
        e.preventDefault();
        e.stopPropagation();
        btn.classList.toggle('active');

        const card = btn.closest('.property-card');
        const propertyId = card.dataset.id;

        if (btn.classList.contains('active')) {
            saveFavorite(propertyId);
        } else {
            removeFavorite(propertyId);
        }
    });
});

// ===== Favorites Management =====
function getFavorites() {
    const favorites = localStorage.getItem('leaseFavorites');
    return favorites ? JSON.parse(favorites) : [];
}

function saveFavorite(propertyId) {
    const favorites = getFavorites();
    if (!favorites.includes(propertyId)) {
        favorites.push(propertyId);
        localStorage.setItem('leaseFavorites', JSON.stringify(favorites));
    }
}

function removeFavorite(propertyId) {
    const favorites = getFavorites();
    const index = favorites.indexOf(propertyId);
    if (index > -1) {
        favorites.splice(index, 1);
        localStorage.setItem('leaseFavorites', JSON.stringify(favorites));
    }
}

function loadFavorites() {
    const favorites = getFavorites();
    document.querySelectorAll('.property-card').forEach(card => {
        const propertyId = card.dataset.id;
        const btn = card.querySelector('.favorite-btn');
        if (favorites.includes(propertyId) && btn) {
            btn.classList.add('active');
        }
    });
}

loadFavorites();

// ===== Filter Form Handling =====
if (filtersForm) {
    filtersForm.addEventListener('submit', (e) => {
        e.preventDefault();
        filterProperties();
        closeFilters();
    });
}

if (resetFilters) {
    resetFilters.addEventListener('click', () => {
        filtersForm.reset();
        document.querySelectorAll('.checkbox-item input').forEach(input => {
            input.checked = false;
        });
        document.querySelectorAll('.property-card').forEach(card => {
            card.style.display = '';
        });
        updateListingsCount();
        if (window.location.search) {
            window.history.replaceState({}, '', window.location.pathname);
        }
    });
}

function filterProperties() {
    const location = (document.getElementById('locationInput')?.value || '').toLowerCase().trim();
    const minPrice = parseInt(document.getElementById('minPrice')?.value || '0') || 0;
    const maxPrice = parseInt(document.getElementById('maxPrice')?.value || '0') || 0;
    const bedrooms = Array.from(document.querySelectorAll('input[name="bedrooms"]:checked')).map(cb => cb.value);

    showLoadingState();

    const cards = document.querySelectorAll('.property-card');
    cards.forEach(card => {
        let show = true;
        const cardLocation = (card.dataset.location || '').toLowerCase();
        const cardPrice = parseInt(card.dataset.price || '0');
        const cardBeds = card.dataset.beds || '0';

        if (location && !cardLocation.includes(location)) {
            show = false;
        }

        if (minPrice && cardPrice < minPrice) show = false;
        if (maxPrice && cardPrice > maxPrice) show = false;

        if (bedrooms.length > 0) {
            const isStudioChecked = bedrooms.includes('Studio');
            const isCardStudio = cardBeds.toLowerCase() === 'studio';
            const numericBeds = bedrooms.filter(b => b !== 'Studio').map(b => b === '4+' ? 4 : parseInt(b) || 0);
            const minBed = numericBeds.length > 0 ? Math.min(...numericBeds) : Infinity;
            const bedNum = parseInt(cardBeds) || 0;

            let matches = false;
            if (isStudioChecked && isCardStudio) matches = true;
            if (numericBeds.length > 0 && bedNum >= minBed) matches = true;
            if (!matches) show = false;
        }

        card.style.display = show ? '' : 'none';
    });

    setTimeout(() => {
        hideLoadingState();
        updateListingsCount();
    }, 300);
}

function showLoadingState() {
    propertyGrid.style.opacity = '0.5';
    propertyGrid.style.pointerEvents = 'none';
}

function hideLoadingState() {
    propertyGrid.style.opacity = '1';
    propertyGrid.style.pointerEvents = 'auto';
}

function updateListingsCount() {
    const count = document.querySelectorAll('.property-card:not([style*="display: none"])').length;
    const countEl = document.getElementById('listingsCount');
    if (countEl) {
        countEl.textContent = count;
    }
}

// ===== Read URL params and pre-fill filters =====
function applyUrlFilters() {
    const params = new URLSearchParams(window.location.search);
    const location = params.get('location') || '';
    const minPriceParam = params.get('minPrice') || '';
    const maxPriceParam = params.get('maxPrice') || '';
    const beds = params.get('beds') || '';

    let hasFilters = false;

    if (location) {
        const el = document.getElementById('locationInput');
        if (el) { el.value = location; hasFilters = true; }
    }

    if (minPriceParam) {
        const el = document.getElementById('minPrice');
        if (el) { el.value = minPriceParam; hasFilters = true; }
    }

    if (maxPriceParam) {
        const el = document.getElementById('maxPrice');
        if (el) { el.value = maxPriceParam; hasFilters = true; }
    }

    if (beds) {
        if (beds === 'studio') {
            document.querySelectorAll('input[name="bedrooms"]').forEach(cb => {
                if (cb.value === 'Studio') {
                    cb.checked = true;
                    hasFilters = true;
                }
            });
        } else {
            const bedNum = parseInt(beds);
            if (bedNum) {
                document.querySelectorAll('input[name="bedrooms"]').forEach(cb => {
                    const cbVal = cb.value === '4+' ? 4 : parseInt(cb.value);
                    if (!isNaN(cbVal) && cbVal >= bedNum) {
                        cb.checked = true;
                        hasFilters = true;
                    }
                });
            }
        }
    }

    if (hasFilters) {
        filterProperties();
    }
}

// ===== Sort Functionality =====
if (sortSelect) {
    sortSelect.addEventListener('change', () => {
        sortProperties(sortSelect.value);
    });
}

function sortProperties(sortBy) {
    const cards = Array.from(document.querySelectorAll('.property-card'));

    cards.sort((a, b) => {
        const priceA = parseInt(a.querySelector('.property-price')?.textContent.replace(/[^0-9]/g, '') || 0);
        const priceB = parseInt(b.querySelector('.property-price')?.textContent.replace(/[^0-9]/g, '') || 0);

        switch (sortBy) {
            case 'price-low':
                return priceA - priceB;
            case 'price-high':
                return priceB - priceA;
            case 'newest':
            default:
                return 0;
        }
    });

    cards.forEach(card => propertyGrid.appendChild(card));
}

// ===== Pagination =====
pageNumbers.forEach(btn => {
    btn.addEventListener('click', () => {
        pageNumbers.forEach(b => b.classList.remove('active'));
        btn.classList.add('active');

        document.querySelector('.listings-main').scrollIntoView({ behavior: 'smooth' });
        loadPage(btn.textContent);
    });
});

paginationBtns.forEach(btn => {
    btn.addEventListener('click', () => {
        if (btn.disabled) return;

        const currentPage = document.querySelector('.page-number.active');
        const currentIndex = Array.from(pageNumbers).indexOf(currentPage);

        if (btn.classList.contains('prev') && currentIndex > 0) {
            pageNumbers[currentIndex].classList.remove('active');
            pageNumbers[currentIndex - 1].classList.add('active');
            updatePaginationButtons();
        } else if (btn.classList.contains('next') && currentIndex < pageNumbers.length - 1) {
            pageNumbers[currentIndex].classList.remove('active');
            pageNumbers[currentIndex + 1].classList.add('active');
            updatePaginationButtons();
        }

        document.querySelector('.listings-main').scrollIntoView({ behavior: 'smooth' });
    });
});

function updatePaginationButtons() {
    const currentPage = document.querySelector('.page-number.active');
    const currentIndex = Array.from(pageNumbers).indexOf(currentPage);

    const prevBtn = document.querySelector('.pagination-btn.prev');
    const nextBtn = document.querySelector('.pagination-btn.next');

    if (prevBtn) prevBtn.disabled = currentIndex === 0;
    if (nextBtn) nextBtn.disabled = currentIndex === pageNumbers.length - 1;
}

function loadPage(page) {
    showLoadingState();
    setTimeout(() => {
        hideLoadingState();
        console.log('Loaded page:', page);
    }, 500);
}

// ===== Toast Notification =====
function showToast(message) {
    const existingToast = document.querySelector('.toast-notification');
    if (existingToast) existingToast.remove();

    const toast = document.createElement('div');
    toast.className = 'toast-notification';
    toast.textContent = message;
    toast.style.cssText = `
        position: fixed;
        bottom: 24px;
        left: 50%;
        transform: translateX(-50%);
        background: var(--color-primary, #8b6914);
        color: #fff;
        padding: 12px 24px;
        border-radius: 8px;
        font-size: 14px;
        font-weight: 500;
        z-index: 9999;
        animation: slideUp 0.3s ease;
    `;

    document.body.appendChild(toast);
    setTimeout(() => {
        toast.style.animation = 'slideDown 0.3s ease';
        setTimeout(() => toast.remove(), 300);
    }, 3000);
}

const toastStyles = document.createElement('style');
toastStyles.textContent = `
    @keyframes slideUp {
        from { opacity: 0; transform: translate(-50%, 20px); }
        to { opacity: 1; transform: translate(-50%, 0); }
    }
    @keyframes slideDown {
        from { opacity: 1; transform: translate(-50%, 0); }
        to { opacity: 0; transform: translate(-50%, 20px); }
    }
`;
document.head.appendChild(toastStyles);

// ===== Lazy Loading Images =====
if ('IntersectionObserver' in window) {
    const imageObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                if (img.dataset.src) {
                    img.src = img.dataset.src;
                    img.removeAttribute('data-src');
                }
                observer.unobserve(img);
            }
        });
    }, { rootMargin: '50px' });

    document.querySelectorAll('img[data-src]').forEach(img => {
        imageObserver.observe(img);
    });
}

// ===== Initialize =====
document.addEventListener('DOMContentLoaded', () => {
    updatePaginationButtons();
    updateListingsCount();
    applyUrlFilters();
});
