// Run on a demo origin with playwright-cli run-code --filename tools/browser-check.js.
async page => {
  const origin = new URL(page.url()).origin;
  const routes = ['/', '/napravleniya', '/raspisanie', '/stoimost', '/komanda', '/faq', '/sertifikaty', '/kontakty', '/cabinet'];
  const widths = [360, 390, 768, 1024, 1440];
  const errors = [];
  const requireCheck = (condition, message) => { if (!condition) throw new Error(message); };
  page.on('pageerror', error => errors.push(error.message));
  for (const route of routes) {
    const response = await page.goto(origin + route);
    requireCheck(response.status() === 200, 'HTTP error ' + route);
    requireCheck(await page.locator('h1').count() === 1, 'H1 ' + route);
    requireCheck(await page.locator('link[rel=canonical]').getAttribute('href') === 'https://classes.homepilates.ru' + route, 'Canonical ' + route);
    for (const width of widths) {
      await page.setViewportSize({width, height: 900});
      const viewport = await page.evaluate(() => [document.documentElement.clientWidth, document.documentElement.scrollWidth]);
      requireCheck(viewport[0] === width && viewport[1] <= viewport[0], 'Overflow ' + route + ' at ' + width + ': ' + viewport);
    }
  }
  await page.setViewportSize({width:390,height:844});
  await page.goto(origin);
  const menu = page.locator('.menu summary');
  await menu.focus();
  await page.keyboard.press('Enter');
  await page.locator('#hp-nav').waitFor({state:'visible'});
  await page.keyboard.press('Tab');
  requireCheck(await page.evaluate(() => document.activeElement.closest('#hp-nav') !== null), 'Tab into menu');
  await page.keyboard.press('Escape');
  requireCheck(await menu.evaluate(el => document.activeElement === el && !el.parentElement.open), 'Escape and focus restoration');
  await menu.click();
  await page.locator('#hp-nav').getByRole('link', {name:'Стоимость',exact:true}).click();
  const priceGroups = page.locator('.acc');
  requireCheck(await priceGroups.count() === 7, 'Seven pricing groups');
  requireCheck(await page.locator('.prices li').count() === 33, '33 price rows');
  for (const group of await priceGroups.all()) {
    const summary = group.locator('summary');
    await summary.focus();
    const before = await group.evaluate(el => el.open);
    await page.keyboard.press('Space');
    requireCheck(await group.evaluate(el => el.open) !== before, 'Price accordion');
  }
  await page.goto(origin + '/faq');
  requireCheck(await page.locator('.acc').count() === 8, 'Eight FAQ topics');
  for (const answer of await page.locator('.acc').all()) {
    await answer.locator('summary').focus();
    await page.keyboard.press('Enter');
    requireCheck(await answer.locator('.answer').isVisible(), 'FAQ keyboard');
  }
  // Cookie choice: nothing goes to Metrika before consent or after "only essential"
  const metrika = [];
  page.on('request', request => { if (request.url().includes('mc.yandex.ru')) metrika.push(request.url()); });
  await page.evaluate(() => localStorage.clear());
  await page.goto(origin);
  await page.locator('.cookie-box').waitFor({state:'visible'});
  await page.locator('.cookie-box [name="essential"]').click();
  requireCheck(await page.locator('.cookie-box').isHidden(), 'Cookie box closes');
  await page.reload();
  requireCheck(await page.locator('.cookie-box').isHidden() && metrika.length === 0, 'Metrika waits for consent');
  await page.locator('.head-actions .btn').click();
  requireCheck(new URL(page.url()).pathname.replace(/\/$/, '') === '/raspisanie', 'Booking leads to the schedule');
  requireCheck(await page.locator('.mobi').count() === 1, 'One Mobifitness widget');
  await page.emulateMedia({reducedMotion:'reduce'});
  requireCheck(await page.locator('.btn').first().evaluate(el => getComputedStyle(el).transitionDuration === '0s'), 'Reduced motion');
  requireCheck(errors.length === 0, errors.join(', '));
  return 'PASS: 9 routes × 5 widths, menu, focus, 7 pricing groups, 8 FAQ, cookie and Metrika, booking route, reduced motion and browser errors.';
}
