# Download all webpack lazy-load chunks named in the Elementor runtimes.
import re
import time
import urllib.request
from pathlib import Path

ROOT = Path(r"C:\Users\Abd elrhman\Downloads\Darak\site")
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36")

RUNTIMES = [
    (ROOT / r"wp-content\plugins\elementor\assets\js\webpack.runtime.min_ver=4.1.1.js",
     "wp-content/plugins/elementor/assets/js"),
    (ROOT / r"wp-content\plugins\elementor-pro\assets\js\webpack-pro.runtime.min_ver=3.35.1.js",
     "wp-content/plugins/elementor-pro/assets/js"),
]
CHUNK_RE = re.compile(r'"((?:[\w-]+\.)?[0-9a-f]{16,24}\.bundle\.min\.js)"')

ok = missing = 0
for runtime, base in RUNTIMES:
    text = runtime.read_text("utf-8", errors="replace")
    names = sorted(set(CHUNK_RE.findall(text)))
    print(f"{runtime.name}: {len(names)} chunks")
    for name in names:
        dest = ROOT / base.replace("/", "\\") / name
        if dest.exists():
            continue
        url = f"https://oliviaharperhomes.com/{base}/{name}"
        req = urllib.request.Request(url, headers={"User-Agent": UA})
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                dest.write_bytes(r.read())
            ok += 1
        except Exception as e:
            print(f"  FAIL {name}: {e}")
            missing += 1
        time.sleep(0.2)
print(f"downloaded={ok} failed={missing}")
