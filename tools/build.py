"""Build a static demo and copyable Tilda T123 blocks. Requires Python 3.9+."""

import csv
import sys
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / 'src'
sys.path.insert(0, str(SRC))
import pages

PRODUCTION = 'https://classes.homepilates.ru'
DEMO = 'https://homepilates-tz-2.vercel.app'
PUBLIC = ROOT / 'public'
TILDA = ROOT / 'tilda'


def write(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.strip()+'\n', encoding='utf-8')


def build():
    with (ROOT/'data/PRICING_SOURCE.csv').open(encoding='utf-8-sig') as f:
        prices = list(csv.DictReader(f))
    content = {
        '/': pages.home(prices), '/napravleniya': pages.directions(), '/raspisanie': pages.schedule(),
        '/stoimost': pages.pricing(prices), '/komanda': pages.team(), '/faq': pages.faq(),
        '/sertifikaty': pages.certificates(), '/kontakty': pages.contacts(), '/cabinet': pages.cabinet()
    }
    css = (SRC/'theme.css').read_text(encoding='utf-8')
    js = (SRC/'menu.js').read_text(encoding='utf-8')
    write(PUBLIC/'assets/theme.css', css)
    write(PUBLIC/'assets/menu.js', js)
    write(PUBLIC/'favicon.svg', pages.LOGO)
    write(TILDA/'shared-head.html', '<style>\n'+css+'\n</style>')
    seo = ['route,title,description,canonical']
    for route, _, title, description in pages.PAGES:
        slug = route.strip('/')
        page_title = title+' — HomePilates'
        body = f'<div id="hp-site">{pages.header(route)}<main id="content" tabindex="-1">{content[route]}</main>{pages.footer(route)}</div>'
        head = f'''<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
        <title>{escape(page_title)}</title><meta name="description" content="{escape(description)}">
        <meta name="robots" content="noindex, nofollow"><link rel="canonical" href="{PRODUCTION}{route}">
        <link rel="icon" href="/favicon.svg?v=studio" type="image/svg+xml"><link rel="stylesheet" href="/assets/theme.css">
        <style>body{{margin:0;background:#f9f8f1}}</style><script src="/assets/menu.js" defer></script>'''
        write(PUBLIC/slug/'index.html', f'<!doctype html>\n<html lang="ru"><head>{head}</head><body>{body}</body></html>')
        write(TILDA/((slug or 'home')+'.html'), body+'\n<script>\n'+js+'\n</script>')
        seo.append(','.join('"'+val.replace('"','""')+'"' for val in (route,page_title,description,PRODUCTION+route)))
    write(TILDA/'seo.csv','\n'.join(seo))
    write(PUBLIC/'robots.txt','User-agent: *\nDisallow: /')
    urls = ''.join(f'<url><loc>{DEMO}{p[0]}</loc></url>' for p in pages.PAGES if p[0]!='/cabinet')
    write(PUBLIC/'sitemap.xml', '<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+urls+'</urlset>')
    print(f'Built {len(content)} pages, {len(prices)} price rows, and {len(content)} T123 blocks.')


if __name__ == '__main__':
    build()
