# Mirror oliviaharperhomes.com into ./site as a static, root-relative clone.
# Reuses assets already downloaded by saveweb2zip (which bakes ?ver=V into
# filenames as name_ver=V.ext); anything missing is fetched from the live site.
import re
import time
import urllib.request
import urllib.parse
from pathlib import Path

ROOT = Path(r"C:\Users\Abd elrhman\Downloads\Darak\site")
HOST = "oliviaharperhomes.com"
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36")

ASSET_EXTS = {".css", ".js", ".jpg", ".jpeg", ".png", ".gif", ".svg", ".webp",
              ".mp4", ".webm", ".woff", ".woff2", ".ttf", ".otf", ".eot",
              ".ico", ".json", ".pdf", ".mp3"}
SKIP_PAGE_PAT = re.compile(
    r"(wp-json|xmlrpc\.php|/feed|/comments|/author/|\?s=|\?p=|\.php|/wp-admin|/wp-login)")

downloaded, failed, pages_saved = [], [], []


def fetch(url, binary=True, tries=2):
    req = urllib.request.Request(url, headers={"User-Agent": UA,
                                               "Accept": "*/*",
                                               "Accept-Language": "en-US,en;q=0.9"})
    for i in range(tries):
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                data = r.read()
            return data if binary else data.decode("utf-8", "replace")
        except Exception as e:
            if i == tries - 1:
                failed.append(f"{url} -> {e}")
                return None
            time.sleep(1)


def ver_named(path, query):
    """Disk filename scheme used by the existing download: name_ver=V.ext"""
    q = urllib.parse.parse_qs(query)
    ver = q.get("ver", [None])[0]
    p = Path(path)
    if ver and p.suffix:
        return p.with_name(f"{p.stem}_ver={ver}{p.suffix}")
    return None


def local_asset(url):
    """Map an asset URL to (disk_path, root_relative_ref). Downloads if absent."""
    u = urllib.parse.urlparse(url)
    if u.netloc == HOST:
        base = ROOT
        prefix = ""
    elif u.netloc == "cdnjs.cloudflare.com":
        base = ROOT / "cdnjs.cloudflare.com"
        prefix = "/cdnjs.cloudflare.com"
    else:
        return None  # leave other hosts untouched
    rel = urllib.parse.unquote(u.path.lstrip("/"))

    vn = ver_named(rel, u.query)
    if vn is not None and (base / vn).exists():
        ref = prefix + "/" + urllib.parse.quote(str(vn).replace("\\", "/"), safe="/")
        return (base / vn, ref)

    plain = base / rel
    if not plain.exists():
        data = fetch(url)
        if data is None:
            return None
        plain.parent.mkdir(parents=True, exist_ok=True)
        plain.write_bytes(data)
        downloaded.append(url)
        time.sleep(0.3)
    ref = prefix + "/" + urllib.parse.quote(rel, safe="/")
    return (plain, ref)


URL_RE = re.compile(
    r"https?://(?:" + re.escape(HOST) + r"|cdnjs\.cloudflare\.com)[^\"'\s\\)<>,]*")


def is_asset(url):
    path = urllib.parse.urlparse(url).path
    return Path(urllib.parse.unquote(path)).suffix.lower() in ASSET_EXTS


def rewrite_html(html, queue, seen):
    css_files = []

    def repl(m):
        url = m.group(0)
        u = urllib.parse.urlparse(url)
        if is_asset(url):
            res = local_asset(url)
            if res is None:
                return url
            disk, ref = res
            if disk.suffix == ".css":
                css_files.append(disk)
            return ref
        if u.netloc != HOST:
            return url
        # internal page link -> root-relative; queue for crawling
        path = u.path if u.path.startswith("/") else "/" + u.path
        if not SKIP_PAGE_PAT.search(url):
            norm = path.rstrip("/") or "/"
            if norm not in seen:
                seen.add(norm)
                queue.append(norm)
        return path + (("?" + u.query) if u.query and "?s=" not in url else "")

    # plain URLs
    html = URL_RE.sub(repl, html)
    # JSON-escaped URLs (https:\/\/host\/...) inside inline JS configs
    esc_re = re.compile(r"https?:\\/\\/" + re.escape(HOST) + r"[^\"']*")

    def esc_repl(m):
        url = m.group(0).replace("\\/", "/")
        u = urllib.parse.urlparse(url)
        if is_asset(url):
            res = local_asset(url)
            new = res[1] if res else url
        else:
            new = u.path + (("?" + u.query) if u.query else "")
        return new.replace("/", "\\/")

    html = esc_re.sub(esc_repl, html)
    return html, css_files


def process_css(css_path, done):
    if css_path in done or not css_path.exists():
        return
    done.add(css_path)
    text = css_path.read_text("utf-8", errors="replace")
    for m in re.finditer(r"url\(\s*['\"]?([^'\")]+)['\"]?\s*\)", text):
        ref = m.group(1).strip()
        if ref.startswith("data:"):
            continue
        if ref.startswith("http"):
            if HOST in ref:
                local_asset(ref)
            continue
        # relative to the css file's location on the original server
        clean = ref.split("?")[0].split("#")[0]
        target = (css_path.parent / urllib.parse.unquote(clean)).resolve()
        if not target.exists():
            # reconstruct original URL from disk layout
            try:
                rel_dir = css_path.parent.relative_to(ROOT)
            except ValueError:
                continue
            url = urllib.parse.urljoin(
                f"https://{HOST}/" + str(rel_dir).replace("\\", "/") + "/", clean)
            local_asset(url)


def page_disk_path(norm):
    if norm == "/":
        return ROOT / "index.html"
    return ROOT / norm.lstrip("/") / "index.html"


def main():
    seen = {"/"}
    queue = ["/"]
    all_css = []
    n = 0
    while queue and n < 60:
        norm = queue.pop(0)
        url = f"https://{HOST}{norm}" + ("" if norm == "/" else "/")
        html = fetch(url, binary=False)
        if html is None:
            continue
        n += 1
        html, css_files = rewrite_html(html, queue, seen)
        all_css.extend(css_files)
        out = page_disk_path(norm)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(html, encoding="utf-8")
        pages_saved.append(norm)
        print(f"PAGE {norm}  ({len(html)} bytes)")
        time.sleep(0.5)

    # also sweep every css on disk for nested url() assets
    done = set()
    for css in list(all_css) + list(ROOT.rglob("*.css")):
        process_css(Path(css), done)

    print(f"\npages: {len(pages_saved)}")
    print(f"assets downloaded: {len(downloaded)}")
    for d in downloaded:
        print("  +", d)
    if failed:
        print(f"FAILED: {len(failed)}")
        for f in failed:
            print("  !", f)


if __name__ == "__main__":
    main()
