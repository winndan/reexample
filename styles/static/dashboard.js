// Dashboard Navigation - active state from URL
(function() {
    var links = document.querySelectorAll('.dash-nav-link');
    var params = new URLSearchParams(window.location.search);
    var tab = params.get('tab') || 'overview';
    links.forEach(function(link) {
        link.classList.remove('active');
        if (link.href && link.href.includes('tab=' + tab)) {
            link.classList.add('active');
        }
    });
})();

// Mobile nav toggle
function toggleDashNav() {
    var nav = document.querySelector('.dash-nav');
    if (nav) nav.classList.toggle('open');
}

// Modal open/close
function openModal(id) {
    var modal = document.getElementById(id);
    if (modal) modal.style.display = 'flex';
}

function closeModal(id) {
    var modal = document.getElementById(id);
    if (modal) modal.style.display = 'none';
}

// Click overlay to close
document.addEventListener('click', function(e) {
    if (e.target.classList.contains('modal-overlay')) {
        e.target.style.display = 'none';
    }
});

// ESC key to close modals
document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape') {
        var modals = document.querySelectorAll('.modal-overlay');
        modals.forEach(function(m) {
            m.style.display = 'none';
        });
    }
});
