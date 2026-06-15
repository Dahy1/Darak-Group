# Capture local clone vs live site at matching scroll positions.
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright

SHOTS = Path(r"C:\Users\Abd elrhman\Downloads\Darak\shots")
PAGES = [
    ("home", "/"),
    ("about", "/about-us/"),
    ("projects", "/homes-projects/"),
    ("project-normandy", "/projects/normandy-shores/"),
    ("contact", "/contact/"),
]
SITES = [("local", "http://localhost:8765"), ("live", "https://oliviaharperhomes.com")]


def shoot(page, site, name, base, path):
    page.goto(base + path, wait_until="networkidle", timeout=60000)
    page.wait_for_timeout(6000)  # let intro animation finish
    h = page.evaluate("document.body.scrollHeight")
    positions = [0, int(h * 0.33), int(h * 0.66), max(0, h - 1080)]
    for i, y in enumerate(positions):
        page.evaluate(f"window.scrollTo(0, {y})")
        page.wait_for_timeout(2500)  # let scroll-triggered animations settle
        page.screenshot(path=str(SHOTS / f"{site}-{name}-{i}.png"))
    print(f"{site} {name}: height={h}")


with sync_playwright() as p:
    browser = p.chromium.launch(channel="chrome", headless=True)
    ctx = browser.new_context(viewport={"width": 1440, "height": 1080})
    page = ctx.new_page()
    only = sys.argv[1] if len(sys.argv) > 1 else None
    for name, path in PAGES:
        if only and only != name:
            continue
        for site, base in SITES:
            try:
                shoot(page, site, name, base, path)
            except Exception as e:
                print(f"FAIL {site} {name}: {e}")
    browser.close()
print("done")
