"""Verify generated links, SEO, price data and Tilda markup with stdlib only."""
import csv
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]


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


def read_csv(path):
    with path.open(encoding='utf-8-sig') as file:
        return list(csv.DictReader(file))


def check():
    pages = {}
    seo = read_csv(ROOT/'tilda/seo.csv')
    assert len(seo) == len({r['route'] for r in seo}) == 9
    assert len({r['title'] for r in seo}) == len({r['description'] for r in seo}) == 9
    for row in seo:
        route = row['route']
        slug = route.strip('/')
        source = (ROOT/'public'/slug/'index.html').read_text()
        page = Page(source)
        pages[route] = page
        assert sum(name == 'h1' for name, _ in page.tags) == 1, route
        assert len(page.ids) == len(set(page.ids)), route
        assert ('link', {'rel':'canonical','href':'https://classes.homepilates.ru'+route}) in page.tags
        assert ('meta', {'name':'robots','content':'noindex, nofollow'}) in page.tags
        assert ('meta', {'name':'description','content':row['description']}) in page.tags
        assert row['title'] in page.text
        assert not any(name in ('form','iframe','input') for name,_ in page.tags), route
        tilda = (ROOT/'tilda'/((slug or 'home')+'.html')).read_text()
        assert source.split('<body>')[1].split('</body>')[0] in tilda, route
    for route, page in pages.items():
        for href in page.links:
            u = urlsplit(href)
            if u.scheme or u.netloc:
                assert u.scheme in ('https','mailto','tel'), href
                continue
            target = u.path or route
            assert target in pages, (route,href)
            assert not u.fragment or u.fragment in pages[target].ids, (route,href)
    rows = read_csv(ROOT/'data/PRICING_SOURCE.csv')
    expected = [f'{int(r["total_rub"]):,}'.replace(',', '\u202f')+' ₽' for r in rows]
    actual = [s for s in pages['/stoimost'].text if s.endswith(' ₽')]
    assert actual == expected, 'Displayed price rows must match CSV totals in order'
    assert len(set(r['category'] for r in rows)) == 7
    assert len(rows) == 33
    assert sum(tag == 'h2' for tag,_ in pages['/napravleniya'].tags) == 6  # Five entries and trial CTA
    print(f'OK: {len(pages)} routes, {sum(len(p.links) for p in pages.values())} links, SEO, T123 parity and {len(expected)} prices.')


if __name__ == '__main__':
    check()
