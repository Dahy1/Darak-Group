# 1) Remove the awwwards floating badge (elementor-element-c90e672) from every page.
# 2) Inject the homepage's Lenis smooth-scroll chunk into every static inner page.
import glob, os, pathlib, re

home = pathlib.Path('site/index.html').read_text(encoding='utf-8')

# --- extract Lenis chunk (css <style> + lenis.min.js + init <script>) from homepage ---
css_start = home.rfind('<style>', 0, home.index('html.lenis, html.lenis body'))
js_end = home.index('</script>', home.index('var lenis = new Lenis')) + len('</script>')
lenis_chunk = home[css_start:js_end]
print('lenis chunk bytes:', len(lenis_chunk))

def strip_badge(html):
    key = '<div class="elementor-element elementor-element-c90e672'
    i = html.find(key)
    if i == -1:
        return html, False
    # walk div nesting from the opening tag to its matching close
    depth = 0; j = i
    while j < len(html):
        nd = html.find('<div', j)
        nc = html.find('</div>', j)
        if nc == -1:
            break
        if nd != -1 and nd < nc:
            depth += 1; j = nd + 4
        else:
            depth -= 1; j = nc + 6
            if depth == 0:
                return html[:i] + html[j:], True
    return html, False

allfiles = glob.glob('site/**/*.html', recursive=True)
for f in allfiles:
    html = pathlib.Path(f).read_text(encoding='utf-8')
    changed = False
    # remove badge (may appear once)
    new, did = strip_badge(html)
    if did:
        html = new; changed = True
    # inject Lenis into inner pages (not the homepage, which already has it)
    if os.path.normpath(f) != os.path.normpath('site/index.html') and 'new Lenis' not in html:
        bm = re.search(r'</body>', html)
        if bm:
            html = html[:bm.start()] + lenis_chunk + '\n' + html[bm.start():]
            changed = True
    if changed:
        pathlib.Path(f).write_text(html, encoding='utf-8')
        print(('debadged ' if did else '         ') + ('+lenis ' if ('new Lenis' in html and os.path.normpath(f)!=os.path.normpath('site/index.html')) else '       ') + f)
