# -*- coding: utf-8 -*-
"""Rewrite visible copy across the whole site to an Egyptian developer, "Darak Group".
Asset paths / routes (in src, srcset, href, url(), JSON-LD urls, og:image, etc.) are
masked first so replacements can never corrupt an image src or a link."""
import re, glob, pathlib

# ordered: most specific first
PAIRS = [
    # ---- brand ----
    ("Olivia Harper Real Estate", "Darak Group"),
    ("Olivia Harper Homes", "Darak Group"),
    ("Olivia Harper", "Darak Group"),
    # ---- founders / leadership (dummy Egyptian names) ----
    ("Jack Echterling", "Karim Darak"),
    ("John Schamy", "Omar El-Sharif"),
    # ---- sub-brands ----
    ("Harper Construction", "Darak Construction"),
    ("Harper Design Studio", "Darak Design Studio"),
    ("Harper Development", "Darak Development"),
    # ---- project display names -> Egyptian developments ----
    ("1716 S. Bayshore Drive", "The Address New Cairo"),
    ("1710 S. Bayshore Drive", "Zayed Dunes"),
    ("445 N. Shore Drive", "Almaza Bay Chalets"),
    ("1000 89 St, Surfside", "Capital Heights"),
    ("Hibiscus Island Estate", "Marsa Sahel Residences"),
    ("Miami Beach Residence", "Katameya Greens"),
    ("Normandy Shores", "Almaza Bay Chalets"),
    # ---- contact / address ----
    ("4770 Biscayne Blvd. Ste 600, Miami, FL 33137", "Plot 24, North 90th Street, New Cairo, Cairo"),
    ("4770 Biscayne Blvd. Ste 600", "Plot 24, North 90th Street"),
    ("Biscayne Blvd", "North 90th Street"),
    ("305-336-7195", "+20 2 2461 1234"),
    ('"postalCode":"33137"', '"postalCode":"11835"'),
    ('"addressLocality":"Miami"', '"addressLocality":"New Cairo"'),
    ('"addressRegion":"FL"', '"addressRegion":"Cairo"'),
    # ---- locations (specifics before bare words) ----
    ("South Florida", "Egypt"),
    ("Miami, Florida", "New Cairo, Egypt"),
    ("Miami, FL", "Cairo, Egypt"),
    ("Miami Beach", "New Cairo"),
    ("Coconut Grove", "New Cairo"),
    ("Miami", "Cairo"),
    ("Florida", "Egypt"),
    ("Bayshore", "New Cairo"),
    ("Surfside", "New Capital"),
    ("Normandy", "Almaza Bay"),
]

# a quoted value or url() containing any of these is treated as a path/route and protected
MARKERS = ('/wp-content', '/uploads', 'http', '.jpg', '.jpeg', '.png', '.svg', '.webp',
           '.mp4', '.woff', '.css', '.js', '/projects/', '/blog/', '/feed', 'gravatar',
           '/cdnjs', '/wp-includes', '/wp-json', 'sourceURL')


def mask(html):
    store = []

    def keep(m):
        store.append(m.group(0))
        return '\x00%d\x00' % (len(store) - 1)

    html = re.sub(r'url\([^)]*\)', keep, html)

    def q(m):
        inner = m.group(0)[1:-1]
        if any(k in inner for k in MARKERS):
            store.append(m.group(0))
            return '\x00%d\x00' % (len(store) - 1)
        return m.group(0)

    html = re.sub(r'"[^"]*"', q, html)
    return html, store


def unmask(html, store):
    return re.sub(r'\x00(\d+)\x00', lambda m: store[int(m.group(1))], html)


def process(path):
    raw = pathlib.Path(path).read_text(encoding='utf-8')
    masked, store = mask(raw)
    out = masked
    for a, b in PAIRS:
        out = out.replace(a, b)
    out = unmask(out, store)
    if out != raw:
        pathlib.Path(path).write_text(out, encoding='utf-8')
        return True
    return False


def main():
    n = 0
    for p in glob.glob('site/**/index.html', recursive=True):
        if process(p):
            n += 1
    print('copy rewritten on %d pages' % n)


if __name__ == '__main__':
    main()
