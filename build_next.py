# Convert the static site/ into a Next.js app under darak-next/.
# Shared nav/menu/footer + global scripts come from the homepage and are reused on every page.
import os, re, json, pathlib
import lxml.html
from lxml import etree

SITE = pathlib.Path('site')
OUT = pathlib.Path('darak-next')
CONT = OUT / 'content'
PAGES = CONT / 'pages'
PAGES.mkdir(parents=True, exist_ok=True)

def ser(el):
    return lxml.html.tostring(el, encoding='unicode', method='html')

def script_obj(el):
    src = el.get('src'); t = (el.get('type') or '').lower()
    o = {}
    if t: o['type'] = t
    if src: o['src'] = src
    else: o['code'] = el.text or ''
    return o

def parse(path):
    return lxml.html.fromstring(pathlib.Path(path).read_text(encoding='utf-8', errors='ignore'))

# ---------- HOMEPAGE: shared chrome + globals ----------
root = parse(SITE / 'index.html')
head = root.head
body = root.body

# global scripts: head scripts first, then body scripts, in document order
global_scripts = [script_obj(s) for s in head.iter('script')]
global_scripts += [script_obj(s) for s in body.iter('script')]

# head assets (links + styles + meta), excluding scripts/title
head_bits = []
for el in head:
    if el.tag in ('script', 'title'):
        continue
    if el.tag == 'link' and (el.get('rel') or '') in ('profile',):
        continue
    head_bits.append(ser(el).strip())
# the custom nav / footer / chrome CSS lives in <style> blocks in the BODY, so pull
# every homepage inline stylesheet up into the global head -> styled on every page.
# (they're class-namespaced, so they only match homepage elements elsewhere.)
for st in body.iter('style'):
    head_bits.append(ser(st).strip())
# the footer is a global Elementor template; link its CSS so it styles on every page
import glob as _glob
_fel = body.find('.//footer')
_fid = _fel.get('data-elementor-id') if _fel is not None else None
if _fid:
    _m = (_glob.glob(f'site/wp-content/uploads/elementor/css/post-{_fid}_ver*.css')
          or _glob.glob(f'site/wp-content/uploads/elementor/css/post-{_fid}.css'))
    if _m:
        _fn = pathlib.Path(_m[0]).name
        head_bits.append(f'<link rel="stylesheet" href="/wp-content/uploads/elementor/css/{_fn}">')
(CONT / '_head.html').write_text('\n'.join(head_bits), encoding='utf-8')

# nav (header.zt-nav + nav.zt-inline + div.zt-overlay)
def grab(sel_id):
    e = body.get_element_by_id(sel_id, None)
    return e
nav_ids = ['ztNav', 'ztInline', 'ztOverlay']
nav_els = [grab(i) for i in nav_ids]
nav_html = '\n'.join(ser(e).strip() for e in nav_els if e is not None)
(CONT / '_nav.html').write_text(nav_html, encoding='utf-8')

# footer (the homepage footer container)
footer_el = body.find('.//footer')
footer_html = ser(footer_el).strip() if footer_el is not None else ''
(CONT / '_footer.html').write_text(footer_html, encoding='utf-8')

(CONT / '_scripts.json').write_text(json.dumps(global_scripts), encoding='utf-8')

def strip_common(body_el):
    # remove all <script> and preloader nodes from a body subtree
    for s in list(body_el.iter('script')):
        s.getparent().remove(s)
    for pre in list(body_el.xpath('.//*[@id="ohPreloader" or contains(@class,"oh-preloader")]')):
        pre.getparent().remove(pre)

# homepage content = body minus nav, footer, scripts, preloader
home_root = parse(SITE / 'index.html')
hbody = home_root.body
strip_common(hbody)
for i in nav_ids:
    e = hbody.get_element_by_id(i, None)
    if e is not None:
        e.getparent().remove(e)
f = hbody.find('.//footer')
if f is not None:
    f.getparent().remove(f)
home_content = ''.join(ser(c) for c in hbody)
(PAGES / 'index.html').write_text(home_content, encoding='utf-8')
(PAGES / 'index.style.html').write_text('', encoding='utf-8')
(PAGES / 'index.scripts.json').write_text('[]', encoding='utf-8')

routes = [{'route': '', 'file': 'index', 'title': (root.findtext('.//title') or 'Olivia Harper Homes')}]

# ---------- OTHER PAGES ----------
for idx in sorted(SITE.glob('**/index.html')):
    rel = idx.parent.relative_to(SITE).as_posix()
    if rel == '.':
        continue  # homepage already done
    r = parse(idx)
    rbody = r.body
    # page-specific inline styles from head
    pstyles = '\n'.join(ser(s).strip() for s in r.head.iter('style'))
    # page inline scripts (no src), document order, from body — but NOT the shared
    # nav JS (it's already a global script; re-running would double-bind handlers)
    pscripts = [script_obj(s) for s in rbody.iter('script')
                if not s.get('src') and 'ztBurger' not in (s.text or '')
                and 'new Lenis' not in (s.text or '')]
    # remove elementor header/footer + scripts + preloader -> content
    strip_common(rbody)
    for chrome in rbody.xpath('.//header[@data-elementor-type="header"] | .//footer[@data-elementor-type="footer"] | .//div[contains(@class,"zt-overlay")] | .//header[contains(@class,"zt-nav")] | .//nav[contains(@class,"zt-inline")]'):
        chrome.getparent().remove(chrome)
    # drop the injected nav CSS block (it's global via _head.html on every page)
    for st in list(rbody.iter('style')):
        if st.text and ('.zt-nav' in st.text or 'html.lenis' in st.text):
            st.getparent().remove(st)
    content = ''.join(ser(c) for c in rbody)
    file = rel.replace('/', '__')
    (PAGES / f'{file}.html').write_text(content, encoding='utf-8')
    (PAGES / f'{file}.style.html').write_text(pstyles, encoding='utf-8')
    (PAGES / f'{file}.scripts.json').write_text(json.dumps(pscripts), encoding='utf-8')
    routes.append({'route': rel, 'file': file, 'title': (r.findtext('.//title') or 'Olivia Harper Homes')})

(CONT / 'routes.json').write_text(json.dumps(routes, indent=1), encoding='utf-8')
print('routes:', len(routes))
for x in routes:
    print(' ', repr(x['route']) or '/', '->', x['file'])
print('global scripts:', len(global_scripts), '| nav bytes', len(nav_html), '| footer bytes', len(footer_html), '| head bytes', len('\n'.join(head_bits)))
