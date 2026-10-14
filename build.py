import re
import time

VER = time.strftime('%Y%m%d%H%M')  # метка версии: браузер не возьмёт старые style.css/app.js из кэша

# Сборка сайта SANDÓVICH (копия структуры labonnebrosse.com 1:1):
#   python -X utf8 build.py  →  index.html, catalog.html, quiz.html, product-<sku>.html
# Общие части (head, шапка, мега-меню, мобильное меню, подвал) — здесь; стили — style.css; поведение — app.js.
# Тексты черновые; [в квадратных скобках] — то, что нужно уточнить/заполнить.

ZYA_NOTE = 'Ссылки на карточки Золотого Яблока — заполнить в app.js (ZYA_LINKS)'

PRODUCTS = [
    # sku, модель, цвет (им. п.), цвет для заголовка, hex, артикул, бейдж
    ('01-gold',   '01', 'Золото',  'Золото',  '#C9A25A', 'HBSG01', 'Хит'),
    ('01-silver', '01', 'Серебро', 'Серебро', '#C7C9CE', 'HBSS01', ''),
    ('01-bronze', '01', 'Бронза',  'Бронза',  '#B4785A', 'HBSB01', ''),
    ('01-ruby',   '01', 'Рубин',   'Рубин',   '#9E1B2A', 'HBSR01', 'Новый цвет'),
    ('02-ruby',   '02', 'Рубин',   'Рубин',   '#9E1B2A', 'HBSR02', 'Новинка'),
    ('02-pink',   '02', 'Розовая', 'Розовая', '#EBA3C3', 'HBSP02', 'Хит'),
]
MODEL = {
    '01': dict(name='№ 01', hand='длинной тонкой ручкой', size='Длина 19 см, ширина головки 4 см.'),
    '02': dict(name='№ 02', hand='короткой широкой ручкой', size='[Размеры № 02 — уточнить.]'),
}

DESC = {
    '01-gold': 'Gold не ждёт особого случая, она устраивает его сама. Рядом с ней любая полка выглядит так, будто здесь готовятся к выходу. Модель № 01 из основательных: с ней хочется задержаться подольше.',
    '01-silver': 'Silver никого не догоняет и ни под кого не подстраивается. Прохладный цвет для тех, у кого всё на своих местах, включая расчёску. Модель № 01 под стать: спокойная, обстоятельная, без суеты.',
    '01-bronze': 'Bronze не бросается в глаза. Её замечают со второго взгляда и потом уже не забывают. Модель № 01 никуда не спешит, и этому цвету так даже больше идёт.',
    '01-ruby': 'Ruby не ищет внимания. Оно находит её само. В модели № 01 у красного есть время: его и так заметили.',
    '02-ruby': 'Ruby в модели № 02. Красный без долгих вступлений: пара движений, волосы на месте, можно идти. Задерживается ненадолго, запоминается надолго.',
    '02-pink': 'Розовый, который не спрашивает разрешения. Pink смелая, весёлая и лёгкая на подъём. С Ruby они сёстры: одна громче, другая быстрее улыбается.',
}
HOWTO = {
    '01': 'Расчёсывайте сухие или мокрые волосы, не спеша, от лба к затылку и дальше по длине. В душе ведите ею маску, бальзам или кондиционер по всей длине. Торопиться с № 01 некуда, она этого и не просит.',
    '02': 'Пара движений от корней по длине, поправить, и можно идти. С мокрыми волосами так же легко: в душе проведите ею маску или бальзам по длине, и готово. № 02 не требует подготовки и не отнимает времени.',
}

ICON = dict(
    search='<svg viewBox="0 0 24 24" fill="none" stroke="#000" stroke-width="1.3"><circle cx="10.5" cy="10.5" r="6.5"/><path d="M15.5 15.5 21 21"/></svg>',
    pin='<svg viewBox="0 0 24 24" fill="none" stroke="#000" stroke-width="1.3"><path d="M12 21s-6.5-6.2-6.5-11a6.5 6.5 0 0 1 13 0c0 4.8-6.5 11-6.5 11z"/><circle cx="12" cy="10" r="2.3"/></svg>',
    bag='<svg viewBox="0 0 24 24" fill="none" stroke="#000" stroke-width="1.3"><path d="M5 8h14l-1 13H6L5 8z"/><path d="M9 8V6a3 3 0 0 1 6 0v2"/></svg>',
    burger='<svg viewBox="0 0 24 24" fill="none" stroke="#000" stroke-width="1.3"><path d="M3 7h18M3 12h18M3 17h18"/></svg>',
    close='<svg viewBox="0 0 24 24" fill="none" stroke="#000" stroke-width="1.3"><path d="M5 5l14 14M19 5 5 19"/></svg>',
    arrow='<svg width="12" height="10" viewBox="0 0 12 10" fill="none" stroke="#000" stroke-width="1.2"><path d="M0 5h11M7 1l4 4-4 4"/></svg>',
)


def head(title, desc):
    return f'''<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Jost:wght@400;500&family=Roboto+Condensed:wght@800&family=EB+Garamond:wght@500&family=Playfair+Display:wght@800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="style.css?v={VER}">
</head>
<body>
'''


def mega_links(items):
    return ''.join(f'<li><a href="{h}">{t}</a></li>' for t, h in items)


BRUSH_LINKS = [('Модель № 01', 'catalog.html#m01'), ('Модель № 02', 'catalog.html#m02'), ('Все расчёски', 'catalog.html'), ('В подарок', 'catalog.html#gift')]
COLOR_LINKS = [(f'№ {m} {c}', f'product-{s}.html') for s, m, c, *_ in PRODUCTS]
ABOUT_LINKS = [('О бренде', 'index.html#about'), ('Ритуал', 'index.html#ritual'), ('Вопросы и ответы', 'index.html#faq'), ('Где купить', '#')]


def header(active=''):
    def li(key, text, href, mega=''):
        cls = ' class="on"' if key == active else ''
        return f'<li{cls} data-mega="{mega}"><a href="{href}">{text}</a></li>' if mega else f'<li{cls}><a href="{href}">{text}</a></li>'
    return f'''<div class="ann"><a href="#" class="zya">Продаётся в Золотом Яблоке · Найти магазин</a>{ICON['arrow']}</div>
<header class="hdr">
  <a class="logo" href="index.html">SANDÓVICH</a>
  <nav class="nav">
    <ul>
      {li('new', 'Новинки', 'product-02-ruby.html')}
      {li('brushes', 'Расчёски', 'catalog.html', 'mg-brush')}
      {li('ritual', 'Ритуал', 'index.html#ritual')}
      {li('quiz', 'Подбор', 'quiz.html')}
      {li('gift', 'В подарок', 'catalog.html#gift')}
      {li('about', 'О бренде', 'index.html#about', 'mg-about')}
    </ul>
    <div class="icons">
      <a href="catalog.html" aria-label="Поиск">{ICON['search']}</a>
      <a href="#" class="zya" aria-label="Где купить">{ICON['pin']}</a>
      <a href="#" class="zya" aria-label="Купить в Золотом Яблоке">{ICON['bag']}</a>
      <button class="burger" aria-label="Меню">{ICON['burger']}</button>
    </div>
  </nav>
  <div class="mega" id="mg-brush">
    <a class="mg-feat" href="quiz.html"><div class="ph" data-ph="Фото 320×400 · модель с расчёсками у лица"><div class="w28">Какая расчёска ваша?</div></div><span class="ulink">Подобрать расчёску →</span></a>
    <div class="mg-col"><p class="mg-h">Расчёски</p><ul>{mega_links(BRUSH_LINKS)}</ul></div>
    <div class="mg-col"><p class="mg-h">По цвету</p><ul>{mega_links(COLOR_LINKS)}</ul></div>
  </div>
  <div class="mega" id="mg-about">
    <a class="mg-feat" href="index.html#ritual"><div class="ph" data-ph="Фото 320×400 · ритуал расчёсывания"><div class="w28">Ритуал</div></div><span class="ulink">Читать →</span></a>
    <div class="mg-col"><p class="mg-h">SANDÓVICH</p><ul>{mega_links(ABOUT_LINKS)}</ul></div>
  </div>
</header>
<div class="drawer" id="drawer" hidden>
  <div class="dr-top"><a class="logo" href="index.html">SANDÓVICH</a><button class="dr-close" aria-label="Закрыть">{ICON['close']}</button></div>
  <ul class="dr-menu">
    <li><a href="product-02-ruby.html">Новинки</a></li>
    <li><details><summary>Расчёски<span>+</span></summary><ul>{mega_links(BRUSH_LINKS + COLOR_LINKS)}</ul></details></li>
    <li><a href="index.html#ritual">Ритуал</a></li>
    <li><a href="quiz.html">Подбор</a></li>
    <li><a href="catalog.html#gift">В подарок</a></li>
    <li><details><summary>О бренде<span>+</span></summary><ul>{mega_links(ABOUT_LINKS)}</ul></details></li>
  </ul>
  <a class="btn btn-black zya dr-buy" href="#">Купить в Золотом Яблоке</a>
</div>
'''


FOOTER = '''<footer class="ftr">
  <div class="fgrid">
    <div><div class="t">Продолжение в Telegram</div><div class="s">Подбор цвета, идеи подарков и все места, где сейчас есть SANDÓVICH.</div><a class="btn btn-lav" href="https://t.me/sandovich_official">Подписаться</a></div>
    <div><h5>Нужна помощь?</h5><ul><li><a href="index.html#faq">Вопросы и ответы</a></li><li><a href="index.html#faq">Как ухаживать за расчёской</a></li><li><a href="#" class="zya">Где купить</a></li><li><a href="mailto:hello@sandovich.ru">Связаться с нами</a></li><li><a href="index.html#reviews">Отзывы покупателей</a></li></ul></div>
    <div><h5>Правовая информация</h5><ul><li><a href="#">Политика конфиденциальности</a></li><li><a href="#">Согласие на обработку данных</a></li><li><a href="#">Реквизиты</a></li></ul></div>
    <div><p class="follow">Мы в соцсетях</p><div class="soci">
      <a href="https://t.me/sandovich_official" aria-label="Telegram"><svg width="22" height="22" viewBox="0 0 24 24" fill="#000"><path d="M21.5 3.6 2.9 10.8c-1.3.5-1.2 1.2-.2 1.5l4.8 1.5 1.8 5.6c.2.6.4.8.9.8.4 0 .6-.2.9-.4l2.3-2.2 4.7 3.5c.9.5 1.5.2 1.7-.8l3.1-14.6c.3-1.3-.5-1.9-1.4-1.5zM9.7 14.6l-.4 4-1.5-4.8 10.4-6.6-8.5 7.4z"/></svg></a>
      <a href="#" aria-label="ВКонтакте"><svg width="22" height="22" viewBox="0 0 24 24" fill="#000"><path d="M12.8 17.3c-5.6 0-8.8-3.8-8.9-10.2h2.8c.1 4.7 2.2 6.6 3.8 7V7.1h2.6v4c1.6-.2 3.3-2 3.8-4h2.6c-.4 2.5-2.2 4.3-3.5 5.1 1.3.6 3.4 2.2 4.2 5.1h-2.9c-.6-1.9-2.2-3.4-4.2-3.6v3.6h-.3z"/></svg></a>
    </div></div>
  </div>
  <div class="zya-line">Продаётся в Золотом Яблоке</div>
  <p class="copy">© 2026 SANDÓVICH</p>
</footer>
<script src="app.js?v=__VER__"></script>
</body>
</html>
'''


# ---------- Фото (новая студийная съёмка, авг 2026; модель по цветотипу совпадает с цветом) ----------
# Текст плашки (data-ph) → файл в img/. Карточки товаров берут предметку по ссылке product-<sku>.
PH_IMG = {
    # Только согласованные фото (14.10). Остальные блоки — серые плашки до выбора по мудбордам.
    'Фото 1440×720 · расчёска как украшение или неожиданный объект (напр. девушка в бигуди и очках с расчёской розового золота, поднос под колпаком)': 'zh-hero-ruby',
    'Фото 585×877 · модель в очках, расчёска у головы, ироничный editorial': 'sc-curlers-glasses',
    'Фото 549×686 · № 01 рубин на подиуме / постаменте, тёплый фон': 'feat-151',  # согласовано 14.10
    'Фото 640×800 · модель в кадре по пояс держит 2–3 расчёски у лица, дерзкий editorial': 'blk-17',  # согласовано 14.10 (поменяны местами с ритуалом)
    'Фото 459×689 · модель с расчёской, светлый фон, крупно': 'blk-58',  # согласовано 14.10
    'Фото 459×689 · модель в очках / пиджаке, расчёска у головы, ироничный editorial': 'blk-62',  # согласовано 14.10
    'Фото 1440×576 · руки держат расчёску и коробку, крупный план, без лица': 'blk-74',  # «Подарите характер», согласовано 14.10
    'Видео / фото 480×600 · руки собирают / упаковывают расчёску': 'blk-190',  # «Вещь на виду», согласовано 14.10
    'Фото 332×415 · пять цветов рядом': 'blk-245',  # колонка «Пять цветов», согласовано 14.10
    'Фото 332×415 · расчёска в душе, маска по длине': 'blk-237',  # колонка «Ей можно в душ», согласовано 14.10
    'Фото 332×415 · № 01 и № 02 рядом': 'blk-255',  # колонка «Не торопит», согласовано 14.10 (вместо 248)
    'Фото 332×415 · расчёска в фирменной коробке': 'blk-174',  # колонка «Готова к подарку», согласовано 14.10
    'Фото 320×400 · ритуал расчёсывания': 'blk-28',  # меню «О бренде» → Ритуал, согласовано 14.10
    'Фото 320×400 · модель с расчёсками у лица': 'blk-238',  # мега-меню «Какая расчёска ваша?», согласовано 14.10
    'Фото 1440×576 · модель расчёсывает волосы, движение': 'blk-238',  # баннер «Какая расчёска ваша?» на карточке товара
    'Фото 720×600 · модель расчёсывает длинные волосы, editorial, контрастный интерьер': 'blk-31',  # согласовано 14.10
}
import os as _os
if _os.environ.get('PREVIEW'):  # мудборды по блокам: кандидаты, не согласованы, не выкладывать
    PH_IMG.update({
        
        'Фото 640×800 · модель в кадре по пояс держит 2–3 расчёски у лица, дерзкий editorial': 'p-3853',
        'Фото 459×689 · модель с расчёской, светлый фон, крупно': 'p-3866',
        'Фото 459×689 · модель в очках / пиджаке, расчёска у головы, ироничный editorial': 'p-3829',
        'Фото 720×600 · модель расчёсывает длинные волосы, editorial, контрастный интерьер': 'p-3873',
        'Фото 1440×576 · руки держат расчёску и коробку, крупный план, без лица': 'p-4022-band',
        'Видео / фото 480×600 · руки собирают / упаковывают расчёску': 'p-3790',
        'Фото 332×415 · пять цветов рядом': 'zya-01-gold-3',
        'Фото 332×415 · № 01 и № 02 рядом': 'zya-02-ruby-4',
        'Фото 332×415 · расчёска в душе, маска по длине': 'zya-01-silver-2',
        'Фото 332×415 · расчёска в фирменной коробке': 'zya-01-bronze-5',
    })
# Галерея товара: героиня по цветотипу (Весна — Gold/Bronze, Лето — Silver/Pink, Зима — Ruby)
GALLERY = {
    '01-gold':   ['v-spring-gold-comb', 'v-spring-gold-hands2', 'm-spring-gold-hands'],
    '01-silver': ['m-summer-silver', 'm-winter-silver-tights', 'v-winter-silver-teeth'],
    '01-bronze': ['v-spring-bronze-comb', 'v-spring-bronze-hands', 'v-spring-bronze-hair'],
    '01-ruby':   ['m-winter-ruby01-a', 'v-winter-ruby01-teeth', 'sc-hands-five'],
    '02-ruby':   ['v-winter-ruby02-cheek', 'v-winter-ruby02-floor', 'v-winter-ruby02-squat'],
    '02-pink':   ['m-summer-pink', 'v-summer-pink-lie', 'v-summer-pink-hair'],
}
BOX = {'01-gold': 'box-01-gold', '01-silver': 'box-01-silver', '01-bronze': 'box-01-bronze',
       '01-ruby': 'box-01-ruby', '02-ruby': 'v-winter-ruby02-c2', '02-pink': 'box-02-pink'}


def img(name, extra=''):
    return f'<img src="img/{name}.jpg" alt="" loading="lazy" decoding="async"{extra}>'


def add_imgs(html):
    def rep(m):
        tag, cls, rest, ph = m.group(1), m.group(2), m.group(3), m.group(4)
        if 'has-img' in cls:
            return m.group(0)
        sku = re.search(r'href="product-([0-9]{2}-[a-z]+)\.html"', rest)
        if tag == 'a' and 'img' in cls.split() and sku:
            return f'<{tag} class="{cls} has-img pack"{rest} data-ph="{ph}">' + img('zya-' + sku.group(1) + '-1')
        if ph in PH_IMG:
            return f'<{tag} class="{cls} has-img"{rest} data-ph="{ph}">' + img(PH_IMG[ph])
        return m.group(0)
    return re.sub(r'<(div|a) class="([^"]*\bph\b[^"]*)"([^>]*?) data-ph="([^"]*)">', rep, html)


def page(fname, title, desc, body, active=''):
    open(fname, 'w', encoding='utf-8').write(add_imgs(head(title, desc) + header(active) + body + '\n' + FOOTER.replace('__VER__', VER)))
    print('ok', fname)


def swatch_dots(model, sel_sku):
    out = ''
    for s, m, c, _, hexc, *_ in PRODUCTS:
        if m != model:
            continue
        cls = ' class="sel"' if s == sel_sku else ''
        out += f'<a{cls} href="product-{s}.html" title="{c}" style="--c:{hexc}"></a>'
    return out


def card(sku, ph=None):
    s, m, c, _, hexc, art, badge = next(p for p in PRODUCTS if p[0] == sku)
    ph = ph or f'Предметка 4:5 · № {m} {c.lower()}, бежевая драпировка'
    b = f'<span class="badge">{badge}</span>' if badge else ''
    return f'''<div class="card"><a class="img ph" href="product-{s}.html" data-ph="{ph}">{b}<div class="num"><i>№</i><b>{m}</b></div></a>
      <div class="info"><a class="name" href="product-{s}.html">№ {m} Массажная расчёска {c}</a>
      <div class="sw sw-l">{swatch_dots(m, s)}</div></div></div>
'''


# ---------- Отзывы: реальные, из выгрузки Wildberries (../отзывы/make_reviews.py → reviews.json) ----------
import json as _json
REV = _json.load(open('reviews.json', encoding='utf-8'))
fmt_n = lambda n: f'{n:,}'.replace(',', '\u00a0')
fmt_d = lambda d: f'{d[8:10]}.{d[5:7]}.{d[2:4]}'
def _word(n):
    n10, n100 = n % 10, n % 100
    return 'отзыв' if n10 == 1 and n100 != 11 else 'отзыва' if 2 <= n10 <= 4 and not 12 <= n100 <= 14 else 'отзывов'
def rev_card(r):
    return (f'<div class="rev"><div class="top"><span>{r["name"]}</span><span class="stars">★★★★★</span></div>'
            f'<div class="txt">{r["text"]}</div></div>')


# ---------- Главная ----------
home = open('src/home.html', encoding='utf-8').read().replace('<a class="ulink" href="#">Все отзывы</a>', '<a class="ulink" href="reviews.html">Все отзывы</a>')
_a = REV['all']
home = re.sub(r'<div class="rate">.*?</div>', f'<div class="rate">{str(_a["avg"]).replace(".", ",")} <span class="stars">★★★★★</span> ({fmt_n(_a["n"])} {_word(_a["n"])})</div>', home, count=1, flags=re.S)
home = re.sub(r'(<div class="revs">).*?(</div>\s*<div class="arrows")', lambda m: m.group(1) + ''.join(rev_card(r) for r in REV['home']) + '\n  </div>\n  <div class="arrows"', home, count=1, flags=re.S)
page('index.html', 'SANDÓVICH · массажные расчёски, которые не прячут',
     'Массажные расчёски SANDÓVICH: две модели, шесть цветов. Продаются в Золотом Яблоке.', home)


# ---------- Карточка товара ----------
def product(sku):
    s, m, c, _, hexc, art, badge = next(p for p in PRODUCTS if p[0] == sku)
    md = MODEL[m]
    tiles = ''
    for s2, m2, c2, _, hex2, *_ in PRODUCTS:
        if m2 != m:
            continue
        cls = ' class="on"' if s2 == s else ''
        tiles += f'<a{cls} href="product-{s2}.html" title="{c2}"><span style="background:{hex2}"></span></a>'
    g = GALLERY[s]
    gal = lambda name, pack=False: f'<div class="ph has-img{" pack" if pack else ""}">{img(name)}</div>'
    acc = [
        ('Описание', DESC[s]),
        ('Как пользоваться', HOWTO[m]),
        ('Материалы', 'Корпус: крашеный ABS-пластик. Щетина: нейлон, кончики закруглены.'),
        ('Уход', 'Волосы со щетины лучше снимать сразу. Мыть расчёску можно целиком: тёплая вода, немного шампуня, мягкая щётка между рядами. Сохнет щетиной вниз, вдали от батареи и солнца.'),
        ('Где купить', 'В магазинах Золотого Яблока и на goldapple.ru. Каждая расчёска продаётся в фирменной коробке.'),
    ]
    rs = REV['sku'][s]['stats']
    accs = ''.join(f'<details class="pacc"><summary><span class="pl">+</span>{t}</summary><div class="a">{a}</div></details>' for t, a in acc)
    others = [p[0] for p in PRODUCTS if p[0] != s][:4]
    body = f'''<nav class="crumbs page"><a href="index.html">Главная</a><span>›</span><a href="catalog.html">Расчёски</a><span>›</span><span>№ {m} Массажная расчёска {c}</span></nav>
<section class="pdp page">
  <div class="gallery">
    <div class="g2">{gal(f'zya-{s}-1', True)}{gal(f'zya-{s}-4')}</div>
    <div class="g3">{gal(f'zya-{s}-2')}{gal(f'zya-{s}-3')}{gal(f'zya-{s}-5')}</div>
  </div>
  <aside class="buy"><div class="buy-in">
    <div class="prate">{str(rs["avg"]).replace(".", ",")} <span class="stars">★★★★★</span> <a href="#reviews" class="ulink">{fmt_n(rs["n"])} {_word(rs["n"])}</a></div>
    <div class="ptitle"><div class="num"><i>№</i><b>{m}</b></div><h1>№ {m} Массажная расчёска {c}</h1></div>
    
    <div class="tiles">{tiles}</div>
    <a class="btn btn-black zya" href="#" data-sku="{art}">Купить в Золотом Яблоке</a>
    <p class="pnote">Артикул {art} · в фирменной коробке</p>
    <div class="stories">{''.join(f'<div class="st"><div class="ph" data-ph="Видео"></div><span>{t}</span></div>' for t in ['Как расчёсываться', 'Шесть цветов', 'Упаковка', 'Отзывы'])}</div>
    <div class="pdiag"><p><b>Сомневаетесь в цвете?</b></p><p>Подбор по цветотипу: пара вопросов о вас.</p><a class="btn btn-outline" href="quiz.html">Пройти подбор</a></div>
    <div class="paccs">{accs}</div>
  </div></aside>
</section>
<section class="s-full" style="padding-top:60px">
  <div class="wrap"><div class="ph dark" data-ph="Фото 1440×576 · модель расчёсывает волосы, движение"></div>
  <div class="ov"><div class="w64">Какая расчёска ваша?</div><a class="btn btn-line" href="quiz.html" style="margin-top:8px">Подобрать</a></div></div>
</section>
<section class="rsum page" id="reviews">
  <div class="rs-avg"><b>{str(rs["avg"]).replace(".", ",")}</b><div><span class="stars">★★★★★</span><p>{fmt_n(rs["n"])} {_word(rs["n"])}</p></div></div>
  <div class="rs-bars">{''.join(f'<div><span>{k} ★</span><i><em style="width:{round(100 * rs["dist"][str(k)] / rs["n"])}%"></em></i><span>{fmt_n(rs["dist"][str(k)])}</span></div>' for k in (5, 4))}</div>
  <div class="rs-cta"><a class="btn btn-black zya" href="#" data-sku="{art}">Купить в Золотом Яблоке</a></div>
</section>
<section class="rlist page">{''.join(f'<div class="ritem"><div class="rh"><b>{r["name"]}</b><span class="stars">★★★★★</span></div><p>{r["text"]}</p></div>' for r in REV["sku"][s]["reviews"])}</section>
<section class="page" style="padding:60px var(--g) 92px">
  <h2 class="w36" style="text-align:center;margin-bottom:16px">Вам может понравиться…</h2>
  <div class="grid4">{''.join(card(o) for o in others)}</div>
</section>'''
    page(f'product-{s}.html', f'№ {m} Массажная расчёска {c} · SANDÓVICH',
         f'Массажная расчёска SANDÓVICH № {m}, цвет {c.lower()}. Купить в Золотом Яблоке.', body, 'brushes')


for p in PRODUCTS:
    product(p[0])


# ---------- Квиз ----------
QUIZ = [
    ('Цветотип', 'Какой у вас цветотип?', 'Не знаете свой? Выберите «Не знаю», подскажем двумя вопросами.', 'season',
     [('spring', 'Весна', 's-spring'), ('summer', 'Лето', 's-summer'), ('autumn', 'Осень', 's-autumn'), ('winter', 'Зима', 's-winter'), ('unknown', 'Не знаю', 's-unknown')]),
    ('Темп', 'Что про вас?', 'Речь о характере, а не о расписании.', 'model',
     [('01', 'Собираюсь основательно', 'h-long'), ('02', 'Быстро и без суеты', 'h-short'), ('any', 'Бывает по-разному', 'h-any')]),
    ('Подтон', 'Какой металл освежает лицо?', 'Приложите к лицу золотое и серебряное украшение. С каким кожа выглядит свежее?', 'tone',
     [('warm', 'Золото', 'ring-g'), ('cool', 'Серебро', 'ring-s')]),
    ('Контраст', 'Волосы и кожа рядом:', 'Посмотрите на себя без макияжа при дневном свете.', 'depth',
     [('light', 'Светлые, мягкий контраст', 'd-light'), ('deep', 'Тёмные или яркий контраст', 'd-deep')]),
]
QICON = {
    's-spring': '<circle cx="20" cy="32" r="8" fill="#ffefae"/><circle cx="32" cy="32" r="8" fill="#eeb480"/><circle cx="44" cy="32" r="8" fill="#c5a56e"/>',
    's-summer': '<circle cx="20" cy="32" r="8" fill="#f9c1ce"/><circle cx="32" cy="32" r="8" fill="#a5c8d1"/><circle cx="44" cy="32" r="8" fill="#b6bfc1"/>',
    's-autumn': '<circle cx="20" cy="32" r="8" fill="#802626"/><circle cx="32" cy="32" r="8" fill="#d8a37b"/><circle cx="44" cy="32" r="8" fill="#1a7444"/>',
    's-winter': '<circle cx="20" cy="32" r="8" fill="#ab2439"/><circle cx="32" cy="32" r="8" fill="#5a82b3"/><circle cx="44" cy="32" r="8" fill="#111314"/>',
    's-unknown': '<circle cx="32" cy="32" r="14" stroke="#000"/><path d="M27 28a5 5 0 1 1 7 4.6c-1.3.6-2 1.6-2 3V37M32 41v1" stroke="#000"/>',
    'd-light': '<circle cx="26" cy="32" r="10" fill="#f3e3cf"/><circle cx="40" cy="32" r="10" fill="#e8c98f"/>',
    'd-deep': '<circle cx="26" cy="32" r="10" fill="#f3e3cf"/><circle cx="40" cy="32" r="10" fill="#2a1d18"/>',
    'ring-g': '<circle cx="32" cy="32" r="14" stroke="#B08A3E" stroke-width="3"/>',
    'ring-s': '<circle cx="32" cy="32" r="14" stroke="#A9ABB0" stroke-width="3"/>',
    'ring-r': '<circle cx="32" cy="32" r="14" stroke="#B4785A" stroke-width="3"/>',
    'ring-0': '<circle cx="32" cy="32" r="14" stroke="#000" stroke-width="1"/><path d="M22 42 42 22" stroke="#000"/>',
    'h-long': '<rect x="29" y="12" width="6" height="40" rx="3" stroke="#000"/>',
    'h-short': '<rect x="26" y="20" width="12" height="26" rx="5" stroke="#000"/>',
    'h-any': '<rect x="22" y="14" width="5" height="36" rx="2.5" stroke="#000"/><rect x="34" y="22" width="10" height="22" rx="4" stroke="#000"/>',
    'p-table': '<path d="M16 36h32M20 36v12M44 36v12M27 36V22h10v14" stroke="#000"/>',
    'p-bag': '<path d="M20 26h24l-2 20H22l-2-20zM27 26v-3a5 5 0 0 1 10 0v3" stroke="#000"/>',
    'p-bath': '<path d="M16 34h32v4a8 8 0 0 1-8 8H24a8 8 0 0 1-8-8v-4zM22 34V20a4 4 0 0 1 8 0" stroke="#000"/>',
    'p-gift': '<path d="M18 28h28v18H18zM16 22h32v6H16zM32 22v24M32 22c-3-6-10-6-8-1M32 22c3-6 10-6 8-1" stroke="#000"/>',
    'c-red': '<circle cx="32" cy="32" r="12" fill="#9E1B2A"/>',
    'c-nude': '<circle cx="32" cy="32" r="12" fill="#D9B8A3"/>',
    'c-black': '<circle cx="32" cy="32" r="12" fill="#111"/>',
    'c-pink': '<circle cx="32" cy="32" r="12" fill="#EBA3C3"/>',
}
qblocks = ''
for title, q, hint, name, opts in QUIZ:
    o = ''.join(f'<label class="qo"><input type="radio" name="{name}" value="{v}"><span class="qi"><svg viewBox="0 0 64 64" fill="none">{QICON[ic]}</svg></span><span class="ql">{t}</span></label>' for v, t, ic in opts)
    helper = ' qhelp" hidden data-help="1' if name in ('tone', 'depth') else ''
    qblocks += f'<fieldset class="qb{helper}"><legend class="w30">{title}</legend><p class="qq">{q}</p><p class="qh">{hint}</p><div class="qopts">{o}</div></fieldset>'
quiz_body = f'''<section class="quiz">
  <div class="qimg"><div class="ph dark" data-ph="Фото 585×877 · модель в очках, расчёска у головы, ироничный editorial"></div><p class="w56">Ваш характер</p></div>
  <form class="qform" id="quiz">{qblocks}
    <div class="qres" id="qres" hidden>
      <p class="qq">Ваша расчёска:</p>
      <div class="qres-card">
        <a class="img ph has-img pack" id="qr-img" href="#"><img id="qr-pic" src="img/zya-01-gold-1.jpg" alt=""><div class="num"><i>№</i><b id="qr-num">01</b></div></a>
        <div><p class="w30" id="qr-name">№ 01 Золото</p><p class="qh" id="qr-why"></p>
        <p class="qh" id="qr-alt" hidden>Ещё подойдёт: <a class="ulink" id="qr-alt-a" href="#"></a></p>
        <a class="btn btn-black zya" id="qr-buy" href="#">Купить в Золотом Яблоке</a>
        <a class="ulink" id="qr-more" href="#" style="display:inline-block;margin-top:18px">Подробнее о расчёске</a></div>
      </div>
    </div>
  </form>
</section>'''
page('quiz.html', 'Подбор расчёски · SANDÓVICH', 'Подбор по цветотипу: подскажем, какой цвет SANDÓVICH ваш.', quiz_body, 'quiz')


# ---------- Каталог ----------
stories = ''.join(f'<a class="story" href="product-{s}.html"><div class="ph has-img pack">{img("zya-" + s + "-1")}</div><span>№ {m} {c}</span></a>' for s, m, c, *_ in PRODUCTS)
cat_cards = [card(p[0]) for p in PRODUCTS]
editorial = '<div class="card ed"><div class="ph" data-ph="Фото 692×1035 · модель с расчёской, editorial (вставка на 2 колонки)"></div></div>'
grid = cat_cards[0] + cat_cards[1] + editorial + cat_cards[2] + cat_cards[3] + cat_cards[4] + cat_cards[5]
cat_body = f'''<nav class="crumbs page"><a href="index.html">Главная</a><span>›</span><span>Расчёски</span></nav>
<section class="cat page">
  <h1 class="w56c">Вся коллекция</h1>
  <div class="stories-row">{stories}</div>
  <div style="text-align:center"><a class="btn btn-black" href="quiz.html" style="width:271px;height:36px">Подобрать свою</a></div>
  <div class="ctabs"><a class="on" href="#all" data-f="all">Все расчёски</a><a href="#m01" data-f="01">Модель № 01</a><a href="#m02" data-f="02">Модель № 02</a><a href="#gift" data-f="gift">В подарок</a></div>
  <div class="cbar"><span>Фильтр</span><span class="sort">Сортировка: <b>Рекомендуем</b></span><span class="cnt" id="cnt">6 расчёсок</span></div>
  <div class="cgrid" id="cgrid">{grid}</div>
</section>'''
page('catalog.html', 'Расчёски SANDÓVICH · каталог', 'Все массажные расчёски SANDÓVICH: модели № 01 и № 02, шесть цветов.', cat_body, 'brushes')
print(ZYA_NOTE)


# ---------- Все отзывы (4–5 звёзд, тексты дословно) ----------
_all = open('reviews-all.json', encoding='utf-8').read().replace('</', '<\\/')
_tabs = ''.join(f'<a href="#" data-r="{k}"{" class=\"on\"" if k == "all" else ""}>{t}</a>' for k, t in
                [('all', 'Все')] + [(sk, f'№ {m} {c}') for sk, m, c, *_ in PRODUCTS])
rev_body = f'''<nav class="crumbs page"><a href="index.html">Главная</a><span>›</span><span>Отзывы</span></nav>
<section class="rv page">
  <h1 class="w56c">Отзывы</h1>
  <div class="rate rv-rate">{str(REV["all"]["avg"]).replace(".", ",")} <span class="stars">★★★★★</span> ({fmt_n(REV["all"]["n"])} {_word(REV["all"]["n"])})</div>
  <div class="ctabs rv-tabs">{_tabs}</div>
  <div class="rlist" id="rvlist"></div>
  <div style="text-align:center"><button class="btn btn-outline" id="rvmore" type="button">Показать ещё</button></div>
</section>
<script type="application/json" id="rvdata">{_all}</script>'''
page('reviews.html', 'Отзывы · SANDÓVICH', 'Что пишут покупательницы о массажных расчёсках SANDÓVICH.', rev_body)
