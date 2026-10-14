// SANDÓVICH — поведение сайта (без библиотек)

// Ссылки на Золотое Яблоко: заполнить, когда появятся карточки товаров.
// Без артикула кнопка ведёт в каталог бренда в ЗЯ.
const ZYA_SEARCH = 'https://goldapple.ru/volosy/aksessuary/rascheski?brandobjectid=1913789';
const ZYA_LINKS = {
  HBSG01: 'https://goldapple.ru/99000205592-sandovich-01',
  HBSS01: 'https://goldapple.ru/99000205595-sandovich-01',
  HBSB01: 'https://goldapple.ru/99000205593-sandovich-01',
  HBSR01: 'https://goldapple.ru/99000205594-sandovich-01',
  HBSR02: 'https://goldapple.ru/99000205596-sandovich-02',
  HBSP02: 'https://goldapple.ru/99000205591-02',
};
const SKU_ART = {
  '01-gold': 'HBSG01', '01-silver': 'HBSS01', '01-bronze': 'HBSB01',
  '01-ruby': 'HBSR01', '02-ruby': 'HBSR02', '02-pink': 'HBSP02',
};

const zyaHref = (art) => (art && ZYA_LINKS[art]) || ZYA_SEARCH;
document.querySelectorAll('.zya').forEach((a) => {
  a.href = zyaHref(a.dataset.sku);
  a.target = '_blank';
  a.rel = 'noopener';
});

// Табы на главной
document.querySelectorAll('[data-tab]').forEach((btn) => {
  btn.addEventListener('click', () => {
    document.querySelectorAll('[data-tab]').forEach((b) => b.classList.replace('on', 'off'));
    btn.classList.replace('off', 'on');
    document.querySelectorAll('.tabpanel').forEach((p) => { p.hidden = p.id !== btn.dataset.tab; });
  });
});

// Мега-меню (десктоп, по наведению)
const megas = document.querySelectorAll('.mega');
let megaTimer;
const closeMegas = () => megas.forEach((m) => m.classList.remove('open'));
document.querySelectorAll('.nav li[data-mega]').forEach((li) => {
  const mega = document.getElementById(li.dataset.mega);
  const open = () => { clearTimeout(megaTimer); closeMegas(); mega.classList.add('open'); };
  const close = () => { megaTimer = setTimeout(closeMegas, 150); };
  li.addEventListener('mouseenter', open);
  li.addEventListener('mouseleave', close);
  mega.addEventListener('mouseenter', () => clearTimeout(megaTimer));
  mega.addEventListener('mouseleave', close);
});
document.querySelectorAll('.nav li:not([data-mega])').forEach((li) => li.addEventListener('mouseenter', closeMegas));

// Мобильное меню
const drawer = document.getElementById('drawer');
document.querySelector('.burger')?.addEventListener('click', () => { drawer.hidden = false; document.body.style.overflow = 'hidden'; });
document.querySelector('.dr-close')?.addEventListener('click', () => { drawer.hidden = true; document.body.style.overflow = ''; });

// Стрелки отзывов
document.querySelectorAll('[data-scroll]').forEach((box) => {
  const track = document.querySelector(box.dataset.scroll);
  const [prev, next] = box.querySelectorAll('svg');
  const step = () => track.firstElementChild.getBoundingClientRect().width;
  prev?.addEventListener('click', () => track.scrollBy({ left: -step(), behavior: 'smooth' }));
  next?.addEventListener('click', () => track.scrollBy({ left: step(), behavior: 'smooth' }));
});

// «+» → «−» у раскрывающихся вопросов
document.querySelectorAll('details').forEach((d) => {
  d.addEventListener('toggle', () => {
    const s = d.querySelector('summary span');
    if (s) s.textContent = d.open ? '−' : '+';
  });
});

// Каталог: фильтр по табам и якорям (#m01, #m02, #gift)
const cgrid = document.getElementById('cgrid');
if (cgrid) {
  const apply = (f) => {
    let n = 0;
    cgrid.querySelectorAll('.card').forEach((c) => {
      if (c.classList.contains('ed')) { c.hidden = f !== 'all'; return; }
      const sku = c.querySelector('a').getAttribute('href').replace('product-', '').replace('.html', '');
      const show = f === 'all' || f === 'gift' || sku.startsWith(f);
      c.hidden = !show; if (show) n += 1;
    });
    document.getElementById('cnt').textContent = `${n} ${n === 1 ? 'расчёска' : n < 5 ? 'расчёски' : 'расчёсок'}`;
    document.querySelectorAll('.ctabs a').forEach((a) => a.classList.toggle('on', a.dataset.f === f));
  };
  const fromHash = () => ({ '#m01': '01', '#m02': '02', '#gift': 'gift' }[location.hash] || 'all');
  document.querySelectorAll('.ctabs a').forEach((a) => a.addEventListener('click', (e) => { e.preventDefault(); history.replaceState(null, '', a.getAttribute('href')); apply(a.dataset.f); }));
  window.addEventListener('hashchange', () => apply(fromHash()));
  apply(fromHash());
}

// Квиз: модель — из вопроса о форме, цвет — из металла и акцента
const quiz = document.getElementById('quiz');
if (quiz) {
  const NAMES = {
    '01-gold': '№ 01 Gold', '01-silver': '№ 01 Silver', '01-bronze': '№ 01 Bronze',
    '01-ruby': '№ 01 Ruby', '02-ruby': '№ 02 Ruby', '02-pink': '№ 02 Pink',
  };
  const CHAR = {
    '01-gold': 'Gold из тех, кого замечают в любой комнате. Ей это нравится.',
    '01-silver': 'Silver: спокойствие, которое со стороны выглядит как вкус.',
    '01-bronze': 'Bronze: тепло, которое не нужно доказывать.',
    '01-ruby': 'Ruby: красный, рядом с которым остальное становится фоном.',
    '02-ruby': 'Ruby № 02: красный, которому хватает пары движений.',
    '02-pink': 'Pink: смелость, которая умеет улыбаться.',
  };
  // Подбор: модель строго из ответа про темп, цвет — сумма очков за металл и акцент.
  const SKUS = { '01': ['gold', 'silver', 'bronze', 'ruby'], '02': ['ruby', 'pink'] };
  const METAL = { gold: { gold: 3 }, silver: { silver: 3 }, rose: { bronze: 3, pink: 1 }, none: {} };
  const ACCENT = { red: { ruby: 3 }, pink: { pink: 3, bronze: 1 }, nude: { bronze: 2, gold: 1 }, black: { silver: 2, ruby: 1 } };
  const score = (a, color) => {
    const m = (METAL[a.metal] || {})[color] || 0;
    const c = (ACCENT[a.accent] || {})[color] || 0;
    return { m, c, total: m + c };
  };
  // при равенстве очков побеждает вопрос, который поменяли последним
  const pick = (a, last) => {
    const models = a.model === '01' || a.model === '02' ? [a.model] : ['01', '02'];
    let best = null;
    for (const model of models) {
      for (const color of SKUS[model]) {
        const s = score(a, color);
        // в сумку, если модель не выбрана, чуть ближе лёгкая № 02
        const bonus = a.model === 'any' && a.place === 'bag' && model === '02' ? 0.5 : 0;
        const total = s.total + bonus;
        const lastPts = last === 'accent' ? s.c : s.m;
        const cand = { sku: `${model}-${color}`, total, m: s.m, c: s.c, lastPts };
        if (!best || total > best.total || (total === best.total && lastPts > best.lastPts)) best = cand;
      }
    }
    return best;
  };
  const why = (a, best) => {
    const parts = [];
    if (best.m > 0) parts.push('Под ваш металл.');
    if (best.c > 0) parts.push('Под акцент в образе.');
    if (a.model === '01' || a.model === '02') parts.push('Под ваш темп.');
    if (a.place === 'gift') parts.push('Приходит в фирменной коробке, дарить можно сразу.');
    else if (a.place) parts.push('Ей будет хорошо на виду.');
    return parts.join(' ');
  };
  let lastQ = 'metal';
  quiz.addEventListener('change', (e) => {
    if (e.target.name === 'metal' || e.target.name === 'accent') lastQ = e.target.name;
    const a = Object.fromEntries(new FormData(quiz));
    if (Object.keys(a).length < 4) return;
    const best = pick(a, lastQ);
    const sku = best.sku;
    const res = document.getElementById('qres');
    res.hidden = false;
    document.getElementById('qr-name').textContent = NAMES[sku];
    document.getElementById('qr-num').textContent = sku.slice(0, 2);
    document.getElementById('qr-why').textContent = `${CHAR[sku]} ${why(a, best)}`;
    const card = res.querySelector('.qres-card');
    card.classList.remove('upd'); void card.offsetWidth; card.classList.add('upd');
    document.getElementById('qr-img').href = `product-${sku}.html`;
    document.getElementById('qr-img').dataset.ph = `Предметка 4:5 · ${NAMES[sku]}`;
    document.getElementById('qr-more').href = `product-${sku}.html`;
    const buy = document.getElementById('qr-buy');
    buy.href = zyaHref(SKU_ART[sku]);
    if (!res.dataset.shown) { res.dataset.shown = '1'; res.scrollIntoView({ behavior: 'smooth', block: 'center' }); }
  });
}
