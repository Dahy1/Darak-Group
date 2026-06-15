# Give every STATIC inner page the homepage's nav + menu (markup + CSS + JS),
# replacing its Elementor header. The Next app already injects this via layout;
# this makes the static templates match too.
import re, pathlib, glob, os

home = pathlib.Path('site/index.html').read_text(encoding='utf-8')

# --- extract the contiguous homepage nav chunk: <style>nav css</style> + markup + <script>nav js</script> ---
css_start = home.rfind('<style>', 0, home.index(':root { --zt-ease'))
js_end = home.index('</script>', home.index("getElementById('ztBurger')")) + len('</script>')
nav_chunk = home[css_start:js_end]
# show immediately on pages with no preloader handoff
nav_chunk = nav_chunk.replace(' zt-prereveal', '')

print('nav chunk bytes:', len(nav_chunk))

inner = [p for p in glob.glob('site/**/index.html', recursive=True)
         if os.path.normpath(p) != os.path.normpath('site/index.html')]

for f in inner:
    html = pathlib.Path(f).read_text(encoding='utf-8')
    if 'class="zt-nav"' in html or 'zt-nav zt-prereveal' in html:
        print('  already has nav, skipping', f); continue
    # 1) remove the Elementor site header
    m = re.search(r'<header data-elementor-type="header"', html)
    if m:
        h_end = html.index('</header>', m.start()) + len('</header>')
        html = html[:m.start()] + html[h_end:]
    else:
        print('  !! no elementor header in', f)
    # 2) inject the homepage nav right after <body ...>
    bm = re.search(r'<body[^>]*>', html)
    if not bm:
        print('  !! no body tag in', f); continue
    html = html[:bm.end()] + '\n' + nav_chunk + '\n' + html[bm.end():]
    pathlib.Path(f).write_text(html, encoding='utf-8')
    print('  navified', f)
