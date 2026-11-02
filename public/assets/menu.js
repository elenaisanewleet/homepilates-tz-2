(() => {
  const site = document.getElementById('hp-site');
  if (!site) return;
  const menu = site.querySelector('.menu');
  site.querySelectorAll('details').forEach(details => {
    const summary = details.querySelector('summary');
    const update = () => summary.setAttribute('aria-expanded', String(details.open));
    update();
    details.addEventListener('toggle', update);
  });
  if (!menu) return;
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
})();
