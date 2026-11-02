"""Verify generated pages against the ТЗ data with stdlib only: SEO, links, prices, integrations, Tilda parity."""
import csv
import json
import re
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
from build import for_tilda

DATA = json.loads((ROOT / 'data/content.json').read_text(encoding='utf-8'))


class Page(HTMLParser):
    def __init__(self, source):
        super().__init__()
        self.ids, self.links, self.tags, self.text = [], [], [], []
        self.feed(source)

    def handle_starttag(self, name, attributes):
        attrs = dict(attributes)
        self.tags.append((name, attrs))
        if 'id' in attrs:
            self.ids.append(attrs['id'])
        if name == 'a':
            self.links.append(attrs['href'])

    def handle_data(self, text):
        self.text.append(text)

    def count(self, name, cls=None):
        return sum(tag == name and (cls is None or cls in (attrs.get('class') or '').split()) for tag, attrs in self.tags)


def read_csv(path):
    with path.open(encoding='utf-8-sig') as file:
        return list(csv.DictReader(file))


def check():
    pages, sources = {}, {}
    seo = read_csv(ROOT / 'tilda/seo.csv')
    assert len(seo) == len({r['route'] for r in seo}) == 9
    assert len({r['title'] for r in seo}) == len({r['description'] for r in seo}) == 9
    counter = DATA['integrations']['metrika']
    for row in seo:
        route = row['route']
        slug = route.strip('/')
        source = (ROOT / 'public' / slug / 'index.html').read_text(encoding='utf-8')
        page = Page(source)
        pages[route], sources[route] = page, source
        assert page.count('h1') == 1, route
        assert len(page.ids) == len(set(page.ids)), route
        assert ('link', {'rel': 'canonical', 'href': 'https://classes.homepilates.ru' + route}) in page.tags, route
        assert ('meta', {'name': 'robots', 'content': 'noindex, nofollow'}) in page.tags, route
        assert ('meta', {'name': 'description', 'content': row['description']}) in page.tags, route
        assert row['title'] in page.text, route
        # Metrika only through site.js after consent; cookie box, requisites and legal links on every page
        assert 'mc.yandex.ru' not in source and f'data-counter="{counter}"' in source, route
        assert page.count('form', 'cookie-box') == 1, route
        for value in DATA['legal']['requisites'].values():
            assert value in page.text, (route, value)
        assert DATA['legal']['policy'] in page.links and DATA['legal']['approval'] in page.links, route
        assert page.count('div', 'mobi') <= 1, ('one Mobifitness widget per page', route)
        assert not re.search(r'парол|password|\bдемо\b', source, re.I), route
        body = source.split('<body>')[1].split('</body>')[0]
        tilda = (ROOT / 'tilda' / ((slug or 'home') + '.html')).read_text(encoding='utf-8')
        assert for_tilda(body) in tilda and 'data-preview-only' not in tilda, route
        assert 'src="/assets/' not in tilda, route
    for route, page in pages.items():
        for href in page.links:
            u = urlsplit(href)
            if u.scheme or u.netloc:
                assert u.scheme in ('https', 'mailto', 'tel'), href
                continue
            target = u.path or route
            assert target in pages, (route, href)
            assert not u.fragment or u.fragment in pages[target].ids, (route, href)
        for tag, attrs in page.tags:
            if tag == 'img' and attrs['src'].startswith('/'):
                assert (ROOT / 'public' / attrs['src'].lstrip('/')).is_file(), attrs['src']
        # Every form with personal data asks for consent with a link to the policy
        if page.count('form', 'feedback'):
            assert ('input', {'type': 'checkbox', 'name': DATA['labels']['approval'],
                              'value': DATA['legal']['consent'], 'required': None}) in page.tags, route
    widgets = {route: attrs['data-type'] for route, page in pages.items() for tag, attrs in page.tags
               if tag == 'div' and attrs.get('class') == 'mobi'}
    assert widgets == {'/': 'personal', '/raspisanie': 'schedule', '/sertifikaty': 'personal', '/cabinet': 'personal'}, widgets
    for route in ('/', '/kontakty'):
        assert any(tag == 'iframe' and 'yandex.ru' in attrs['src'] for tag, attrs in pages[route].tags), route
    groups = DATA['prices']['groups']
    expected = [row[2] for group in groups for row in group['rows']]
    actual = [s for s in pages['/stoimost'].text if s in expected]
    assert actual == expected, 'Displayed prices must follow content.json in order'
    assert len(groups) == 7 and len(expected) == 33
    assert pages['/napravleniya'].count('h2') == len(DATA['directions']['items'])
    assert pages['/komanda'].count('article', 'person') == len(DATA['team']['people'])
    print(f'OK: {len(pages)} routes, {sum(len(p.links) for p in pages.values())} links, SEO, consent, '
          f'{len(widgets)} widgets, T123 parity and {len(expected)} prices.')


if __name__ == '__main__':
    check()
