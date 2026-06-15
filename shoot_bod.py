import asyncio, threading, functools, http.server, socketserver, os
from playwright.async_api import async_playwright
ROOT=os.path.join(os.getcwd(),'site'); PORT=8872
def serve():
    h=functools.partial(http.server.SimpleHTTPRequestHandler,directory=ROOT)
    socketserver.TCPServer.allow_reuse_address=True
    with socketserver.TCPServer(('127.0.0.1',PORT),h) as s: s.serve_forever()
async def main():
    threading.Thread(target=serve,daemon=True).start(); await asyncio.sleep(1)
    os.makedirs('shots',exist_ok=True)
    async with async_playwright() as p:
        b=await p.chromium.launch()
        pg=await b.new_page(viewport={'width':1440,'height':900})
        await pg.goto(f'http://127.0.0.1:{PORT}/about-us/',wait_until='load'); await pg.wait_for_timeout(1500)
        await pg.evaluate("()=>{const p=document.getElementById('ohPreloader');if(p)p.remove();}")
        await pg.wait_for_timeout(900)
        # philosophy stage (eyebrow + desc centered)
        await pg.evaluate("()=>{document.querySelector('.ohf-stage').scrollIntoView();}"); await pg.wait_for_timeout(800)
        await pg.screenshot(path='shots/v2-ohf.png')
        # BOD: scroll into the section and sample at a couple depths
        bodTop=await pg.evaluate("()=>Math.round(window.scrollY+document.querySelector('.ohb').getBoundingClientRect().top)")
        print('bod top y', bodTop)
        for i,off in enumerate([200, 900, 1600]):
            await pg.evaluate(f"window.scrollTo(0,{bodTop+off})"); await pg.wait_for_timeout(800)
            await pg.screenshot(path=f'shots/v2-bod-{i}.png')
        # check sticky title stays + card parallax y
        ys=await pg.evaluate("""()=>{const cards=[...document.querySelectorAll('.ohb-card')]; return cards.map(c=>Math.round(new DOMMatrix(getComputedStyle(c).transform).m42));}""")
        print('card parallax y now:', ys)
        await b.close()
asyncio.run(main())
