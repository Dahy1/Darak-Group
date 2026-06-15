# Content pages (no full-bleed hero) need top padding so their first heading
# clears the fixed nav. Hero pages (about/projects) keep the homepage-style
# overlay (nav floats over the full-bleed hero). Putting the rule in <head>
# means build_next picks it up as a page style, so Next stays consistent too.
import glob, os, pathlib

PAD = '<style id="zt-innerpad">body{padding-top:clamp(72px,8vh,92px);}</style>'

inner = [p for p in glob.glob('site/**/index.html', recursive=True)
         if os.path.normpath(p) != os.path.normpath('site/index.html')]

for f in inner:
    html = pathlib.Path(f).read_text(encoding='utf-8')
    if 'zt-innerpad' in html:
        print('  already padded', f); continue
    if 'oha-hero' in html or 'ohp-hero' in html:
        print('  full-bleed hero -> overlay (no pad):', f); continue
    if '</head>' not in html:
        print('  !! no </head>', f); continue
    html = html.replace('</head>', PAD + '\n</head>', 1)
    pathlib.Path(f).write_text(html, encoding='utf-8')
    print('  padded', f)
