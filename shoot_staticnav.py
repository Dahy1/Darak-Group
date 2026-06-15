import asyncio, threading, functools, http.server, socketserver, os
from playwright.async_api import async_playwright
ROOT=os.path.join(os.getcwd(),'site'); PORT=8830
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
        for r in ['services','about-us','projects/normandy-shores','vision','contact']:
            await pg.goto(f'http://127.0.0.1:{PORT}/{r}/',wait_until='load'); await pg.wait_for_timeout(1500)
            await pg.evaluate("()=>{const p=document.getElementById('ohPreloader');if(p)p.remove();}")
            await pg.wait_for_timeout(500)
            info=await pg.evaluate("""()=>{const n=document.querySelector('.zt-nav'); const inl=document.querySelector('.zt-inline'); const ov=document.querySelector('.zt-overlay'); const lg=document.querySelector('.zt-logo-img');
              const vis=e=>{if(!e)return 'MISSING'; const c=getComputedStyle(e); return c.display+'/'+c.opacity;}
              return {nav:vis(n), inline:vis(inl), overlay:!!ov, logoW: lg?Math.round(lg.getBoundingClientRect().width):0};}""")
            print(f"{r:26} {info}")
        # screenshot services nav + open menu
        await pg.goto(f'http://127.0.0.1:{PORT}/services/',wait_until='load'); await pg.wait_for_timeout(1500)
        await pg.evaluate("()=>{const p=document.getElementById('ohPreloader');if(p)p.remove();}")
        await pg.wait_for_timeout(500)
        await pg.screenshot(path='shots/sn-services-nav.png', clip={'x':0,'y':0,'width':1440,'height':120})
        await pg.evaluate("()=>{const b=document.getElementById('ztBurger'); if(b) b.click();}")
        await pg.wait_for_timeout(900)
        await pg.screenshot(path='shots/sn-services-menu.png')
        await b.close()
asyncio.run(main())
