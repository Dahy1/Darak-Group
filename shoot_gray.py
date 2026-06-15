import asyncio, threading, functools, http.server, socketserver, os
from playwright.async_api import async_playwright
ROOT=os.path.join(os.getcwd(),'site'); PORT=8810
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
        for route,name in [('/about-us/','g-about'),('/contact/','g-contact'),('/services/','g-services')]:
            await pg.goto(f'http://127.0.0.1:{PORT}{route}',wait_until='load'); await pg.wait_for_timeout(2000)
            await pg.evaluate("()=>{const p=document.getElementById('ohPreloader');if(p)p.remove();}")
            await pg.wait_for_timeout(900)
            await pg.screenshot(path=f'shots/{name}.png')
        # button hover check on contact submit
        await pg.goto(f'http://127.0.0.1:{PORT}/contact/',wait_until='load'); await pg.wait_for_timeout(1500)
        await pg.evaluate("()=>{const p=document.getElementById('ohPreloader');if(p)p.remove();}")
        btn=await pg.query_selector('.ohc-submit') or await pg.query_selector('button[type=submit]')
        if btn:
            await btn.scroll_into_view_if_needed(); await btn.hover(); await pg.wait_for_timeout(300)
            col=await pg.evaluate("()=>{const b=document.querySelector('.ohc-submit'); const c=getComputedStyle(b); return {bg:c.backgroundColor,color:c.color};}")
            print('submit hover:', col)
            await pg.screenshot(path='shots/g-btn-hover.png', clip={'x':350,'y':500,'width':760,'height':360})
        # hover a nav link + check computed
        await pg.evaluate("()=>{const a=document.querySelector('header a, .zt-inline a'); if(a) a.dispatchEvent(new MouseEvent('mouseover',{bubbles:true}));}")
        await b.close()
asyncio.run(main())
