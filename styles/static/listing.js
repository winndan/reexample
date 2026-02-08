// ===== DOM Elements =====

const nav = document.getElementById('nav');
const mobileMenuToggle = document.getElementById('mobileMenuToggle');
const filtersSidebar = document.getElementById('filtersSidebar');
const filterToggleBtn = document.getElementById('filterToggleBtn');
const filtersClose = document.getElementById('filtersClose');
const filtersForm = document.getElementById('filtersForm');
const resetFilters = document.getElementById('resetFilters');
const searchTabs = document.querySelectorAll('.search-tab');
const viewBtns = document.querySelectorAll('.view-btn');
const propertyGrid = document.getElementById('propertyGrid');
const favoriteBtns = document.querySelectorAll('.favorite-btn');
const sortSelect = document.getElementById('sortSelect');
const pageNumbers = document.querySelectorAll('.page-number');
const paginationBtns = document.querySelectorAll('.pagination-btn');

// ===== Mobile Menu Toggle =====
if (mobileMenuToggle && nav) {
    mobileMenuToggle.addEventListener('click', () => {
        mobileMenuToggle.classList.toggle('active');
        nav.classList.toggle('active');
    });
}






// ===== Filters Sidebar Toggle =====
// Create overlay element
const overlay = document.createElement('div');
overlay.className = 'filters-overlay';
document.body.appendChild(overlay);

function openFilters() {
  if (!filtersSidebar) return;

  // Close navbar if open
  nav?.classList.remove('active');
  mobileMenuToggle?.classList.remove('active');

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

// Close on escape key
document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
        closeFilters();
    }
});

// ===== Search Tabs =====
searchTabs.forEach(tab => {
    tab.addEventListener('click', () => {
        searchTabs.forEach(t => t.classList.remove('active'));
        tab.classList.add('active');
        
        // Update active tab styling
        const tabType = tab.dataset.tab;
        console.log('Selected tab:', tabType);
        
        // Here you would typically filter properties based on tab
        filterProperties();
    });
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
            console.log('Added to favorites:', propertyId);
            // Here you would save to localStorage or send to server
            saveFavorite(propertyId);
        } else {
            console.log('Removed from favorites:', propertyId);
            removeFavorite(propertyId);
        }
    });
});

// ===== Favorites Management =====
function getFavorites() {
    const favorites = localStorage.getItem('propertyFavorites');
    return favorites ? JSON.parse(favorites) : [];
}

function saveFavorite(propertyId) {
    const favorites = getFavorites();
    if (!favorites.includes(propertyId)) {
        favorites.push(propertyId);
        localStorage.setItem('propertyFavorites', JSON.stringify(favorites));
    }
}

function removeFavorite(propertyId) {
    const favorites = getFavorites();
    const index = favorites.indexOf(propertyId);
    if (index > -1) {
        favorites.splice(index, 1);
        localStorage.setItem('propertyFavorites', JSON.stringify(favorites));
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

// Load favorites on page load
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
        // Reset checkbox styling
        document.querySelectorAll('.checkbox-item input, .amenity-item input').forEach(input => {
            input.checked = false;
        });
        filterProperties();
    });
}

function filterProperties() {
    // Get filter values
    const filters = {
        location: document.getElementById('locationInput')?.value || '',
        propertyType: document.getElementById('propertyType')?.value || '',
        minPrice: document.getElementById('minPrice')?.value || '',
        maxPrice: document.getElementById('maxPrice')?.value || '',
        status: document.getElementById('propertyStatus')?.value || '',
        furnishing: document.getElementById('furnishing')?.value || '',
        bedrooms: Array.from(document.querySelectorAll('input[name="bedrooms"]:checked')).map(cb => cb.value),
        bathrooms: Array.from(document.querySelectorAll('input[name="bathrooms"]:checked')).map(cb => cb.value),
        amenities: Array.from(document.querySelectorAll('input[name="amenities"]:checked')).map(cb => cb.value),
        tab: document.querySelector('.search-tab.active')?.dataset.tab || 'for-lease'
    };
    
    console.log('Applied filters:', filters);
    
    // Here you would typically send these filters to a server
    // or filter client-side if all data is loaded
    
    // For demo, show a loading state
    showLoadingState();
    
    // Simulate API call
    setTimeout(() => {
        hideLoadingState();
        updateListingsCount();
    }, 500);
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
    const count = document.querySelectorAll('.property-card').length;
    const countEl = document.getElementById('listingsCount');
    if (countEl) {
        countEl.textContent = count;
    }
}

// ===== Sort Functionality =====
if (sortSelect) {
    sortSelect.addEventListener('change', () => {
        const sortBy = sortSelect.value;
        console.log('Sorting by:', sortBy);
        
        // Here you would implement sorting logic
        sortProperties(sortBy);
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
                return 0; // Keep original order for demo
        }
    });
    
    // Re-append sorted cards
    cards.forEach(card => propertyGrid.appendChild(card));
}

// ===== Pagination =====
pageNumbers.forEach(btn => {
    btn.addEventListener('click', () => {
        pageNumbers.forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        
        const page = btn.textContent;
        console.log('Go to page:', page);
        
        // Scroll to top of listings
        document.querySelector('.listings-main').scrollIntoView({ behavior: 'smooth' });
        
        // Here you would load the corresponding page
        loadPage(page);
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
        
        // Scroll to top
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
    
    // Simulate page load
    setTimeout(() => {
        hideLoadingState();
        console.log('Loaded page:', page);
    }, 500);
}

// ===== Share Button Functionality =====
document.querySelectorAll('.share-btn').forEach(btn => {
    btn.addEventListener('click', (e) => {
        e.preventDefault();
        e.stopPropagation();
        
        const card = btn.closest('.property-card');
        const title = card.querySelector('.property-title a')?.textContent || 'Property';
        const url = window.location.href;
        
        if (navigator.share) {
            navigator.share({
                title: title,
                url: url
            }).catch(console.error);
        } else {
            // Fallback: copy to clipboard
            navigator.clipboard.writeText(url).then(() => {
                showToast('Link copied to clipboard!');
            }).catch(console.error);
        }
    });
});

// ===== Compare Button Functionality =====
const compareList = [];

document.querySelectorAll('.compare-btn').forEach(btn => {
    btn.addEventListener('click', (e) => {
        e.preventDefault();
        e.stopPropagation();
        
        const card = btn.closest('.property-card');
        const propertyId = card.dataset.id;
        
        if (compareList.includes(propertyId)) {
            // Remove from compare
            const index = compareList.indexOf(propertyId);
            compareList.splice(index, 1);
            btn.classList.remove('active');
            showToast('Removed from comparison');
        } else {
            if (compareList.length >= 4) {
                showToast('Maximum 4 properties can be compared');
                return;
            }
            compareList.push(propertyId);
            btn.classList.add('active');
            showToast('Added to comparison');
        }
        
        console.log('Compare list:', compareList);
    });
});

// ===== Toast Notification =====
function showToast(message) {
    // Remove existing toast
    const existingToast = document.querySelector('.toast-notification');
    if (existingToast) {
        existingToast.remove();
    }
    
    // Create toast
    const toast = document.createElement('div');
    toast.className = 'toast-notification';
    toast.textContent = message;
    toast.style.cssText = `
        position: fixed;
        bottom: 24px;
        left: 50%;
        transform: translateX(-50%);
        background: var(--color-primary, #c1a162);
        color: #000;
        padding: 12px 24px;
        border-radius: 8px;
        font-size: 14px;
        font-weight: 500;
        z-index: 9999;
        animation: slideUp 0.3s ease;
    `;
    
    document.body.appendChild(toast);
    
    // Remove after 3 seconds
    setTimeout(() => {
        toast.style.animation = 'slideDown 0.3s ease';
        setTimeout(() => toast.remove(), 300);
    }, 3000);
}

// Add toast animation styles
const toastStyles = document.createElement('style');
toastStyles.textContent = `
    @keyframes slideUp {
        from {
            opacity: 0;
            transform: translate(-50%, 20px);
        }
        to {
            opacity: 1;
            transform: translate(-50%, 0);
        }
    }
    @keyframes slideDown {
        from {
            opacity: 1;
            transform: translate(-50%, 0);
        }
        to {
            opacity: 0;
            transform: translate(-50%, 20px);
        }
    }
`;
document.head.appendChild(toastStyles);

// ===== Smooth Scroll for Navigation =====
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        const href = this.getAttribute('href');
        if (href === '#') return;
        
        e.preventDefault();
        const target = document.querySelector(href);
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});

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
    }, {
        rootMargin: '50px'
    });
    
    document.querySelectorAll('img[data-src]').forEach(img => {
        imageObserver.observe(img);
    });
}

// ===== Initialize =====
document.addEventListener('DOMContentLoaded', () => {
    updatePaginationButtons();
    updateListingsCount();
});

