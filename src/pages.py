"""Pages of the HomePilates site. Texts come verbatim from the ТЗ via data/content.json;
the layout and visual system are this project's own (Atlas of movement)."""
import json
from html import escape as esc
from pathlib import Path
from urllib.parse import urlencode

from reformer import illustration

ROOT = Path(__file__).resolve().parents[1]
DATA = json.loads((ROOT / 'data/content.json').read_text(encoding='utf-8'))
LABEL = DATA['labels']
C = DATA['contacts']
LEGAL = DATA['legal']
INTEGR = DATA['integrations']
MISS = DATA['placeholder']

# route, menu label (as in ТЗ), page heading, description (ТЗ text of the page)
PAGES = [
    ('/', DATA['pages'][''], DATA['pages'][''], DATA['seo']['']),
    ('/napravleniya', DATA['pages']['napravleniya'], DATA['pages']['napravleniya'], DATA['seo']['napravleniya']),
    ('/raspisanie', DATA['pages']['raspisanie'], DATA['pages']['raspisanie'], DATA['seo']['raspisanie']),
    ('/stoimost', DATA['pages']['stoimost'], DATA['pages']['stoimost'], DATA['seo']['stoimost']),
    ('/komanda', DATA['pages']['komanda'], DATA['pages']['komanda'], DATA['seo']['komanda']),
    ('/faq', DATA['pages']['faq'], DATA['pages']['faq'], DATA['seo']['faq']),
    ('/sertifikaty', DATA['pages']['sertifikaty'], DATA['pages']['sertifikaty'], DATA['seo']['sertifikaty']),
    ('/kontakty', DATA['pages']['kontakty'], DATA['pages']['kontakty'], DATA['seo']['kontakty']),
    ('/cabinet', LABEL['account'], LABEL['account'],
     'Записывайтесь сами или меняйте запись в личном кабинете – без звонков и переписок.'),
]
TITLES = dict(DATA['titles'], cabinet=LABEL['account'] + ' — HomePilates')
BOOK = '/raspisanie'


def digits(phone):
    return ''.join(ch for ch in phone if ch.isdigit())


PHONE = 'tel:+' + digits(C['phone'])
WHATSAPP = 'https://wa.me/' + digits(C['messengerPhone'])


def arrow(symbol='↗'):
    return f'<span class="arrow" aria-hidden="true">{symbol}</span>'


def btn(label, url, secondary=False, cls=''):
    return f'<a class="btn{" secondary" if secondary else ""}{" " + cls if cls else ""}" href="{esc(url)}">{esc(label)}{arrow()}</a>'


def textlink(label, url, symbol='↗'):
    return f'<a class="textlink" href="{esc(url)}">{esc(label)} {arrow(symbol)}</a>'


def section_label(number, label):
    return f'<div class="eyebrow"><span class="index">{number}</span>{esc(label)}</div>'


def p(text, cls=''):
    return f'<p{" class=" + chr(34) + cls + chr(34) if cls else ""}>{esc(text)}</p>'


def missing():
    return f'<span class="missing">{MISS}</span>'


def first_sentence(text):
    head, _, rest = text.partition('. ')
    return (head + '.', rest) if rest else (text, '')


def title(num, kicker, heading, desc):
    return (f'<div class="page-intro wrap">{section_label(num, kicker)}<h1>{esc(heading)}</h1>'
            f'<p class="lede">{esc(desc)}</p></div>')


LOGO = Path(__file__).with_name('logo.svg').read_text(encoding='utf-8').strip()


def wordmark():
    return f'<a class="wordmark" href="/" aria-label="Хоум Пилатес — главная">{LOGO}</a>'


def navlink(page, route):
    url, label, *_ = page
    current = ' aria-current="page"' if url == route else ''
    return f'<a href="{url}"{current}>{esc(label)}</a>'


def header(route):
    primary = ''.join(navlink(p_, route) for p_ in PAGES[1:8])
    all_pages = ''.join(navlink(p_, route) for p_ in PAGES)
    return f'''<a class="skip" href="#content">К содержанию</a><header class="header"><div class="wrap headbar">
    {wordmark()}<nav class="quick" aria-label="Основные разделы">{primary}</nav>
    <div class="head-actions"><a class="cab-link" href="/cabinet">{esc(LABEL['account'])}</a>{btn(LABEL['book'], BOOK)}
    <details class="menu"><summary aria-controls="hp-nav" aria-label="Меню разделов"><span class="menu-lines" aria-hidden="true"></span><span class="menu-word">{esc(LABEL['menu'])}</span></summary>
    <nav id="hp-nav" aria-label="Все разделы">{all_pages}</nav></details></div></div></header>'''


def social(cls='social'):
    icons = {
        'vk': 'M2 5h3.6c.4 5 2.7 8 4.7 8.7V5H14v5.1c2-.2 4.1-2.6 4.9-5.1h3.5c-.7 3.2-3 5.7-4.7 6.8 1.7.9 4.3 3.1 5.1 6.7h-3.9c-.9-2.3-2.6-4.1-4.9-4.4v4.4h-.6C6.1 18.5 2.5 13.5 2 5Z',
        'telegram': 'M21.8 3.2 18.3 20c-.3 1.2-1 1.5-2 .9l-5.4-4-2.6 2.5.4-5.6L18.9 5.9 6.3 12.6l-4.8-1.5c-1-.3-1-1 .2-1.5L20.4 2.5c.9-.3 1.6.1 1.4.7Z',
    }
    return f'<div class="{cls}">' + ''.join(
        f'<a aria-label="{esc(LABEL[key])}" href="{esc(C[key])}"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="{d}"/></svg></a>'
        for key, d in icons.items()) + '</div>'


def max_value():
    if C['maxUrl']:
        return f'<a href="{esc(C["maxUrl"])}">{esc(C["messengerPhone"])}</a>'
    return f'{esc(C["messengerPhone"])}{missing()}'


def consent():
    start, end = LEGAL['consent'].rsplit(' ', 1)
    return (f'<label class="check"><input type="checkbox" name="{esc(LABEL["approval"])}" '
            f'value="{esc(LEGAL["consent"])}" required><span>{esc(start)} '
            f'<a href="{esc(LEGAL["policy"])}">{esc(end)}</a></span></label>')


def footer(route):
    terms = ''.join(f'<dt>{esc(k)}</dt><dd>{esc(v)}</dd>' for k, v in LEGAL['requisites'].items())
    # In the footer MAX is a plain number until the studio sends the link; the [уточнить] mark stays on /kontakty
    max_number = f'<a href="{esc(C["maxUrl"])}">{esc(C["messengerPhone"])}</a>' if C['maxUrl'] else esc(C['messengerPhone'])
    lines = ''.join(f'<dt>{esc(label)}</dt><dd>{value}</dd>' for label, value in (
        (LABEL['phone'], f'<a href="{PHONE}">{esc(C["phone"])}</a>'),
        (C['whatsappLabel'], f'<a href="{WHATSAPP}">{esc(C["messengerPhone"])}</a>'),
        (LABEL['max'], max_number)))
    contacts = (f'<div class="foot-contacts"><span class="foot-title">Связь</span><dl>{lines}</dl>'
                f'<div class="fc-actions"><a class="fc-btn" href="{esc(C["bot"])}">{esc(LABEL["footerBot"])}{arrow()}</a>'
                f'<a class="fc-btn" href="/kontakty#feedback">{esc(LABEL["feedback"])}{arrow("→")}</a></div></div>')
    studio = f'<div class="foot-studio">{wordmark()}<p>{esc(C["address"])}<br>{esc(C["hours"])}</p>{social()}</div>'
    links = ''.join(navlink(p_, route) for p_ in PAGES[1:])
    return f'''<footer><div class="wrap footgrid">{studio}
    <nav aria-label="Разделы в подвале"><span class="foot-title">Разделы</span><div class="foot-links">{links}</div></nav>{contacts}</div>
    <div class="wrap legal"><details><summary>{esc(LABEL['requisites'])}</summary><dl>{terms}</dl></details>
    <div class="policy-links"><a href="{esc(LEGAL['policy'])}">{esc(LABEL['policy'])}</a><a href="{esc(LEGAL['approval'])}">{esc(LABEL['approval'])}</a>
    <button type="button" class="linklike" data-cookie-open>{esc(LABEL['cookie'])}</button></div></div></footer>'''


def cookie_box():
    cfg = DATA['cookie']
    names = ['essential-cookie', 'analytics', 'ads']
    opts = ''.join(f'<label class="check"><input type="checkbox" name="{name}"{" checked disabled" if i == 0 else ""}>'
                   f'<span>{esc(text)}</span></label>' for i, (name, text) in enumerate(zip(names, cfg['categories'])))
    return (f'<form class="cookie-box" aria-label="{esc(LABEL["cookie"])}" hidden><p>{esc(cfg["intro"])}</p>'
            f'<details><summary>{esc(LABEL["categories"])}</summary><div class="cookie-opts">{opts}</div></details>'
            f'<div class="cookie-foot"><button class="linklike" name="essential">{esc(LABEL["essentialOnly"])}</button>'
            f'<button class="btn" name="save">{esc(LABEL["save"])}</button></div></form>')


def widget(kind, section=''):
    """Mobifitness widget, shown at once: Mobifitness asks for consent in its own sign-up and booking forms."""
    cfg = INTEGR['mobifitness']
    params = dict(code=cfg['code'], club=cfg['club'], type=kind, language='ru', version='v6', host=cfg['domain'])
    if section:
        params['section'] = section
    url = f'https://{cfg["domain"]}/{kind}-widget/?' + urlencode(params)
    standalone = url + ('#' + section if section else '')
    name = DATA['pages']['raspisanie'] if kind == 'schedule' else LABEL['account']
    return (f'<div class="mobi" id="hp-mobi" data-code="{cfg["code"]}" data-club="{cfg["club"]}" data-type="{kind}" '
            f'data-section="{esc(section)}" data-url="{esc(url)}" data-title="{esc(name)}"></div>'
            f'{textlink(LABEL["mobiOpen"], standalone)}')


def numbered(items):
    return '<ol class="steps">' + ''.join(
        f'<li><span class="serial">{i:02d}</span><span>{esc(x)}</span></li>' for i, x in enumerate(items, 1)) + '</ol>'


def home(_prices=None):
    h = DATA['home']
    fig = f'''<figure class="plate"><div class="plate-top"><span>АТЛАС ДВИЖЕНИЯ</span><span>ЛИСТ 01 / 01</span></div>
    {illustration()}<figcaption><span><b>Реформер</b><small>01 Каретка · 02 Упор · 03 Ремни</small></span><span>Схема<br>Фиг. 01</span></figcaption></figure>'''
    head, tagline = h['title'].split(' — ', 1)
    why_big, why_rest = first_sentence(h['why'])
    who = ''.join(f'<div class="dir-link static"><small>0{i}</small><span>{esc(x)}</span></div>' for i, x in enumerate(h['who'], 1))
    routes = ''.join(f'<a class="dir-link" href="/napravleniya#napr-{i}"><small>0{i}</small><span>{esc(d["title"])}</span>{arrow()}</a>'
                     for i, d in enumerate(DATA['directions']['items'][:5], 1))
    trial_rows = {row[0]: row for row in DATA['prices']['groups'][0]['rows']}
    trial = ''.join(f'<a class="trial" href="/stoimost#category-1"><span>{esc(name)}</span><b>{esc(trial_rows[name][2])}</b>{arrow()}</a>'
                    for name in ('Пилатес-знакомство (в группе)', 'Пилатес-знакомство (индивид.)'))
    tiles = ''.join(f'<a class="tile" href="{url}"><small>0{i}</small><span>{esc(label)}</span>{arrow()}</a>'
                    for i, (url, label, *_) in enumerate(PAGES[1:], 1))
    reviews_url = 'https://yandex.ru/maps-reviews-widget/' + INTEGR['organization'] + '?comments'
    cta_head, cta_rest = first_sentence(h['cta'])
    return f'''<section class="hero wrap"><div class="hero-text"><div class="eyebrow"><i class="dot"></i>{esc(LABEL['brandPlace'])}</div>
    <h1>{esc(head)} <span class="tagline">— {esc(tagline)}</span></h1>
    <p class="lede">{esc(h['intro'])}</p><p class="trial-note">{esc(h['trial'])}</p>
    <div class="actions">{btn(LABEL['book'], BOOK)}{textlink(DATA['pages']['stoimost'], '/stoimost', '→')}</div></div>{fig}</section>
    <section class="facts"><div class="wrap factgrid"><div><small>Продолжительность</small><strong>60 минут</strong></div><div><small>Ближайшее метро</small><strong>Ботанический сад</strong></div><div><small>Студия открыта</small><strong>08:00 — 21:00</strong></div></div></section>
    <section class="section wrap split"><div>{section_label('01', 'Студия')}<h2>{esc(h['whyTitle'])}</h2></div>
    <div class="copy">{p(why_big, 'big')}{p(why_rest) if why_rest else ''}</div></section>
    <section class="section tint"><div class="wrap split"><div>{section_label('02', 'Практика')}<h2>{esc(h['whoTitle'])}</h2></div><div>{who}</div></div></section>
    <section class="section wrap split"><div>{section_label('03', 'Занятие')}<h2>{esc(h['lessonTitle'])}</h2><p>{esc(h['lesson'])}</p></div>
    <div>{numbered(h['steps'])}</div></section>
    <section class="quote-band"><div class="wrap"><blockquote>{esc(h['quote'])}</blockquote><cite>{esc(h['author'])}</cite></div></section>
    <section class="section tint"><div class="wrap split"><div>{section_label('04', DATA['pages']['napravleniya'])}<h2>{esc(DATA['pages']['napravleniya'])}</h2></div><div>{routes}</div></div></section>
    <section class="section wrap split"><div>{section_label('05', DATA['pages']['stoimost'])}<h2>{esc(DATA['prices']['groups'][0]['title'])}</h2></div>
    <div>{trial}{btn(DATA['pages']['stoimost'], '/stoimost', True)}</div></section>
    <section class="section tint"><div class="wrap split"><div>{section_label('06', LABEL['reviews'])}<h2>{esc(LABEL['reviews'])}</h2>
    <div class="actions">{textlink(LABEL['maps'], INTEGR['map'] + 'reviews/')}</div></div>
    <iframe class="reviews" title="{esc(LABEL['reviews'])}" loading="lazy" src="{reviews_url}"></iframe></div></section>
    <nav class="section wrap tiles" aria-label="Все разделы">{tiles}</nav>
    <aside class="join" id="cabinet"><div class="wrap join-grid"><div>{section_label('HP', LABEL['account'])}<h2>{esc(cta_head)}</h2>{p(cta_rest) if cta_rest else ''}</div>
    <div class="join-widget">{widget('personal')}</div></div></aside>'''


def directions():
    d = DATA['directions']
    rows = []
    for i, item in enumerate(d['items'], 1):
        pending = item['title'] == MISS
        body = (f'<p class="pending">{esc(LABEL["directionPending"])}</p>' if pending else p(item['text']))
        rows.append(f'''<article id="napr-{i}" class="directory-row{" is-pending" if pending else ""}"><div class="serial">0{i}</div><div><h2>{esc(item['title'])}</h2>{body}</div>
        <a class="textlink" href="{BOOK}" aria-label="{esc(LABEL['book'])} — {esc(item['title'])}">{esc(LABEL['book'])} {arrow()}</a></article>''')
    return title('01', 'Практика', DATA['pages']['napravleniya'], d['intro']) + f'<section class="wrap list-section">{"".join(rows)}</section>'


def schedule():
    s = DATA['schedule']
    return title('02', 'Запись', DATA['pages']['raspisanie'], s['intro']) + f'''<div class="wrap widget-section">{widget('schedule')}</div>
    <div class="wrap panels single"><aside class="side-card">{section_label('24 ч', LABEL['account'])}<p class="big">{esc(s['rule'])}</p>
    {btn(LABEL['account'], '/cabinet', True)}</aside></div>'''


def pricing(_rows=None):
    data = DATA['prices']
    blocks = []
    for i, group in enumerate(data['groups'], 1):
        cols = data['singleColumns'] if i == 1 else data['columns']
        items = []
        for row in group['rows']:
            cells = dict(zip(cols, row))
            info = [cells.get('Описание') or cells.get('Формат', '')]
            if i > 1:
                info += [f'{cols[3]}: {cells[cols[3]]}', f'{cols[4]}: {cells[cols[4]]}']
            items.append(f'<li><div><strong>{esc(cells["Название"])}</strong><small>{" · ".join(esc(x) for x in info)}</small></div>'
                         f'<b>{esc(cells["Цена"])}</b></li>')
        blocks.append(f'''<details id="category-{i}" class="acc"{" open" if i == 1 else ""}><summary aria-controls="plans-{i}"><span class="idx">0{i}</span><span>{esc(group['title'])}</span><i class="plus" aria-hidden="true"></i></summary>
        <div id="plans-{i}"><ul class="prices">{''.join(items)}</ul></div></details>''')
    return title('03', 'Прайс студии', DATA['pages']['stoimost'], data['intro']) + f'''<div class="wrap list-section"><h2 class="list-title">{esc(data['title'])}</h2>{''.join(blocks)}
    <div class="actions">{btn(LABEL['book'], BOOK)}</div></div>
    <div class="wrap panels single"><aside class="side-card">{section_label('!', data['notice'].rstrip(':'))}<h2>{esc(data['notice'])}</h2>{p(data['rule'])}</aside></div>'''


def team():
    t = DATA['team']
    people = sorted(t['people'], key=lambda person: not person.get('lead'))
    rows = []
    for i, person in enumerate(people, 1):
        name = person['name']
        if person.get('photo'):
            pic = f'<img class="portrait" src="/assets/photos/{person["photo"]}.jpg" alt="{esc(name)}" loading="lazy" decoding="async">'
        else:
            initials = ''.join(x[0] for x in name.split())
            pic = (f'<div class="portrait portrait-pending" role="img" aria-label="{esc(LABEL["photo"])}: {esc(name)}">'
                   f'<span class="initials">{initials}</span><small>{esc(LABEL["photoPending"])} {MISS}</small></div>')
        role = f'<p class="role">{esc(person["role"])}</p>' if person.get('role') else ''
        bio = ''.join(p(x) for x in person['bio'])
        rows.append(f'''<article class="person{" person-lead" if person.get("lead") else ""}">{pic}<div><span class="idx">{i:02d} / {len(people):02d}</span>
        <h2>{esc(name)}</h2>{role}<div class="bio">{bio}</div></div></article>''')
    return title('04', 'Студия', DATA['pages']['komanda'], t['intro']) + f'<div class="wrap list-section">{"".join(rows)}</div>'


def faq():
    f = DATA['faq']
    items = ''.join(f'<details class="acc"><summary aria-controls="answer-{i}"><span class="idx">0{i}</span><span>{esc(q)}</span><i class="plus" aria-hidden="true"></i></summary><p id="answer-{i}" class="answer">{esc(a)}</p></details>'
                    for i, (q, a) in enumerate(f['items'], 1))
    return title('05', 'Перед визитом', DATA['pages']['faq'], f['intro']) + f'<div class="wrap list-section">{items}</div>'


def certificates():
    c = DATA['certificates']
    denoms = ''.join(f'<li>{missing() if x == MISS else esc(x)}</li>' for x in c['denominations'])
    return title('06', 'В подарок', DATA['pages']['sertifikaty'], c['intro']) + f'''<div class="wrap panels"><div class="gift"><div class="giftmark" role="img" aria-label="Хоум Пилатес">{LOGO}</div><p>Подарочный<br>сертификат</p><small>HomePilates · Москва</small></div>
    <section class="side-card">{section_label('01', c['how'].rstrip(':'))}<h2>{esc(c['how'])}</h2>{numbered(c['steps'])}</section></div>
    <div class="wrap panels"><section class="side-card">{section_label('02', LABEL['buy'])}<h2>{esc(c['denominationsTitle'])}</h2><ul class="plain">{denoms}</ul>{p(c['end'])}
    <div class="actions">{textlink(LABEL['footerBot'], C['bot'])}</div></section>
    <section class="side-card widget-card">{widget('personal', 'shop/all')}</section></div>'''


def feedback():
    email = esc(C['email'])
    return (f'<form class="feedback" data-feedback="{email}" data-subject="{esc(LABEL["feedback"])}" '
            f'action="mailto:{email}" method="post" enctype="text/plain">'
            f'<label class="field">{esc(LABEL["phone"])}<input type="tel" autocomplete="tel" name="{esc(LABEL["phone"])}" required></label>'
            f'<label class="field">{esc(LABEL["message"])}<textarea rows="3" name="{esc(LABEL["message"])}" required></textarea></label>'
            f'{consent()}<p class="form-note" data-preview-only>{esc(LABEL["feedbackNote"])}</p>'
            f'<button class="btn" type="submit">{esc(LABEL["submit"])}{arrow()}</button></form>')


def contacts():
    map_url = 'https://yandex.ru/map-widget/v1/?' + urlencode(dict(ol='biz', oid=INTEGR['organization'], z='17'))
    apps = ''.join(f'<li>{esc(label)} ' + (f'<a href="{esc(url)}">{esc(url)}</a>' if url else missing()) + '</li>'
                   for label, url in C['stores'].items())
    lines = [
        (C['botLabel'].rstrip(':'), C['bot'], C['bot'].replace('https://', '')),
        (C['whatsappLabel'], WHATSAPP, C['messengerPhone']),
        (LABEL['phone'], PHONE, C['phone']),
        (C['emailLabel'], 'mailto:' + C['email'], C['email']),
    ]
    channels = ''.join(f'<a href="{esc(url)}"><span><small>{esc(label)}</small>{esc(value)}</span>{arrow()}</a>' for label, url, value in lines)
    channels += f'<div class="channel-static"><span><small>{esc(LABEL["max"])}</small>{max_value()}</span></div>'
    return title('07', 'Ботанический сад', DATA['pages']['kontakty'], C['address']) + f'''<div class="wrap panels"><section class="side-card address">{section_label('01', C['addressLabel'].rstrip(':'))}<h2>{esc(C['addressLabel'])}</h2>
    {p(C['address'], 'big')}{p(C['directions'])}{p(C['hours'])}{textlink(LABEL['maps'], INTEGR['map'])}</section>
    <iframe class="map" title="{esc(LABEL['maps'])}" loading="lazy" src="{esc(map_url)}"></iframe></div>
    <div class="wrap panels"><section class="side-card" id="svyaz">{section_label('02', C['booking'].rstrip(':'))}<h2>{esc(C['booking'])}</h2>
    <p class="cap">{esc(C['apps'])}</p><ul class="plain">{apps}</ul><div class="channels">{channels}</div>
    <p class="cap">{esc(LABEL['social'])}</p>{social()}<p class="insta">{esc(C['instagramLabel'])} <a href="{esc(C['instagram'])}">{esc(C['instagram'])}</a></p><p class="note">{esc(C['instagramNote'])}</p></section>
    <section class="side-card" id="feedback">{section_label('03', LABEL['feedback'])}<h2>{esc(LABEL['formTitle'])}</h2>{feedback()}</section></div>'''


def cabinet():
    return title('08', 'Клиентам студии', LABEL['account'], PAGES[-1][3]) + f'<div class="wrap widget-section">{widget("personal")}</div>'
