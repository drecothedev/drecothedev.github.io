"""Check course routes, assets, layout markup, and cart calculations."""
from pathlib import Path
import re, sys
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'submission/ActivityWebserver'))
from app import app, PROJECTS
from html.parser import HTMLParser

class Page(HTMLParser):
    def __init__(self, html):
        super().__init__(); self.tags=[]; self.feed(html)
    def handle_starttag(self, tag, attrs):
        self.tags.append((tag, dict(attrs)))

with app.test_client() as client:
    for route in ['/', '/a2', '/a4', '/a5', '/a6', '/a7', '/a8', '/a9', '/project',
                  '/project2', '/project2/products', '/project2/details', '/project2/cart', '/project2/current-project']:
        response = client.get(route)
        assert response.status_code == 200, route
        if not route.startswith('/project2'): continue
        html = response.get_data(as_text=True); page=Page(html)
        scripts = [a for t,a in page.tags if t == 'script']
        assert len(scripts) == 1 and scripts[0]['src'].endswith('/js/project2/spotlight.js'), route
        assert 'defer' in scripts[0], route
        assert not any(k.startswith('on') for t,a in page.tags for k in a), route
        for tag, attrs in page.tags:
            for key in ['href', 'src', 'action']:
                url=attrs.get(key, '')
                if url.startswith('/static/') or url.startswith('/project2'):
                    assert client.get(url.split('#')[0]).status_code == 200, (route,url)
            if tag == 'img':
                assert attrs.get('alt') and attrs.get('width') and attrs.get('height'), route
                assert attrs.get('decoding') == 'async', route
                for candidate in attrs.get('srcset', '').split(','):
                    if candidate.strip(): assert client.get(candidate.strip().split()[0]).status_code == 200

        assert len([1 for t,a in page.tags if t=='header'])==1
        assert len([1 for t,a in page.tags if t=='footer'])==1
    products=client.get('/project2/products').get_data(as_text=True)
    assert products.count('class="product-card"')==6
    assert '<table' not in products
    detail_urls = []
    for project in PROJECTS:
        url = app.url_map.bind('localhost').build('project2_details', {'project_id': project['id']})
        detail_urls.append(url)
        assert products.count('href="' + url + '"') == 2, project['id']
        detail = client.get(url)
        assert detail.status_code == 200, url
        html = detail.get_data(as_text=True)
        assert '<h1>' + project['name'] + '</h1>' in html, url
        assert project['repository_url'] in html, url
        assert str(project['exploration_minutes']) + ' min' in html, url
        for tag, attrs in Page(html).tags:
            if tag == 'img': assert client.get(attrs['src']).status_code == 200, url
    assert len(set(detail_urls)) == len(PROJECTS)
    assert client.get('/project2/details/unknown-project').status_code == 404
    assert '<h1>GEMMA</h1>' in client.get('/project2/details').get_data(as_text=True)
    cart = client.get('/project2/cart').get_data(as_text=True)
    assert '/project2/details/jess' in cart
    for category,count in [('apps',4),('languages',1),('learning',1),('invalid',6)]:
        html=client.get('/project2/products?category='+category).get_data(as_text=True)
        assert html.count('class="product-card"')==count
    for query,amounts in [('', ['30 min','45 min','75 min']),
                          ('?gemma_qty=2&jess_qty=1', ['60 min','45 min','105 min']),
                          ('?gemma_qty=99&jess_qty=99', ['2,970 min','4,455 min','7,425 min'])]:
        html=client.get('/project2/cart'+query).get_data(as_text=True)
        for amount in amounts: assert amount in html, (query,amount)
        assert html.count('class="cart-item glass-panel"')==2
        assert '$' not in html and 'Tax' not in html and 'shipping' not in html
    for route in ['/project2/products', '/project2/details']:
        html=client.get(route).get_data(as_text=True)
        assert 'min' in html and '$' not in html
    for invalid in ['-1','0','100','1.5','abc','']:
        html=client.get('/project2/cart?gemma_qty='+invalid).get_data(as_text=True)
        assert 'role="alert"' in html and '75 min' in html
    html=client.get('/project2',environ_overrides={'SCRIPT_NAME':'/~sampleid'}).get_data(as_text=True)
    assert '/~sampleid/static/css/project2/styles.css' in html
    assert '/~sampleid/project2/products' in html
print('PASS: all routes, internal links/assets, six products, categories, six matching detail pages, shared layout, deferred spotlight script, cart totals, invalid quantities, and NetID prefix.')
