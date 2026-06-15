import asyncio, threading, functools, http.server, socketserver, os
from playwright.async_api import async_playwright
ROOT=os.path.join(os.getcwd(),'site'); PORT=8883
def serve():
    h=functools.partial(http.server.SimpleHTTPRequestHandler,directory=ROOT)
    socketserver.TCPServer.allow_reuse_address=True
    with socketserver.TCPServer(('127.0.0.1',PORT),h) as s: s.serve_forever()
async def main():
    threading.Thread(target=serve,daemon=True).start(); await asyncio.sleep(1)
    async with async_playwright() as p:
        b=await p.chromium.launch()
        pg=await b.new_page(viewport={'width':390,'height':844},device_scale_factor=2)
        await pg.goto(f'http://127.0.0.1:{PORT}/about-us/',wait_until='load'); await pg.wait_for_timeout(1500)
        await pg.evaluate("()=>{const p=document.getElementById('ohPreloader');if(p)p.remove();}")
        await pg.wait_for_timeout(600)
        g=await pg.evaluate("()=>{const e=document.querySelector('.ohc2-gallery');const r=e.getBoundingClientRect();return {top:r.top+window.scrollY,h:r.height};}")
        print('gallery',g)
        base=int(g['top'])
        for i,off in enumerate([-120,150,420]):
            await pg.evaluate(f"window.scrollTo(0,{base+off})"); await pg.wait_for_timeout(500)
            await pg.screenshot(path=f'shots/mc-{i}.png')
        await b.close()
asyncio.run(main())
