from collections import defaultdict
from html import escape as esc
from urllib.parse import quote

from reformer import illustration

# route, navigation label, page title, description
PAGES = [
    ('/', 'Главная', 'Пилатес на реформерах у Ботанического сада', 'Пробные занятия на реформере в мини-группе и индивидуально в студии HomePilates в Москве.'),
    ('/napravleniya', 'Направления', 'Направления занятий на реформере', 'Пять направлений студии HomePilates, от классического пилатеса до персональных тренировок.'),
    ('/raspisanie', 'Расписание', 'Расписание и запись на пилатес', 'Как узнать свободное время, выбрать занятие и договориться о переносе с администратором HomePilates.'),
    ('/stoimost', 'Стоимость', 'Стоимость занятий и абонементов', 'Итоговые цены пробных занятий, разовых посещений и абонементов HomePilates по категориям.'),
    ('/komanda', 'Команда', 'Тренеры студии пилатеса', 'Команда HomePilates у Ботанического сада и связь со студией для выбора тренера.'),
    ('/faq', 'Вопросы', 'Вопросы о первом занятии', 'Как подготовиться к пилатесу, что взять с собой и как изменить время записи.'),
    ('/sertifikaty', 'Сертификаты', 'Подарочные сертификаты на пилатес', 'Варианты подарочных занятий и контакт администратора HomePilates для уточнения условий.'),
    ('/kontakty', 'Контакты', 'Адрес и контакты студии', 'Как найти HomePilates в проезде Серебрякова, позвонить в студию и связаться с администратором.'),
    ('/cabinet', 'Личный кабинет', 'Личный кабинет клиента HomePilates', 'Статус онлайн-кабинета и связь с администратором по вопросам абонемента и записи.')
]
PHONE = 'tel:+79053058779'
TG = 'https://t.me/Home_Pilates_bot'
MAP = 'https://yandex.ru/maps/?text=' + quote('Москва, проезд Серебрякова, 2 корпус 1')
CONTACT = '/kontakty#svyaz'
DIRECTIONS = [
    ('Классический пилатес на реформере', 'Всё тело', 'Каретка скользит по направляющим, а пружины задают сопротивление. На занятии чередуются упражнения для рук, ног и корпуса.', 'classic'),
    ('Здоровая спина', 'Техника', 'Спокойное занятие с вниманием к положению корпуса и качеству каждого движения.', 'spina'),
    ('Восстановление после родов', 'Возвращение к движению', 'Индивидуальные ограничения и сроки возвращения к нагрузке обсудите с врачом. Администратор поможет уточнить формат занятия.', 'posle-rodov'),
    ('Стретчинг и шпагаты', 'Гибкость', 'Работа с амплитудой движения и растяжкой, в том числе на тренажёре кадиллак.', 'stretch'),
    ('Персональные тренировки', 'Один на один', 'Занятие с тренером вокруг вашего запроса. Вместе вы подбираете упражнения, темп и нагрузку.', 'personal')
]
TEAM = ['Анастасия Шалимова','Лидия Калашникова','Татьяна Негреева','Лев Зайцев','Марина Щепотина']
FAQ = [
    ('Можно ли начать без подготовки?', 'Да. Для знакомства с реформером можно выбрать пробное в мини-группе или персональную тренировку. Скажите администратору, что вы идёте впервые.'),
    ('Что делать, если болит спина или шея?', 'Обсудите возможность занятий с врачом до записи. Если врач уже дал рекомендации по нагрузке, сообщите об ограничениях тренеру.'),
    ('Чем реформер отличается от коврика?', 'На реформере есть подвижная платформа, пружины и ремни. На коврике вы работаете на неподвижной поверхности.'),
    ('Когда я замечу результат?', 'Темп изменений индивидуален. На первой встрече можно обсудить с тренером, какие движения вы хотите освоить и как отслеживать прогресс.'),
    ('Что взять на занятие?', 'Выберите удобную одежду, в которой легко двигаться. Требования к носкам и другим принадлежностям уточните при записи.'),
    ('Можно ли заниматься во время беременности и после родов?', 'Сначала обсудите нагрузку с наблюдающим врачом. Затем уточните у студии доступный формат с учётом рекомендаций.'),
    ('Как отменить или перенести запись?', 'Сообщите студии не позднее чем за 24 часа до начала занятия. Администратор уточнит варианты переноса.'),
    ('Могут ли заниматься мужчины?', 'Да. Выбирайте групповое или персональное занятие исходя из своих целей и предпочтений.')
]


def arrow(symbol='↗'):
    return f'<span class="arrow" aria-hidden="true">{symbol}</span>'


def btn(label, url, secondary=False):
    return f'<a class="btn{" secondary" if secondary else ""}" href="{esc(url)}">{label}{arrow()}</a>'


def section_label(number, label):
    return f'<div class="eyebrow"><span class="index">{number}</span>{label}</div>'


def title(num, kicker, heading, desc):
    return f'<div class="page-intro wrap">{section_label(num,kicker)}<h1>{heading}</h1><p class="lede">{desc}</p></div>'


def mark():
    return '''<svg viewBox="0 0 40 36" width="40" height="36" aria-hidden="true"><g fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round"><path d="M2 29c4-1 7-6 11-15S22 2 28 3c4 1 5 5 3 9l-8 16c-3 6-11 7-12 1-1-5 6-12 13-14s12-1 13 2c2 5-6 11-15 11"/></g></svg>'''


def wordmark():
    return f'<a class="wordmark" href="/" aria-label="HomePilates — главная">{mark()}<span>HomePilates</span></a>'


def navlink(page, route):
    url, label, *_ = page
    current = ' aria-current="page"' if url==route else ''
    return f'<a href="{url}"{current}>{label}</a>'


def header(route):
    primary = ''.join(navlink(PAGES[i],route) for i in (1,2,3,4))
    all_pages = ''.join(navlink(p,route) for p in PAGES)
    return f'''<a class="skip" href="#content">К содержанию</a><header class="header"><div class="wrap headbar">
    {wordmark()}<nav class="quick" aria-label="Основные разделы">{primary}</nav>
    <div class="head-actions">{btn('Записаться',CONTACT)}
    <details class="menu"><summary aria-controls="hp-nav" aria-label="Меню разделов"><span class="menu-lines" aria-hidden="true"></span><span class="menu-word">Меню</span></summary>
    <nav id="hp-nav" aria-label="Все разделы">{all_pages}</nav></details></div></div></header>'''


def footer(route):
    return f'''<footer><div class="wrap footgrid"><div>{wordmark()}<p>Студия пилатеса на реформерах<br>Москва, м. Ботанический сад</p></div>
    <nav aria-label="Разделы в подвале">{''.join(navlink(p,route) for p in PAGES[1:])}</nav></div>
    <div class="wrap footnote"><span>HomePilates · Москва</span><span>Демонстрационная версия</span></div></footer>'''


def join_band():
    return f'''<aside class="join"><div class="wrap join-inner"><div>{section_label('HP','Первый визит')}<h2>Начнём с пробного?</h2>
    <p>Напишите в студию. Администратор поможет выбрать формат и время.</p></div>{btn('Связаться со студией',CONTACT)}</div></aside>'''


def home(prices):
    fig = f'''<figure class="plate"><div class="plate-top"><span>АТЛАС ДВИЖЕНИЯ</span><span>ЛИСТ 01 / 01</span></div>
    {illustration()}<figcaption><span><b>Реформер</b><small>01 Каретка · 02 Упор · 03 Ремни</small></span><span>Схема<br>Фиг. 01</span></figcaption></figure>'''
    by_name = {row['name']: row for row in prices}
    formats = [
        ('В мини-группе', by_name['Пилатес-знакомство (в группе)']),
        ('Индивидуально', by_name['Пилатес-знакомство (индивид.)'])
    ]
    trial = ''.join(f'<a class="trial" href="/stoimost#category-1"><span>{label}</span><b>{rub(p["total_rub"])}</b>{arrow()}</a>' for label,p in formats)
    routes = ''.join(f'<a class="dir-link" href="/napravleniya#{slug}"><small>0{i}</small><span>{name}</span>{arrow()}</a>' for i,(name,_,__,slug) in enumerate(DIRECTIONS,1))
    return f'''<section class="hero wrap"><div class="hero-text"><div class="eyebrow"><i class="dot"></i>Студия движения <span class="slash">/</span> Москва</div>
    <h1>Пилатес на реформерах в Москве <span class="tagline">— тело, которое вас слушается.</span></h1>
    <p class="lede">60 минут на реформере в мини-группе или один на один с тренером у метро Ботанический сад.</p>
    <div class="actions">{btn('Записаться на пробное',CONTACT)}<a class="textlink" href="/raspisanie">Расписание {arrow('→')}</a></div></div>{fig}</section>
    <section class="facts"><div class="wrap factgrid"><div><small>Продолжительность</small><strong>60 минут</strong></div><div><small>Ближайшее метро</small><strong>Ботанический сад</strong></div><div><small>Студия открыта</small><strong>08:00 — 21:00</strong></div></div></section>
    <section class="section wrap split"><div>{section_label('01','Студия')}<h2>Как устроено занятие</h2></div><div class="copy"><p class="big">Реформер — это подвижная каретка с пружинами. Она скользит вдоль рамы, пока вы двигаетесь.</p><p>Первые минуты тренер посвящает знакомству с оборудованием. Затем вы переходите к упражнениям с пружинами, ремнями и аксессуарами. Сопротивление можно менять по ходу занятия.</p>
    <a class="textlink" href="/faq">О первом визите {arrow('→')}</a></div></section>
    <section class="section tint"><div class="wrap split"><div>{section_label('02','Практика')}<h2>Направления</h2><p>Пять способов выстроить свою практику.</p></div><div>{routes}</div></div></section>
    <section class="section wrap split"><div>{section_label('03','Знакомство')}<h2>Первое занятие</h2><p>Пробные форматы из прайса студии.</p></div><div>{trial}<p class="note">Цены для демо. Актуальную стоимость уточните при записи.</p>{btn('Все тарифы','/stoimost',True)}</div></section>
    <section class="section tint"><div class="wrap split"><div>{section_label('04','Люди и место')}<h2>Ждём в студии</h2></div><div class="copy"><p class="big">Москва, проезд Серебрякова, д. 2, корп. 1</p><p>От метро и МЦК Ботанический сад. Поднимитесь на 8 этаж, помещения 26 и 27.</p><div class="actions">{btn('Как добраться','/kontakty',True)}<a class="textlink" href="/komanda">Команда {arrow('→')}</a></div></div></div></section>{join_band()}'''


def directions():
    cards = ''.join(f'''<article id="{slug}" class="directory-row"><div class="serial">0{i}</div><div><small>{kicker}</small><h2>{name}</h2><p>{copy}</p></div>
        <a class="textlink" href="{CONTACT}" aria-label="Уточнить запись — {name}">Уточнить запись {arrow()}</a></article>''' for i,(name,kicker,copy,slug) in enumerate(DIRECTIONS,1))
    return title('01','Практика','Направления','Выберите практику, которая вам интересна. Формат и нагрузку можно обсудить до первого визита.') + f'<section class="wrap list-section">{cards}</section>' + join_band()


def status_card(label, heading, copy, link, url=CONTACT):
    return f'<section class="status-card"><div class="eyebrow"><i class="dot"></i>{label} · Демо</div><h2>{heading}</h2><p>{copy}</p>{btn(link,url)}</section>'


def schedule():
    return title('02','Запись','Расписание','Свободное время и тренера для пробного занятия можно уточнить у администратора.') + f'''<div class="wrap panels">
    {status_card('Расписание','Выбрать время','Онлайн-расписание Mobifitness пока не подключено. Свяжитесь со студией, чтобы узнать о ближайших занятиях.','Узнать свободное время')}
    <aside class="side-card">{section_label('24 ч','Правила записи')}<h2>Перенос и отмена</h2><p>Сообщите студии об изменении планов не позднее чем за 24 часа до занятия.</p><a class="textlink" href="/faq">Вопросы о занятиях {arrow('→')}</a></aside></div>'''


def rub(amount):
    return f'{int(amount):,}'.replace(',', '\u202f') + ' ₽'


def pricing(rows):
    groups=defaultdict(list)
    for row in rows:
        groups[row['category']].append(row)
    blocks=[]
    for i,(category,items) in enumerate(groups.items(),1):
        cards=[]
        for p in items:
            info=[f'Занятий: {p["sessions"]}']
            if p['validity_tz']:
                info.append(f'Срок: {esc(p["validity_tz"])}')
            if p['freeze_tz']=='отсутствуют':
                info.append('Без заморозки')
            elif p['freeze_tz']:
                info.append(f'Заморозка по прайсу: {esc(p["freeze_tz"])} (уточняется)')
            if p['participants_multiplier']=='2':
                info.append('На двоих')
            detail = ''
            if p['name'].startswith('NEW!'):
                detail = '<p>'+esc(p['detail_tz'])+'</p>'
            cards.append(f'<li><div><strong>{esc(p["name"].removeprefix("NEW! "))}</strong><small>{" · ".join(info)}</small>{detail}</div><b>{rub(p["total_rub"])}</b></li>')
        blocks.append(f'''<details id="category-{i}" class="acc"{" open" if i==1 else ""}><summary aria-controls="plans-{i}"><span class="idx">0{i}</span><span>{esc(category)}</span><i class="plus" aria-hidden="true"></i></summary>
        <div id="plans-{i}"><ul class="prices">{''.join(cards)}</ul></div></details>''')
    return title('03','Прайс студии','Стоимость занятий','Пробные занятия, разовые посещения и абонементы. Откройте категорию, чтобы увидеть итоговую стоимость и срок действия.') + f'''<div class="wrap list-section"><p class="notice">Демо-прайс. Итоговые суммы приведены по данным студии. Перед покупкой уточните цену и условия заморозки у администратора.</p>{''.join(blocks)}<div class="actions">{btn('Уточнить запись','/raspisanie')}</div></div>'''


def team():
    people = ''.join(f'<li><span class="initials" aria-hidden="true">{"".join(x[0] for x in name.split())}</span><strong>{name}</strong><span class="idx">0{i}</span></li>' for i,name in enumerate(TEAM,1))
    return title('04','Студия','Наша команда','Познакомьтесь с тренерами HomePilates. Администратор подскажет, кто ведёт выбранное направление и когда можно прийти.') + f'<div class="wrap list-section"><ul class="people">{people}</ul></div>' + join_band()


def faq():
    items = ''.join(f'<details class="acc"><summary aria-controls="answer-{i}"><span class="idx">0{i}</span><span>{question}</span><i class="plus" aria-hidden="true"></i></summary><p id="answer-{i}" class="answer">{answer}</p></details>' for i,(question,answer) in enumerate(FAQ,1))
    return title('05','Перед визитом','Частые вопросы','О подготовке, реформере и правилах записи. Если вашего вопроса здесь нет, напишите администратору.') + f'<div class="wrap list-section">{items}</div>' + join_band()


def certificates():
    return title('06','В подарок','Подарочные сертификаты','Подарите близкому человеку знакомство с реформером. Детали оформления можно обсудить со студией.') + f'''<div class="wrap panels"><div class="gift"><span class="eyebrow">HomePilates / Студия движения</span><div aria-hidden="true" class="giftmark">{mark()}</div><p>Подарочный<br>сертификат</p><small>Эскиз · Не для активации</small></div>
    <section class="side-card">{section_label('HP','Оформление')}<h2>Выберите подарок</h2><p>Предложены варианты на 1, 2 или 3 занятия и VIP. Доступность, номинал, срок и способ получения уточните у администратора.</p><p class="note">Продажа и активация в демо недоступны.</p>{btn('Уточнить условия',CONTACT)}</section></div>'''


def contacts():
    return title('07','Ботанический сад','Контакты','Студия на северо-востоке Москвы, рядом с метро и МЦК Ботанический сад.') + f'''<div class="wrap panels"><section class="side-card address">{section_label('01','Как добраться')}<h2>Проезд Серебрякова,<br>д. 2, корп. 1</h2><p>Москва · 8 этаж, помещения 26 и 27</p><p>Ежедневно с 08:00 до 21:00</p>{btn('Открыть Яндекс Карты',MAP,True)}</section>
    <section class="side-card" id="svyaz">{section_label('02','Запись на пробное')}<h2>Связаться со студией</h2><p>Выберите удобный канал и уточните время, направление или условия абонемента.</p>
    <div class="actions">{btn('Написать в Telegram',TG)}<a class="textlink" href="{PHONE}">+7 (905) 305-87-79 {arrow()}</a></div>
    <div class="channels"><a href="https://wa.me/79253058779">WhatsApp · +7 (925) 305-87-79 {arrow()}</a><a href="mailto:HomePilates.ru@yandex.ru">HomePilates.ru@yandex.ru {arrow()}</a><a href="https://vk.ru/club219971929">Студия во ВКонтакте {arrow()}</a></div></section></div>'''


def cabinet():
    return title('08','Клиентам студии','Личный кабинет','Здесь будет доступ к записям и абонементам через кабинет Mobifitness.') + f'''<div class="wrap panels">{status_card('Личный кабинет','Вход пока недоступен','В демо вход по SMS отключён. О записи, остатке занятий или переносе спросите администратора.','Обратиться к администратору')}
    <aside class="side-card">{section_label('HP','Быстрый переход')}<h2>Планируете занятие?</h2><p>Посмотрите форматы и стоимость или уточните удобное время.</p><a class="textlink" href="/raspisanie">К расписанию {arrow('→')}</a></aside></div>'''
