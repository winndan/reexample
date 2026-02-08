// ===== NAVBAR DOM ELEMENTS =====

const navheader = document.querySelector('.header');
const mobileToggle = document.querySelector('.mobile-toggle');
const mobileMenu = document.querySelector('.mobile-menu');
const mobileOverlay = document.querySelector('.mobile-overlay');
const mobileClose = document.querySelector('.mobile-menu-close');
const navLinks = document.querySelectorAll('.nav-link');
const mobileNavLinks = document.querySelectorAll('.mobile-nav-link');

// ===== HEADER SCROLL EFFECT =====
if (navheader) {
  window.addEventListener('scroll', () => {
    navheader.classList.toggle('scrolled', window.scrollY > 50);
  });
}


// ===== MOBILE MENU OPEN / CLOSE =====
function openMobileMenu() {
  if (!mobileMenu || !mobileOverlay) return;

  // Close filters sidebar if it exists (listing page)
  document.getElementById('filtersSidebar')?.classList.remove('active');
  document.querySelector('.filters-overlay')?.classList.remove('active');

  mobileMenu.classList.add('active');
  mobileOverlay.classList.add('active');
  document.body.style.overflow = 'hidden';
}


function closeMobileMenu() {
  if (!mobileMenu || !mobileOverlay) return;

  mobileMenu.classList.remove('active');
  mobileOverlay.classList.remove('active');
  document.body.style.overflow = '';
}

// Toggle button
if (mobileToggle) {
  mobileToggle.addEventListener('click', openMobileMenu);
}

// Close button
if (mobileClose) {
  mobileClose.addEventListener('click', closeMobileMenu);
}

// Overlay click
if (mobileOverlay) {
  mobileOverlay.addEventListener('click', closeMobileMenu);
}

// Close menu when clicking a mobile nav link
mobileNavLinks.forEach(link => {
  link.addEventListener('click', closeMobileMenu);
});

// ===== ACTIVE NAV LINK (OPTIONAL) =====
// Marks clicked link as active (for multi-page apps)
function setActiveLink(clickedLink, links) {
  links.forEach(link => link.classList.remove('active'));
  clickedLink.classList.add('active');
}

navLinks.forEach(link => {
  link.addEventListener('click', () => {
    setActiveLink(link, navLinks);
  });
});

mobileNavLinks.forEach(link => {
  link.addEventListener('click', () => {
    setActiveLink(link, mobileNavLinks);
  });
});
