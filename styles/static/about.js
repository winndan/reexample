const mobileToggle = document.querySelector('.mobile-toggle');
const mobileMenu = document.querySelector('.mobile-menu');
const mobileOverlay = document.querySelector('.mobile-overlay');
const mobileMenuClose = document.querySelector('.mobile-menu-close');
const statNumbers = document.querySelectorAll('.stat-number');
const featureCards = document.querySelectorAll('.feature-card');
const teamCards = document.querySelectorAll('.team-card');

function toggleMobileMenu() {
  mobileMenu.classList.toggle('active');
  mobileOverlay.classList.toggle('active');
  document.body.style.overflow = mobileMenu.classList.contains('active') ? 'hidden' : '';
}

function closeMobileMenu() {
  mobileMenu.classList.remove('active');
  mobileOverlay.classList.remove('active');
  document.body.style.overflow = '';
}

if (mobileToggle) {
  mobileToggle.addEventListener('click', toggleMobileMenu);
}

if (mobileMenuClose) {
  mobileMenuClose.addEventListener('click', closeMobileMenu);
}

if (mobileOverlay) {
  mobileOverlay.addEventListener('click', closeMobileMenu);
}

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
  const statsSection = document.querySelector('.stats-section');
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

featureCards.forEach(card => {
  card.style.opacity = '0';
  card.style.transform = 'translateY(30px)';
  card.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
});

teamCards.forEach(card => {
  card.style.opacity = '0';
  card.style.transform = 'translateY(30px)';
  card.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
});

function revealElements() {
  const windowHeight = window.innerHeight;

  featureCards.forEach((card, index) => {
    const cardTop = card.getBoundingClientRect().top;
    if (cardTop < windowHeight - 100) {
      setTimeout(() => {
        card.style.opacity = '1';
        card.style.transform = 'translateY(0)';
      }, index * 100);
    }
  });

  teamCards.forEach((card, index) => {
    const cardTop = card.getBoundingClientRect().top;
    if (cardTop < windowHeight - 100) {
      setTimeout(() => {
        card.style.opacity = '1';
        card.style.transform = 'translateY(0)';
      }, index * 150);
    }
  });
}

window.addEventListener('scroll', () => {
  checkStatsVisibility();
  revealElements();
});

window.addEventListener('load', () => {
  checkStatsVisibility();
  revealElements();
});

document.addEventListener('DOMContentLoaded', () => {
  checkStatsVisibility();
  revealElements();
});
