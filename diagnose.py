# Compare console errors / failed requests / preloader state: local vs live.
import sys
from playwright.sync_api import sync_playwright

SITES = [("local", "http://localhost:8765/"), ("live", "https://oliviaharperhomes.com/")]

with sync_playwright() as p:
    browser = p.chromium.launch(channel="chrome", headless=True)
    for site, url in SITES:
        ctx = browser.new_context(viewport={"width": 1440, "height": 1080})
        page = ctx.new_page()
        console, failures = [], []
        page.on("console", lambda m, c=console: c.append(f"{m.type}: {m.text}"))
        page.on("response", lambda r, f=failures: f.append(f"{r.status} {r.url}")
                if r.status >= 400 else None)
        page.on("requestfailed", lambda r, f=failures: f.append(f"FAILED {r.url} {r.failure}"))
        try:
            page.goto(url, wait_until="load", timeout=60000)
        except Exception as e:
            print(f"[{site}] goto error: {e}")
        page.wait_for_timeout(10000)
        state = page.evaluate("""() => {
            const b = getComputedStyle(document.body);
            const hero = document.querySelector('.e-con.e-parent');
            const pre = document.querySelector('[class*="preloader" i], [id*="preloader" i], [class*="loader" i]');
            return {
                bodyOpacity: b.opacity, bodyVisibility: b.visibility, bodyOverflow: b.overflow,
                heroVisible: hero ? getComputedStyle(hero).opacity : 'none',
                preloader: pre ? pre.className + ' | display=' + getComputedStyle(pre).display + ' opacity=' + getComputedStyle(pre).opacity : 'none',
                gsap: typeof window.gsap, SplitText: typeof window.SplitText,
                jQuery: typeof window.jQuery,
            };
        }""")
        print(f"\n===== {site} =====")
        print("STATE:", state)
        print("FAILED REQUESTS:")
        for f in sorted(set(failures)):
            print("  ", f)
        print("CONSOLE (errors/warnings):")
        for c in console:
            if c.startswith(("error", "warning")):
                print("  ", c[:300])
        ctx.close()
    browser.close()
