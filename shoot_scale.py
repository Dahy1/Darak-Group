import asyncio, threading, functools, http.server, socketserver, os
from playwright.async_api import async_playwright
ROOT=os.path.join(os.getcwd(),'site'); PORT=8896
def serve():
    h=functools.partial(http.server.SimpleHTTPRequestHandler,directory=ROOT)
    socketserver.TCPServer.allow_reuse_address=True
    with socketserver.TCPServer(('127.0.0.1',PORT),h) as s: s.serve_forever()
async def main():
    threading.Thread(target=serve,daemon=True).start(); await asyncio.sleep(1)
    async with async_playwright() as p:
        b=await p.chromium.launch()
        pg=await b.new_page(viewport={'width':1440,'height':820})
        await pg.goto(f'http://127.0.0.1:{PORT}/',wait_until='load'); await pg.wait_for_timeout(1600)
        await pg.evaluate("()=>{const p=document.getElementById('ohPreloader');if(p)p.remove();}")
        await pg.wait_for_timeout(600)
        base=await pg.evaluate("()=>{const e=document.getElementById('ohzFormat');return e.getBoundingClientRect().top+window.scrollY;}")
        vh=820
        # full-bleed sits ~progress 0.30-0.45 within a 300vh track (=> ~0.6-0.9 vh*? ) sample several
        for i,frac in enumerate([0.55,0.75,0.95,1.15]):
            y=int(base+frac*vh)
            await pg.evaluate(f"(y)=>{{if(window.__lenis&&window.__lenis.scrollTo)window.__lenis.scrollTo(y,{{immediate:true}});window.scrollTo(0,y);}}", y)
            await pg.wait_for_timeout(500)
            await pg.screenshot(path=f'shots/scale-{i}.png')
        await b.close()
asyncio.run(main())
