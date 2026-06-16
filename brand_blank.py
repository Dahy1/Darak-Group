# -*- coding: utf-8 -*-
"""Final brand pass over site/:
  1) replace any remaining "Olivia Harper" wordmark (incl. ALL-CAPS) with "Darak Group"
  2) blank the href of every link that points at the old brand (oliviaharper*)

No masking is needed: the wordmark is matched WITH its space, while asset paths use a
hyphen ("Olivia-Harper.jpg") and the domain has no space ("oliviaharper"), and URLs never
contain a raw space -- so a spaced replacement can never touch a path, src or url()."""
import re, glob, pathlib

# ordered: most specific first so "...Homes" collapses before the bare wordmark
PAIRS = [
    ("Olivia Harper Real Estate", "Darak Group"),
    ("Olivia Harper Homes", "Darak Group"),
    ("OLIVIA HARPER HOMES", "DARAK GROUP"),
    ("Olivia Harper", "Darak Group"),
    ("OLIVIA HARPER", "DARAK GROUP"),
]

# blank the href of any link aimed at the old brand (double- or single-quoted)
HREF = re.compile(r'href\s*=\s*"[^"]*oliviaharper[^"]*"', re.I)
HREF_S = re.compile(r"href\s*=\s*'[^']*oliviaharper[^']*'", re.I)


def process(path):
    raw = pathlib.Path(path).read_text(encoding='utf-8')
    out = raw

    text_hits = 0
    for a, b in PAIRS:
        text_hits += out.count(a)
        out = out.replace(a, b)

    href_hits = len(HREF.findall(out)) + len(HREF_S.findall(out))
    out = HREF.sub('href=""', out)
    out = HREF_S.sub("href=''", out)

    if out != raw:
        pathlib.Path(path).write_text(out, encoding='utf-8')
    return text_hits, href_hits


def main():
    files = changed = total_text = total_href = 0
    for p in sorted(glob.glob('site/**/*.html', recursive=True)):
        files += 1
        t, h = process(p)
        if t or h:
            changed += 1
            total_text += t
            total_href += h
            print('%-55s text:%-3d href-blanked:%-3d' % (p, t, h))
    print('\nscanned %d files | %d changed | %d wordmark replacements | %d hrefs blanked'
          % (files, changed, total_text, total_href))


if __name__ == '__main__':
    main()
