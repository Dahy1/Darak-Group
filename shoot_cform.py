import asyncio, threading, functools, http.server, socketserver, os
from playwright.async_api import async_playwright
ROOT=os.path.join(os.getcwd(),'site'); PORT=8806
def serve():
    h=functools.partial(http.server.SimpleHTTPRequestHandler,directory=ROOT)
    socketserver.TCPServer.allow_reuse_address=True
    with socketserver.TCPServer(('127.0.0.1',PORT),h) as s: s.serve_forever()
async def main():
    threading.Thread(target=serve,daemon=True).start(); await asyncio.sleep(1)
    os.makedirs('shots',exist_ok=True)
    async with async_playwright() as p:
        b=await p.chromium.launch()
        pg=await b.new_page(viewport={'width':1440,'height':1400},device_scale_factor=2)
        await pg.goto(f'http://127.0.0.1:{PORT}/contact/',wait_until='load'); await pg.wait_for_timeout(1800)
        await pg.evaluate("()=>{const p=document.getElementById('ohPreloader');if(p)p.remove();}")
        await pg.wait_for_timeout(800)
        f=await pg.query_selector('.ohc-form')
        if f:
            await f.scroll_into_view_if_needed(); await pg.wait_for_timeout(500)
            await f.screenshot(path='shots/ohc-form.png')
        # select open state
        await pg.evaluate("()=>{const s=document.getElementById('ohc-type'); if(s){s.selectedIndex=1; s.dispatchEvent(new Event('change'));}}")
        await pg.wait_for_timeout(300)
        await pg.screenshot(path='shots/ohc-page.png', clip={'x':0,'y':0,'width':1440,'height':1200})
        # mobile
        m=await b.new_page(viewport={'width':390,'height':844},device_scale_factor=2,is_mobile=True)
        await m.goto(f'http://127.0.0.1:{PORT}/contact/',wait_until='load'); await m.wait_for_timeout(1800)
        await m.evaluate("()=>{const p=document.getElementById('ohPreloader');if(p)p.remove();}")
        await m.wait_for_timeout(600)
        ov=await m.evaluate("()=>({sw:document.documentElement.scrollWidth,iw:window.innerWidth})")
        print('mobile overflow', ov)
        fm=await m.query_selector('.ohc-form')
        if fm:
            await fm.scroll_into_view_if_needed(); await m.wait_for_timeout(400)
            await fm.screenshot(path='shots/ohc-form-m.png')
        await b.close()
asyncio.run(main())
