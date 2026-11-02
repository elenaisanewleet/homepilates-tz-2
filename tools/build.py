"""Build the static preview and copyable Tilda T123 blocks. Requires Python 3.9+."""

import re
import shutil
import sys
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / 'src'
sys.path.insert(0, str(SRC))
import pages

PRODUCTION = 'https://classes.homepilates.ru'
DEMO = 'https://homepilates-tz-2.vercel.app'
# Tilda blocks cannot use the preview's /assets, so photos are served from the public repository via jsDelivr.
CDN = 'https://cdn.jsdelivr.net/gh/elenaisanewleet/homepilates-tz-2@main/public/assets'
PUBLIC = ROOT / 'public'
TILDA = ROOT / 'tilda'


def write(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.strip() + '\n', encoding='utf-8')


def for_tilda(body):
    """Tilda copy: absolute photo URLs, no preview-only notes."""
    body = body.replace('src="/assets/photos/', f'src="{CDN}/photos/')
    return re.sub(r'<p class="form-note" data-preview-only>.*?</p>', '', body, flags=re.S)


def build():
    content = {
        '/': pages.home(), '/napravleniya': pages.directions(), '/raspisanie': pages.schedule(),
        '/stoimost': pages.pricing(), '/komanda': pages.team(), '/faq': pages.faq(),
        '/sertifikaty': pages.certificates(), '/kontakty': pages.contacts(), '/cabinet': pages.cabinet()
    }
    css = (SRC / 'theme.css').read_text(encoding='utf-8')
    js = (SRC / 'site.js').read_text(encoding='utf-8')
    write(PUBLIC / 'assets/theme.css', css)
    write(PUBLIC / 'assets/site.js', js)
    old_menu = PUBLIC / 'assets/menu.js'
    if old_menu.exists():
        old_menu.unlink()
    photos = PUBLIC / 'assets/photos'
    photos.mkdir(parents=True, exist_ok=True)
    for photo in (SRC / 'photos').glob('*.jpg'):
        shutil.copyfile(photo, photos / photo.name)
    write(PUBLIC / 'favicon.svg', pages.LOGO)
    write(TILDA / 'shared-head.html', '<style>\n' + css + '\n</style>')
    seo = ['route,title,description,canonical']
    counter = pages.INTEGR['metrika']
    for route, _, _, description in pages.PAGES:
        slug = route.strip('/')
        page_title = pages.TITLES.get(slug) or pages.TITLES.get('')
        body = (f'<div id="hp-site" data-counter="{counter}">{pages.header(route)}<main id="content" tabindex="-1">'
                f'{content[route]}</main>{pages.footer(route)}{pages.cookie_box()}</div>')
        preview = (f'<meta property="og:type" content="website"><meta property="og:site_name" content="HomePilates">'
                   f'<meta property="og:title" content="{escape(page_title)}"><meta property="og:description" content="{escape(description)}">'
                   f'<meta property="og:url" content="{DEMO}{route}"><meta property="og:locale" content="ru_RU">'
                   f'<meta property="og:image" content="{DEMO}/assets/photos/trainer-negreeva.jpg"><meta name="twitter:card" content="summary_large_image">')
        head = f'''<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
        <title>{escape(page_title)}</title><meta name="description" content="{escape(description)}">
        <meta name="robots" content="noindex, nofollow"><link rel="canonical" href="{PRODUCTION}{route}">{preview}
        <link rel="icon" href="/favicon.svg?v=studio" type="image/svg+xml"><link rel="stylesheet" href="/assets/theme.css">
        <style>body{{margin:0;background:#f9f8f1}}</style><script src="/assets/site.js" defer></script>'''
        write(PUBLIC / slug / 'index.html', f'<!doctype html>\n<html lang="ru"><head>{head}</head><body>{body}</body></html>')
        write(TILDA / ((slug or 'home') + '.html'), for_tilda(body) + '\n<script>\n' + js + '\n</script>')
        seo.append(','.join('"' + val.replace('"', '""') + '"' for val in (route, page_title, description, PRODUCTION + route)))
    write(TILDA / 'seo.csv', '\n'.join(seo))
    write(PUBLIC / 'robots.txt', 'User-agent: *\nDisallow: /')
    urls = ''.join(f'<url><loc>{DEMO}{p[0]}</loc></url>' for p in pages.PAGES if p[0] != '/cabinet')
    write(PUBLIC / 'sitemap.xml', '<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' + urls + '</urlset>')
    print(f'Built {len(content)} pages and {len(content)} T123 blocks.')


if __name__ == '__main__':
    build()
