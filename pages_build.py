# -*- coding: utf-8 -*-
"""Build a GitHub Pages deploy copy of site/ that works when served from the
project sub-path /Darak-Group/. Root-absolute URLs in the HTML are prefixed;
CSS/JS use relative paths and need no changes."""
import re, pathlib, shutil

SITE = pathlib.Path('site')
DIST = pathlib.Path('_pagesdist')
PREFIX = '/Darak-Group'


def fix_html(t):
    # attributes whose value is a single root-absolute path (skip protocol-relative //)
    t = re.sub(r'(\b(?:href|src|poster|action|data-url)=")/(?!/)', r'\1' + PREFIX + '/', t)
    # og:image / og:url style meta (only values that start with a single slash)
    t = re.sub(r'(content=")/(?!/)', r'\1' + PREFIX + '/', t)
    # url(...) inside inline styles, <style> blocks and @font-face
    t = re.sub(r'url\((["\']?)/(?!/)', r'url(\1' + PREFIX + '/', t)
    # JSON-LD path fields
    t = re.sub(r'("(?:url|@id|contentUrl)":")/(?!/)', r'\1' + PREFIX + '/', t)
    # srcset: prefix every candidate URL in the list
    def _srcset(m):
        return 'srcset="' + re.sub(r'(^|,\s*)/(?!/)', r'\1' + PREFIX + '/', m.group(1)) + '"'
    t = re.sub(r'srcset="([^"]*)"', _srcset, t)
    return t


def main():
    if DIST.exists():
        shutil.rmtree(DIST)
    shutil.copytree(SITE, DIST)
    (DIST / '.nojekyll').write_text('', encoding='utf-8')
    n = 0
    for f in DIST.rglob('*.html'):
        s = f.read_text(encoding='utf-8', errors='ignore')
        o = fix_html(s)
        if o != s:
            f.write_text(o, encoding='utf-8')
            n += 1
    print('pages dist ready: %s  (prefixed %d html files with %s)' % (DIST, n, PREFIX))


if __name__ == '__main__':
    main()
