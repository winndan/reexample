// ===== DOM ELEMENTS =====
const searchTabs = document.querySelectorAll('.search-tab');
const favoriteButtons = document.querySelectorAll('.property-favorite');
const testimonialTrack = document.querySelector('.testimonials-track');
const testimonialDots = document.querySelectorAll('.testimonial-dot');
const statNumbers = document.querySelectorAll('.stat-number');
const contactForm = document.querySelector('.contact-form');
const searchForm = document.querySelector('.search-form');

// ===== PRICE OPTIONS PER TAB =====
const buyPriceOptions = [
  { label: 'Any Price', value: '' },
  { label: 'Under $15M', value: '0-15000000' },
  { label: '$15M - $25M', value: '15000000-25000000' },
  { label: '$25M - $50M', value: '25000000-50000000' },
  { label: '$50M+', value: '50000000' },
];

const rentPriceOptions = [
  { label: 'Any Price', value: '' },
  { label: 'Under $50K/mo', value: '0-50000' },
  { label: '$50K - $100K/mo', value: '50000-100000' },
  { label: '$100K - $200K/mo', value: '100000-200000' },
  { label: '$200K+/mo', value: '200000' },
];

function updatePriceOptions(tabText) {
  const priceSelect = document.getElementById('price-range');
  if (!priceSelect) return;
  const options = tabText === 'rent' ? rentPriceOptions : buyPriceOptions;
  priceSelect.innerHTML = '';
  options.forEach(opt => {
    const o = document.createElement('option');
    o.value = opt.value;
    o.textContent = opt.label;
    priceSelect.appendChild(o);
  });
}

// ===== SEARCH TABS =====
searchTabs.forEach(tab => {
  tab.addEventListener('click', () => {
    searchTabs.forEach(t => t.classList.remove('active'));
    tab.classList.add('active');
    updatePriceOptions(tab.textContent.toLowerCase());
  });
});

// ===== PROPERTY FAVORITES =====
favoriteButtons.forEach(button => {
  button.addEventListener('click', (e) => {
    e.preventDefault();
    e.stopPropagation();
    button.classList.toggle('active');
  });
});

// ===== ANIMATED STATS COUNTER =====
function animateCounter(element, target, duration = 2000) {
  let start = 0;
  const increment = target / (duration / 16);

  function updateCounter() {
    start += increment;
    if (start < target) {
      element.textContent = Math.floor(start).toLocaleString() + '+';
      requestAnimationFrame(updateCounter);
    } else {
      element.textContent = target.toLocaleString() + '+';
    }
  }

  updateCounter();
}

let statsAnimated = false;

function checkStatsVisibility() {
  const statsSection = document.querySelector('.stats');
  if (!statsSection || statsAnimated) return;

  const rect = statsSection.getBoundingClientRect();
  if (rect.top < window.innerHeight && rect.bottom > 0) {
    statsAnimated = true;
    statNumbers.forEach(stat => {
      const target = parseInt(stat.dataset.target || '0', 10);
      animateCounter(stat, target);
    });
  }
}

window.addEventListener('scroll', checkStatsVisibility);
window.addEventListener('load', checkStatsVisibility);

// ===== TESTIMONIALS SLIDER =====
let currentTestimonial = 0;
const testimonialCards = document.querySelectorAll('.testimonial-card');
const totalTestimonials = testimonialCards.length;

function updateTestimonialSlider() {
  if (!testimonialTrack) return;

  testimonialTrack.style.transform =
    `translateX(-${currentTestimonial * 100}%)`;

  testimonialDots.forEach((dot, index) => {
    dot.classList.toggle('active', index === currentTestimonial);
  });
}

testimonialDots.forEach((dot, index) => {
  dot.addEventListener('click', () => {
    currentTestimonial = index;
    updateTestimonialSlider();
  });
});

if (totalTestimonials > 1) {
  setInterval(() => {
    currentTestimonial = (currentTestimonial + 1) % totalTestimonials;
    updateTestimonialSlider();
  }, 5000);
}

// ===== CONTACT FORM =====
if (contactForm) {
  contactForm.addEventListener('submit', (e) => {
    const formData = new FormData(contactForm);
    const data = Object.fromEntries(formData.entries());

    let isValid = true;
    const requiredFields = ['name', 'email', 'phone', 'message'];

    requiredFields.forEach(field => {
      const input = contactForm.querySelector(`[name="${field}"]`);
      if (!data[field]?.trim()) {
        isValid = false;
        if (input) input.style.borderColor = '#ef4444';
      } else if (input) {
        input.style.borderColor = '';
      }
    });

    const emailInput = contactForm.querySelector('[name="email"]');
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

    if (emailInput && data.email && !emailRegex.test(data.email)) {
      isValid = false;
      emailInput.style.borderColor = '#ef4444';
    }

    if (!isValid) {
      e.preventDefault();
      return;
    }

    // Valid — let the form submit naturally via POST
  });
}

// ===== SEARCH FORM =====
if (searchForm) {
  searchForm.addEventListener('submit', (e) => {
    e.preventDefault();

    const formData = new FormData(searchForm);
    const params = Object.fromEntries(formData.entries());

    const activeTab = document.querySelector('.search-tab.active');
    const tabText = activeTab ? activeTab.textContent.toLowerCase() : 'buy';

    // Build query string from non-empty values
    const query = new URLSearchParams();
    if (params.location) query.set('location', params.location);
    if (params['property-type']) query.set('type', params['property-type']);
    if (params.bedrooms) query.set('beds', params.bedrooms);

    // Parse price range (e.g. "15000000-25000000" or "50000000" for open-ended)
    const priceVal = params['price-range'] || '';
    if (priceVal) {
      const parts = priceVal.split('-');
      if (parts[0]) query.set('minPrice', parts[0]);
      if (parts[1]) query.set('maxPrice', parts[1]);
    }

    const qs = query.toString() ? '?' + query.toString() : '';

    if (tabText === 'buy') {
      window.location.href = '/for-sale' + qs;
    } else if (tabText === 'rent') {
      window.location.href = '/for-lease' + qs;
    } else if (tabText === 'sell') {
      window.location.href = '/contact';
    }
  });
}

// ===== SCROLL REVEAL ANIMATION =====
const revealElements = document.querySelectorAll(
  '.property-card, .category-card, .about-feature'
);

revealElements.forEach(el => {
  el.style.opacity = '0';
  el.style.transform = 'translateY(30px)';
  el.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
});

function revealOnScroll() {
  const windowHeight = window.innerHeight;

  revealElements.forEach(el => {
    const elementTop = el.getBoundingClientRect().top;
    if (elementTop < windowHeight - 150) {
      el.style.opacity = '1';
      el.style.transform = 'translateY(0)';
    }
  });
}

window.addEventListener('scroll', revealOnScroll);
window.addEventListener('load', revealOnScroll);

// ===== PROPERTY CARD CLICK =====
document.querySelectorAll('.property-card').forEach(card => {
  card.addEventListener('click', (e) => {
    if (e.target.closest('.property-favorite')) return;
    const title = card.querySelector('.property-title')?.textContent;
    if (title) console.log('Viewing property:', title);
  });
});

// ===== CATEGORY CARD CLICK =====
document.querySelectorAll('.category-card').forEach(card => {
  card.addEventListener('click', () => {
    const category = card.querySelector('.category-title')?.textContent;
    if (category) console.log('Browsing category:', category);
  });
});

// ===== INITIALIZE =====
document.addEventListener('DOMContentLoaded', () => {
  updateTestimonialSlider();
});
