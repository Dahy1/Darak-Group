# Compare hero headline visibility and section inventory: local vs live.
from playwright.sync_api import sync_playwright

SITES = [("local", "http://localhost:8765/"), ("live", "https://oliviaharperhomes.com/")]

with sync_playwright() as p:
    browser = p.chromium.launch(channel="chrome", headless=True)
    for site, url in SITES:
        ctx = browser.new_context(viewport={"width": 1440, "height": 1080})
        page = ctx.new_page()
        page.goto(url, wait_until="networkidle", timeout=60000)
        page.wait_for_timeout(12000)
        info = page.evaluate("""() => {
            const heads = [...document.querySelectorAll('h1,h2')].slice(0, 12).map(h => {
                const s = getComputedStyle(h);
                const r = h.getBoundingClientRect();
                return {
                    text: h.textContent.trim().replace(/\\s+/g, ' ').slice(0, 40),
                    opacity: s.opacity, visibility: s.visibility,
                    y: Math.round(r.top + window.scrollY),
                };
            });
            return {
                sections: document.querySelectorAll('.e-con.e-parent').length,
                height: document.body.scrollHeight,
                videoReady: [...document.querySelectorAll('video')].map(v => v.readyState),
                heads,
            };
        }""")
        print(f"===== {site} =====")
        print("sections:", info["sections"], " height:", info["height"],
              " videoReady:", info["videoReady"])
        for h in info["heads"]:
            print(f"  y={h['y']:>6} op={h['opacity']:>4} vis={h['visibility']:<8} {h['text']}")
        ctx.close()
    browser.close()
