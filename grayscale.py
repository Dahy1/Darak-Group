# Convert the whole site to white/black/gray: every color token (hex, %23-hex,
# rgb/rgba, hsl/hsla) is replaced by a neutral gray of the same luminance.
# The four approved brand mappings are honored exactly; everything else uses luma.
import re, pathlib, glob

BRAND = {                      # exact RGB -> exact gray RGB (user-approved)
    (238,235,228): (242,242,242),   # cream  #EEEBE4 -> #F2F2F2
    (182,171,153): (154,154,154),   # taupe  #B6AB99 -> #9A9A9A
    (150,132,122): (110,110,110),   # mauve  #96847A -> #6E6E6E
    (20,17,15):    (17,17,17),       # dark   #14110F -> #111111
}

def gray(r, g, b):
    for (br,bg,bb), v in BRAND.items():
        if abs(r-br)<=3 and abs(g-bg)<=3 and abs(b-bb)<=3:
            return v
    y = round(0.299*r + 0.587*g + 0.114*b)
    y = max(0, min(255, y))
    return (y, y, y)

count = [0]
def hx(n): return '%02x' % n

def repl_hex6(m):
    s = m.group(1); r,g,b = int(s[0:2],16),int(s[2:4],16),int(s[4:6],16)
    gr = gray(r,g,b); count[0]+=1
    return m.group(0)[0:len(m.group(0))-6] + hx(gr[0])+hx(gr[1])+hx(gr[2])

def repl_hex3(m):
    s = m.group(1); r,g,b = int(s[0]*2,16),int(s[1]*2,16),int(s[2]*2,16)
    gr = gray(r,g,b); count[0]+=1
    pre = m.group(0)[:-3]
    return pre + hx(gr[0])+hx(gr[1])+hx(gr[2])

def repl_hex8(m):  # #rrggbbaa  -> gray rgb, keep alpha
    s = m.group(1); r,g,b = int(s[0:2],16),int(s[2:4],16),int(s[4:6],16)
    gr = gray(r,g,b); count[0]+=1
    return m.group(0)[:-8] + hx(gr[0])+hx(gr[1])+hx(gr[2]) + s[6:8]

def repl_hex4(m):  # #rgba shorthand -> gray rgb, keep alpha
    s = m.group(1); r,g,b = int(s[0]*2,16),int(s[1]*2,16),int(s[2]*2,16)
    gr = gray(r,g,b); count[0]+=1
    return m.group(0)[:-4] + hx(gr[0])+hx(gr[1])+hx(gr[2]) + s[3]*2

def repl_rgb(m):
    r,g,b = int(m.group(1)),int(m.group(2)),int(m.group(3))
    a = m.group(4)
    gr = gray(r,g,b); count[0]+=1
    if a is not None and a != '':
        return f'rgba({gr[0]}, {gr[1]}, {gr[2]}, {a})'
    return f'rgb({gr[0]}, {gr[1]}, {gr[2]})'

def repl_hsl(m):
    h = m.group(1); l = m.group(3); a = m.group(4)
    count[0]+=1
    if a is not None and a != '':
        return f'hsla({h}, 0%, {l}%, {a})'
    return f'hsl({h}, 0%, {l}%)'

# order matters: longer/encoded first
RE_PCT6 = re.compile(r'%23([0-9a-fA-F]{6})(?![0-9a-fA-F])')
RE_HEX8 = re.compile(r'#([0-9a-fA-F]{8})(?![0-9a-fA-F])')
RE_HEX6 = re.compile(r'#([0-9a-fA-F]{6})(?![0-9a-fA-F])')
RE_HEX4 = re.compile(r'#([0-9a-fA-F]{4})(?![0-9a-fA-F])')
RE_HEX3 = re.compile(r'#([0-9a-fA-F]{3})(?![0-9a-fA-F])')
RE_RGB  = re.compile(r'rgba?\(\s*(\d{1,3})\s*,\s*(\d{1,3})\s*,\s*(\d{1,3})\s*(?:,\s*([\d.]+)\s*)?\)')
RE_HSL  = re.compile(r'hsla?\(\s*(\d{1,3})\s*,\s*(\d{1,3})%\s*,\s*(\d{1,3})%\s*(?:,\s*([\d.]+)\s*)?\)')

def repl_pct6(m):
    s = m.group(1); r,g,b = int(s[0:2],16),int(s[2:4],16),int(s[4:6],16)
    gr = gray(r,g,b); count[0]+=1
    return '%23' + hx(gr[0])+hx(gr[1])+hx(gr[2])

def transform(text):
    text = RE_PCT6.sub(repl_pct6, text)
    text = RE_HEX8.sub(repl_hex8, text)
    text = RE_HEX6.sub(repl_hex6, text)
    text = RE_HEX4.sub(repl_hex4, text)
    text = RE_HEX3.sub(repl_hex3, text)
    text = RE_RGB.sub(repl_rgb, text)
    text = RE_HSL.sub(repl_hsl, text)
    return text

# roots: the static source AND the Next app's served copies (public/ + content/)
ROOTS = ['site', 'darak-next/public', 'darak-next/content']

# ---- CSS files: transform whole file ----
css_files = []
for _r in ROOTS:
    css_files += glob.glob(_r + '/**/*.css', recursive=True)
for f in css_files:
    p = pathlib.Path(f); t = p.read_text(encoding='utf-8', errors='ignore')
    n0 = count[0]; t2 = transform(t)
    if t2 != t: p.write_text(t2, encoding='utf-8')

# ---- HTML files: only inside <style>, <script>, and style="" / style='' ----
RE_STYLE  = re.compile(r'(<style[^>]*>)(.*?)(</style>)', re.S|re.I)
RE_SCRIPT = re.compile(r'(<script[^>]*>)(.*?)(</script>)', re.S|re.I)
RE_ATTR_D = re.compile(r'style="([^"]*)"')
RE_ATTR_S = re.compile(r"style='([^']*)'")

html_files = []
for _r in ROOTS:
    html_files += glob.glob(_r + '/**/*.html', recursive=True)
for f in html_files:
    p = pathlib.Path(f); t = p.read_text(encoding='utf-8', errors='ignore')
    t = RE_STYLE.sub(lambda m: m.group(1)+transform(m.group(2))+m.group(3), t)
    t = RE_SCRIPT.sub(lambda m: m.group(1)+transform(m.group(2))+m.group(3), t)
    t = RE_ATTR_D.sub(lambda m: 'style="'+transform(m.group(1))+'"', t)
    t = RE_ATTR_S.sub(lambda m: "style='"+transform(m.group(1))+"'", t)
    p.write_text(t, encoding='utf-8')

print('css files:', len(css_files), '| html files:', len(html_files), '| color tokens converted:', count[0])
