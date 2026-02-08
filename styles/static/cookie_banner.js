// Cookie Consent Banner + GA4 Conditional Loading
// Banner only appears on homepage; GA4 loads on ALL pages once consent is given
(function() {
  var GA_ID = 'G-6NGE48T3KE';

  function getCookie(name) {
    var match = document.cookie.match(new RegExp('(^| )' + name + '=([^;]+)'));
    return match ? match[2] : null;
  }

  function setCookie(name, value, days) {
    var d = new Date();
    d.setTime(d.getTime() + days * 24 * 60 * 60 * 1000);
    document.cookie = name + '=' + value + ';expires=' + d.toUTCString() + ';path=/;SameSite=Lax';
  }

  function loadGA4() {
    if (window._ga4Loaded) return;
    window._ga4Loaded = true;
    var script = document.createElement('script');
    script.async = true;
    script.src = 'https://www.googletagmanager.com/gtag/js?id=' + GA_ID;
    document.head.appendChild(script);
    window.dataLayer = window.dataLayer || [];
    function gtag() { dataLayer.push(arguments); }
    window.gtag = gtag;
    gtag('js', new Date());
    gtag('config', GA_ID);
  }

  function hideBanner(banner) {
    banner.classList.add('hidden');
  }

  function init() {
    var banner = document.getElementById('cookieBanner');
    var consent = getCookie('cookie_consent');

    if (consent === 'accepted') {
      loadGA4();
      if (banner) hideBanner(banner);
    } else if (consent === 'declined') {
      if (banner) hideBanner(banner);
    }
    // If no consent and banner exists, it stays visible (default CSS state)

    // Accept button
    var acceptBtn = document.getElementById('cookieAccept');
    if (acceptBtn) {
      acceptBtn.addEventListener('click', function() {
        setCookie('cookie_consent', 'accepted', 365);
        loadGA4();
        if (banner) hideBanner(banner);
      });
    }

    // Decline button
    var declineBtn = document.getElementById('cookieDecline');
    if (declineBtn) {
      declineBtn.addEventListener('click', function() {
        setCookie('cookie_consent', 'declined', 365);
        if (banner) hideBanner(banner);
      });
    }
  }

  // Run when DOM is ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
