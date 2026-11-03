"""Render a static visual preview for Sites.
The course submission is the Flask app, which handles quantity recalculation.
"""
from pathlib import Path
import re, shutil, sys
ROOT=Path(__file__).resolve().parents[1]
APP=ROOT/'submission/ActivityWebserver'
sys.path.insert(0,str(APP))
from app import app, PROJECTS
OUT=ROOT/'portfolio/dist'
OUT.mkdir(parents=True, exist_ok=True)
(OUT/'assets').mkdir(parents=True, exist_ok=True)
ROUTES={'/project2':'index.html','/project2/products':'products.html',
        '/project2/products?category=all':'products.html',
        '/project2/products?category=apps':'products-apps.html',
        '/project2/products?category=languages':'products-languages.html',
        '/project2/products?category=learning':'products-learning.html',
        '/project2/current-project':'current-project.html',
        '/project2/details':'details.html','/project2/cart':'cart.html'}

for product in PROJECTS:
    if product['id'] != 'gemma':
        ROUTES['/project2/details/' + product['id']] = 'details-' + product['id'] + '.html'

def local_link(match):
    attribute,url=match.groups()
    base,sep,fragment=url.partition('#')
    if base in ROUTES: url=ROUTES[base]+(sep+fragment if sep else '')
    elif base.startswith('/static/img/project2/'):url='assets/'+base.rsplit('/',1)[1]
    elif base.startswith('/static/files/project2/'):url='assets/'+base.rsplit('/',1)[1]
    elif base=='/static/css/project2/styles.css':url='styles.css'
    elif base=='/static/js/project2/spotlight.js':url='spotlight.js'
    return f'{attribute}="{url}"'

with app.test_client() as client:
    for route,filename in ROUTES.items():
        html=client.get(route).get_data(as_text=True)
        html=re.sub(r'(href|src|action)="([^"]+)"',local_link,html)
        html=html.replace('/static/img/project2/', 'assets/')
        if filename=='cart.html':
            html=html.replace('Update recalculates your time plan; Remove and Start exploring are mock-up controls.',
                              'Visual preview only. Session counts and time totals are examples; list controls are mock-ups.')
            html=html.replace('type="submit">Update','type="button">Update')
        # Collapse ordinary HTML whitespace while preserving terminal/code formatting.
        parts=re.split(r'(<pre\b.*?</pre>)', html, flags=re.S | re.I)
        html=''.join(part if part.lower().startswith('<pre') else re.sub(r'\s+', ' ', re.sub(r'<!--.*?-->', '', part, flags=re.S)) for part in parts)
        (OUT/filename).write_text(html.strip())
shutil.copy2(APP/'static/css/project2/styles.css',OUT/'styles.css')
for kind in ['img','files']:
    for file in (APP/f'static/{kind}/project2').iterdir():
        if file.is_file() and file.suffix != '.jpg':shutil.copy2(file,OUT/'assets'/file.name)
print('Static preview exported; course Flask submission retains functional quantity updates.')

shutil.copy2(APP/'static/js/project2/spotlight.js', OUT/'spotlight.js')

for name in ['gemma.jpg','sxmpler.jpg']:
    stale=OUT/'assets'/name
    if stale.exists(): stale.unlink()
