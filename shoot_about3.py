import asyncio, threading, functools, http.server, socketserver, os
from playwright.async_api import async_playwright
ROOT=os.path.join(os.getcwd(),'site'); PORT=8873
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
        # BOD heading + image cards
        await pg.evaluate("()=>{document.querySelector('.ohb').scrollIntoView();}"); await pg.wait_for_timeout(800)
        await pg.screenshot(path='shots/v3-bod.png')
        # sub-brands stacking
        await pg.evaluate("()=>{document.querySelector('.ohs2').scrollIntoView();}"); await pg.wait_for_timeout(800)
        await pg.screenshot(path='shots/v3-sub.png')
        # culture gallery
        await pg.evaluate("()=>{document.querySelector('.ohc2').scrollIntoView();}"); await pg.wait_for_timeout(800)
        await pg.screenshot(path='shots/v3-culture.png')
        m=await b.new_page(viewport={'width':390,'height':844},device_scale_factor=2,is_mobile=True)
        await m.goto(f'http://127.0.0.1:{PORT}/about-us/',wait_until='load'); await m.wait_for_timeout(1500)
        ov=await m.evaluate("()=>({sw:document.documentElement.scrollWidth,iw:window.innerWidth})")
        print('mobile overflow', ov)
        await b.close()
asyncio.run(main())
