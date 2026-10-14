// Автотест сайта: node test.cjs → скриншоты в test_shots/, отчёт в консоль
const { chromium } = require('D:/my-project/node_modules/playwright');
const path = require('path');
const fs = require('fs');
const url = (f) => 'file:///' + path.resolve(__dirname, f).split(path.sep).join('/');
const out = path.join(__dirname, 'test_shots');
fs.mkdirSync(out, { recursive: true });
const PAGES = ['index.html', 'catalog.html', 'quiz.html', 'product-01-gold.html', 'product-02-pink.html'];
const results = [];
const ok = (name, cond, extra = '') => results.push(`${cond ? 'OK  ' : 'FAIL'} ${name}${extra ? ' — ' + extra : ''}`);

(async () => {
  const b = await chromium.launch();
  for (const [W, H, tag] of [[1440, 900, 'd'], [390, 844, 'm']]) {
    const mob = W < 600;
    const ctx = await b.newContext({ viewport: { width: W, height: H }, isMobile: mob, hasTouch: mob });
    for (const f of PAGES) {
      const p = await ctx.newPage();
      const errs = [];
      p.on('pageerror', (e) => errs.push(e.message));
      p.on('console', (m) => { if (m.type() === 'error' && !/fonts\.g/.test(m.text())) errs.push(m.text()); });
      await p.goto(url(f), { waitUntil: 'networkidle' });
      await p.evaluate(() => document.fonts.ready);
      const ov = await p.evaluate(() => document.documentElement.scrollWidth - innerWidth);
      ok(`${tag} ${f} без горизонтальной прокрутки`, ov <= 0, `overflow ${ov}px`);
      ok(`${tag} ${f} без ошибок JS`, errs.length === 0, errs.join(' | '));
      const broken = await p.evaluate(() => [...document.querySelectorAll('a[href$=".html"]')].map((a) => a.getAttribute('href').split('#')[0]));
      const missing = [...new Set(broken)].filter((h) => !fs.existsSync(path.join(__dirname, h)));
      ok(`${tag} ${f} все ссылки на страницы существуют`, missing.length === 0, missing.join(', '));
      await p.screenshot({ path: path.join(out, `${tag}_${f.replace('.html', '')}.jpg`), fullPage: true, type: 'jpeg', quality: 70 });
      await p.close();
    }
    // интерактив
    const p = await ctx.newPage();
    await p.goto(url('index.html'), { waitUntil: 'networkidle' });
    await p.click('[data-tab="t2"]');
    ok(`${tag} табы: модель № 02 показывается`, await p.isVisible('#t2 .card') && !(await p.isVisible('#t1 .card')));
    await p.click('#faq details summary');
    ok(`${tag} FAQ раскрывается`, await p.isVisible('#faq details[open] .a'));
    const zya = await p.getAttribute('.feat .zya', 'href');
    ok(`${tag} кнопка ЗЯ ведёт на goldapple.ru`, /goldapple\.ru/.test(zya || ''), zya);
    if (!mob) {
      await p.hover('.nav li[data-mega="mg-brush"]');
      await p.waitForTimeout(200);
      ok('d мега-меню «Расчёски» открывается', await p.isVisible('#mg-brush'));
      await p.screenshot({ path: path.join(out, 'd_mega.jpg'), type: 'jpeg', quality: 70 });
    } else {
      await p.click('.burger');
      ok('m мобильное меню открывается', await p.isVisible('#drawer .dr-menu'));
      await p.screenshot({ path: path.join(out, 'm_drawer.jpg'), type: 'jpeg', quality: 70 });
    }
    await p.goto(url('quiz.html'), { waitUntil: 'networkidle' });
    for (const [n, v] of [['metal', 'silver'], ['model', '01'], ['place', 'bag'], ['accent', 'black']]) await p.check(`input[name="${n}"][value="${v}"]`, { force: true });
    ok(`${tag} квиз: результат «№ 01 Silver»`, (await p.textContent('#qr-name')) === '№ 01 Silver', await p.textContent('#qr-name'));
    await p.check('input[name="metal"][value="gold"]', { force: true });
    ok(`${tag} квиз: смена металла пересчитывает → № 01 Gold`, (await p.textContent('#qr-name')) === '№ 01 Gold', await p.textContent('#qr-name'));
    await p.check('input[name="accent"][value="red"]', { force: true });
    ok(`${tag} квиз: красный акцент → № 01 Ruby`, (await p.textContent('#qr-name')) === '№ 01 Ruby', await p.textContent('#qr-name'));
    await p.check('input[name="model"][value="02"]', { force: true });
    await p.check('input[name="accent"][value="pink"]', { force: true });
    ok(`${tag} квиз: № 02 + розовый → № 02 Pink`, (await p.textContent('#qr-name')) === '№ 02 Pink', await p.textContent('#qr-name'));
    await p.check('input[name="model"][value="01"]', { force: true });
    ok(`${tag} квиз: модель из ответа про темп (01 при розовом)`, (await p.textContent('#qr-name')).startsWith('№ 01'), await p.textContent('#qr-name'));
    await p.screenshot({ path: path.join(out, `${tag}_quiz_result.jpg`), type: 'jpeg', quality: 70 });
    await p.goto(url('catalog.html#m02'), { waitUntil: 'networkidle' });
    ok(`${tag} каталог #m02 → 2 расчёски`, (await p.textContent('#cnt')) === '2 расчёски', await p.textContent('#cnt'));
    await ctx.close();
  }
  await b.close();
  console.log(results.join('\n'));
  console.log(`\n${results.filter((r) => r.startsWith('FAIL')).length} FAIL из ${results.length}`);
})();
