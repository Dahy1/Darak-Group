import asyncio, threading, functools, http.server, socketserver, os
from playwright.async_api import async_playwright
ROOT=os.path.join(os.getcwd(),'site'); PORT=8840
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
        await pg.goto(f'http://127.0.0.1:{PORT}/',wait_until='load'); await pg.wait_for_timeout(2800)
        await pg.evaluate("()=>{const p=document.getElementById('ohPreloader');if(p)p.remove();document.dispatchEvent(new Event('oh:preloaded'));}")
        await pg.wait_for_timeout(1200)
        # find impulse top
        top=await pg.evaluate("()=>{const e=document.getElementById('ohzImpulse'); const r=e.getBoundingClientRect(); return Math.round(window.scrollY + r.top);}")
        print('impulse top y=', top)
        # scroll through the pin (impulse height ~900 + 320% pin = ~3780 of scroll)
        for i,frac in enumerate([0.0, 0.30, 0.6, 0.9]):
            y = top + int(frac*3600) + 5
            await pg.evaluate(f"window.scrollTo(0,{y})"); await pg.wait_for_timeout(700)
            cnt=await pg.evaluate("()=>{const c=document.querySelector('[data-ohz-count]'); return c?c.textContent:'?';}")
            print(f'  frac {frac} -> counter {cnt}')
            await pg.screenshot(path=f'shots/imp-{i}.png')
        # button hover
        await pg.evaluate(f"window.scrollTo(0,{top})"); await pg.wait_for_timeout(500)
        btn=await pg.query_selector('#ohzImpulse .ohz-btn')
        if btn:
            await btn.hover(); await pg.wait_for_timeout(500)
            await pg.screenshot(path='shots/imp-btn-hover.png', clip={'x':720,'y':300,'width':620,'height':400})
        await b.close()
asyncio.run(main())
