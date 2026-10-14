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

// Стрелки отзывов: листаем на ширину видимой части, неактивная стрелка бледнеет
document.querySelectorAll('[data-scroll]').forEach((box) => {
  const track = document.querySelector(box.dataset.scroll);
  const [prev, next] = box.querySelectorAll('svg');
  const go = (dir) => track.scrollBy({ left: dir * track.clientWidth, behavior: 'smooth' });
  const sync = () => {
    const end = track.scrollWidth - track.clientWidth - 2;
    prev?.setAttribute('stroke', track.scrollLeft > 2 ? '#000' : '#bbb');
    next?.setAttribute('stroke', track.scrollLeft < end ? '#000' : '#bbb');
  };
  [prev, next].forEach((el, i) => { if (!el) return; el.style.cursor = 'pointer'; el.addEventListener('click', () => go(i ? 1 : -1)); });
  track.addEventListener('scroll', sync, { passive: true }); sync();
});

// Страница всех отзывов: вкладки по цвету и «Показать ещё»
const rvdata = document.getElementById('rvdata');
if (rvdata) {
  const all = JSON.parse(rvdata.textContent);
  const list = document.getElementById('rvlist');
  const more = document.getElementById('rvmore');
  const esc = (t) => t.replace(/[&<>]/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;' }[c]));
  const d = (x) => `${x.slice(8, 10)}.${x.slice(5, 7)}.${x.slice(2, 4)}`;
  let cur = 'all'; let shown = 0;
  const items = () => (cur === 'all' ? all : all.filter((r) => r.sku === cur));
  const render = (reset) => {
    if (reset) { list.innerHTML = ''; shown = 0; }
    const part = items().slice(shown, shown + 20);
    list.insertAdjacentHTML('beforeend', part.map((r) => `<div class="ritem"><div class="rh"><b>${esc(r.name)}</b><span class="stars">${'★'.repeat(r.stars)}${'☆'.repeat(5 - r.stars)}</span></div><p>${esc(r.text)}</p></div>`).join(''));
    shown += part.length;
    more.hidden = shown >= items().length;
  };
  document.querySelectorAll('[data-r]').forEach((t) => t.addEventListener('click', (e) => {
    e.preventDefault(); cur = t.dataset.r;
    document.querySelectorAll('[data-r]').forEach((x) => x.classList.toggle('on', x === t)); render(true);
  }));
  more.addEventListener('click', () => render(false));
  render(true);
}

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

// Квиз: цвет — только по цветотипу (таблица по словарю Вады), модель — из ответа про темп.
// Не знаете цветотип → два наводящих вопроса: подтон (металл) + контраст.
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
  // Цветотип → цвета по модели, первый — главный.
  const REC = {
    spring: { '01': ['gold', 'bronze'], '02': ['pink'] },
    summer: { '01': ['silver'], '02': ['pink'] },
    autumn: { '01': ['bronze', 'gold'], '02': ['ruby'] },
    winter: { '01': ['ruby', 'silver'], '02': ['ruby'] },
  };
  const SEASON_WHY = {
    spring: 'Весна тёплая и светлая, ей к лицу солнечный блеск.',
    summer: 'Лето прохладное и мягкое, ему идёт блеск без нажима.',
    autumn: 'Осень тёплая и глубокая, как металл в свете свечи.',
    winter: 'Зима холодная и контрастная, полутона ей скучны.',
  };
  const FROM_HELP = { 'warm-light': 'spring', 'warm-deep': 'autumn', 'cool-light': 'summer', 'cool-deep': 'winter' };
  const helpers = quiz.querySelectorAll('[data-help]');
  const res = document.getElementById('qres');

  const seasonOf = (a) => {
    if (a.season && a.season !== 'unknown') return a.season;
    if (a.season === 'unknown' && a.tone && a.depth) return FROM_HELP[`${a.tone}-${a.depth}`];
    return null;
  };

  quiz.addEventListener('change', () => {
    const a = Object.fromEntries(new FormData(quiz));
    helpers.forEach((f) => { f.hidden = a.season !== 'unknown'; });
    const season = seasonOf(a);
    if (!season || !a.model) { res.hidden = true; return; }
    const model = a.model === '02' ? '02' : '01';
    const colors = REC[season][model];
    const sku = `${model}-${colors[0]}`;
    const parts = [CHAR[sku], SEASON_WHY[season]];
    if (season === 'spring' && model === '02') parts.push('В № 02 тёплых оттенков нет, но Pink такая же светлая, как вы.');
    if (a.model === '01' || a.model === '02') parts.push('Под ваш темп.');
    res.hidden = false;
    document.getElementById('qr-name').textContent = NAMES[sku];
    document.getElementById('qr-num').textContent = model;
    document.getElementById('qr-why').textContent = parts.join(' ');
    document.getElementById('qr-pic').src = `img/zya-${sku}-1.jpg`;
    document.getElementById('qr-img').href = `product-${sku}.html`;
    document.getElementById('qr-more').href = `product-${sku}.html`;
    document.getElementById('qr-buy').href = zyaHref(SKU_ART[sku]);
    const alt = document.getElementById('qr-alt');
    alt.hidden = !colors[1];
    if (colors[1]) {
      const altSku = `${model}-${colors[1]}`;
      const link = document.getElementById('qr-alt-a');
      link.textContent = NAMES[altSku];
      link.href = `product-${altSku}.html`;
    }
    const card = res.querySelector('.qres-card');
    card.classList.remove('upd'); void card.offsetWidth; card.classList.add('upd');
    if (!res.dataset.shown) { res.dataset.shown = '1'; res.scrollIntoView({ behavior: 'smooth', block: 'center' }); }
  });
}
