# Audit the static clone: check every local ref resolves; list external refs.
import re
import urllib.parse
from pathlib import Path
from collections import Counter

ROOT = Path(r"C:\Users\Abd elrhman\Downloads\Darak\site")
missing, external = [], Counter()

ATTR_RE = re.compile(r'(?:href|src|poster|data-src|content)="([^"]+)"')
SRCSET_RE = re.compile(r'srcset="([^"]+)"')
URLFUNC_RE = re.compile(r'url\(\s*[\'"]?([^\'")]+)[\'"]?\s*\)')
ESC_RE = re.compile(r'"(\\/[^"]*)"')


def check(ref, page):
    ref = ref.strip()
    if not ref or ref.startswith(("data:", "#", "mailto:", "tel:", "javascript:")):
        return
    if ref.startswith(("http://", "https://", "//")):
        host = urllib.parse.urlparse(ref).netloc
        external[host] += 1
        if "oliviaharperhomes.com" in host:
            external["!!LEAK " + ref.split("?")[0]] += 1
        return
    if not ref.startswith("/"):
        return  # page-relative (rare); skip
    path = urllib.parse.unquote(ref.split("?")[0].split("#")[0])
    if path == "/" or path.endswith("/"):
        target = ROOT / path.lstrip("/") / "index.html"
    else:
        target = ROOT / path.lstrip("/")
        if not target.suffix:
            target = target / "index.html"
    if not target.exists():
        missing.append(f"{page}: {ref}")


for html_file in ROOT.rglob("*.html"):
    page = str(html_file.relative_to(ROOT))
    text = html_file.read_text("utf-8", errors="replace")
    for m in ATTR_RE.finditer(text):
        check(m.group(1), page)
    for m in SRCSET_RE.finditer(text):
        for item in m.group(1).split(","):
            check(item.strip().split(" ")[0], page)
    for m in URLFUNC_RE.finditer(text):
        check(m.group(1), page)
    for m in ESC_RE.finditer(text):
        check(m.group(1).replace("\\/", "/"), page)

print("MISSING local refs:", len(missing))
for x in sorted(set(missing)):
    print(" ", x)
print("\nEXTERNAL hosts:")
for host, n in external.most_common():
    print(f"  {n:4d}  {host}")
