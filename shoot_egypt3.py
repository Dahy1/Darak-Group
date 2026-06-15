import asyncio, threading, functools, http.server, socketserver, os
from playwright.async_api import async_playwright
ROOT=os.path.join(os.getcwd(),'site'); PORT=8851
def serve():
    h=functools.partial(http.server.SimpleHTTPRequestHandler,directory=ROOT)
    socketserver.TCPServer.allow_reuse_address=True
    with socketserver.TCPServer(('127.0.0.1',PORT),h) as s: s.serve_forever()
async def main():
    threading.Thread(target=serve,daemon=True).start(); await asyncio.sleep(1)
    async with async_playwright() as p:
        b=await p.chromium.launch()
        pg=await b.new_page(viewport={'width':1440,'height':900})
        await pg.goto(f'http://127.0.0.1:{PORT}/',wait_until='load'); await pg.wait_for_timeout(2600)
        await pg.evaluate("()=>{const p=document.getElementById('ohPreloader');if(p)p.remove();document.dispatchEvent(new Event('oh:preloaded'));}")
        await pg.wait_for_timeout(1000)
        info=await pg.evaluate("""()=>{const t=document.querySelector('.ohz-format2-track'); const r=t.getBoundingClientRect(); return {top:Math.round(window.scrollY+r.top), h:Math.round(r.height), vh:window.innerHeight};}""")
        print(info)
        for frac in [0.62, 0.74]:
            y = info['top'] + int(frac*(info['h']-info['vh']))
            await pg.evaluate(f"window.scrollTo(0,{y})"); await pg.wait_for_timeout(900)
            await pg.screenshot(path=f'shots/egypt-live-{int(frac*100)}.png')
        await b.close()
asyncio.run(main())
