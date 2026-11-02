(() => {
  const site = document.getElementById('hp-site');
  if (!site || site.dataset.ready) return;
  site.dataset.ready = '1';
  const find = selector => site.querySelector(selector);

  // Menu and accordions
  const menu = site.querySelector('.menu');
  site.querySelectorAll('details').forEach(details => {
    const summary = details.querySelector('summary');
    const update = () => summary.setAttribute('aria-expanded', String(details.open));
    update();
    details.addEventListener('toggle', update);
  });
  if (menu) {
    document.addEventListener('keydown', event => {
      if (event.key === 'Escape' && menu.open) {
        menu.open = false;
        menu.querySelector('summary').focus();
      }
    });
    document.addEventListener('click', event => {
      if (menu.open && !menu.contains(event.target)) menu.open = false;
    });
    menu.addEventListener('click', event => {
      if (event.target.closest('a')) menu.open = false;
    });
    menu.addEventListener('focusout', event => {
      if (event.relatedTarget && !menu.contains(event.relatedTarget)) menu.open = false;
    });
  }

  // Cookie consent; Yandex Metrika starts only after analytics consent
  const cookie = find('.cookie-box');
  if (cookie) {
    const analytics = cookie.querySelector('[name="analytics"]');
    const ads = cookie.querySelector('[name="ads"]');
    const prefsKey = 'hp.cookie.v1';
    const counter = Number(site.dataset.counter);
    let prefs;
    try { prefs = JSON.parse(localStorage.getItem(prefsKey)); } catch (_) {}
    let running = false;
    const meter = enabled => {
      if (location.protocol === 'file:' || !counter) return;
      if (!enabled && running) {
        window.ym(counter, 'destruct');
        running = false;
      } else if (enabled && !running) {
        if (!window.ym) {
          window.ym = function () { (window.ym.a = window.ym.a || []).push(arguments); };
          window.ym.l = Date.now();
          const tag = document.createElement('script');
          tag.src = 'https://mc.yandex.ru/metrika/tag.js';
          tag.async = true;
          document.head.appendChild(tag);
        }
        window.ym(counter, 'init', {clickmap: true, trackLinks: true, accurateTrackBounce: true});
        running = true;
      }
    };
    if (prefs && typeof prefs.analytics === 'boolean' && typeof prefs.ads === 'boolean') {
      analytics.checked = prefs.analytics;
      ads.checked = prefs.ads;
      meter(prefs.analytics);
    } else {
      cookie.hidden = false;
    }
    const reopen = find('[data-cookie-open]');
    if (reopen) reopen.addEventListener('click', () => {
      cookie.hidden = false;
      cookie.querySelector('details').open = true;
      cookie.querySelector('summary').focus();
    });
    cookie.addEventListener('submit', event => {
      event.preventDefault();
      if (event.submitter && event.submitter.name === 'essential') analytics.checked = ads.checked = false;
      prefs = {analytics: analytics.checked, ads: ads.checked};
      try { localStorage.setItem(prefsKey, JSON.stringify(prefs)); } catch (_) {}
      meter(prefs.analytics);
      cookie.hidden = true;
    });
  }

  // Feedback form: opens the visitor's mail app (in Tilda the form is replaced by a native Tilda form → amoCRM)
  const feedback = find('[data-feedback]');
  if (feedback) feedback.addEventListener('submit', event => {
    event.preventDefault();
    const body = Array.from(new FormData(feedback), ([key, value]) => key + ': ' + value).join('\n');
    location.href = 'mailto:' + feedback.dataset.feedback + '?subject=' +
      encodeURIComponent(feedback.dataset.subject) + '&body=' + encodeURIComponent(body);
  });

  // Mobifitness widget: the schedule mounts at once, the others when the visitor scrolls close to them
  const host = find('.mobi');
  if (!host) return;
  const cfg = host.dataset;
  const address = new URL(cfg.url);
  const mount = () => {
    if (host.dataset.mounted) return;
    host.dataset.mounted = '1';
    if (location.protocol === 'https:') {
      const script = document.createElement('script');
      script.id = 'mobifitness_personal_widget_script';
      Object.assign(script.dataset, {code: cfg.code, club: cfg.club, domain: address.hostname,
        div: host.id, type: cfg.type, language: 'ru'});
      if (cfg.section) script.dataset.section = cfg.section;
      script.src = address.origin + '/personal-widget/js/code.js';
      const observer = new MutationObserver(() => {
        const frame = host.querySelector('iframe');
        if (frame) { frame.title = cfg.title; observer.disconnect(); }
      });
      observer.observe(host, {subtree: true, childList: true});
      host.after(script);
    } else {
      const frame = document.createElement('iframe');
      frame.src = address.href;
      frame.title = cfg.title;
      frame.height = cfg.type === 'schedule' ? '640' : '520';
      host.appendChild(frame);
    }
  };
  if (cfg.type === 'schedule' || !('IntersectionObserver' in window)) mount();
  else {
    const io = new IntersectionObserver(entries => {
      if (entries.some(entry => entry.isIntersecting)) { io.disconnect(); mount(); }
    }, {rootMargin: '600px 0px'});
    io.observe(host);
  }
})();
