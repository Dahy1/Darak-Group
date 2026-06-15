# Insert the cloned project-template sections into every project page's
# (emptied) single-post wrapper, substituting the per-page project name.
import re, pathlib

frag = pathlib.Path('project_template.html').read_text(encoding='utf-8')

names = {
    '1000-89-st-surfside': '1000 89th Street',
    '1710-s-bayshore-drive': '1710 S. Bayshore Drive',
    '1716-s-bayshore-drive': '1716 S. Bayshore Drive',
    'hibiscus-island-estate': 'Hibiscus Island Estate',
    'miami-beach-residence': 'Miami Beach Residence',
    'normandy-shores': 'Normandy Shores',
}

open_re = re.compile(r'(<div[^>]*data-elementor-type="single-post"[^>]*>)', re.I)

for slug, name in names.items():
    p = pathlib.Path('site/projects') / slug / 'index.html'
    html = p.read_text(encoding='utf-8')
    m = open_re.search(html)
    if not m:
        print('!! no single-post wrapper in', slug); continue
    open_tag = m.group(1)
    # find the matching (currently-empty) close: first </div> after the opening tag
    close_idx = html.index('</div>', m.end())
    body = frag.replace('__NAME__', name)
    new = html[:m.end()] + '\n' + body + '\n\t\t' + html[close_idx:]
    p.write_text(new, encoding='utf-8')
    print('ok', slug, '->', name, '|', len(new), 'bytes')
