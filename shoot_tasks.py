import asyncio, threading, functools, http.server, socketserver, os
from playwright.async_api import async_playwright
ROOT=os.path.join(os.getcwd(),'site'); PORT=8813
def serve():
    h=functools.partial(http.server.SimpleHTTPRequestHandler,directory=ROOT)
    socketserver.TCPServer.allow_reuse_address=True
    with socketserver.TCPServer(('127.0.0.1',PORT),h) as s: s.serve_forever()
async def main():
    threading.Thread(target=serve,daemon=True).start(); await asyncio.sleep(1)
    os.makedirs('shots',exist_ok=True)
    async with async_playwright() as p:
        b=await p.chromium.launch()
        # Preloader text (capture early, before it's removed)
        pg=await b.new_page(viewport={'width':1440,'height':900})
        await pg.goto(f'http://127.0.0.1:{PORT}/',wait_until='commit')
        await pg.wait_for_timeout(700)
        await pg.screenshot(path='shots/t1-preloader.png')
        # Impulse section: scroll to it; capture + hover the View projects button
        await pg.wait_for_timeout(2500)
        await pg.evaluate("()=>{const p=document.getElementById('ohPreloader');if(p)p.remove();}")
        await pg.evaluate("()=>{const s=document.getElementById('ohzImpulse'); if(s) s.scrollIntoView();}")
        await pg.wait_for_timeout(1200)
        await pg.screenshot(path='shots/t4-impulse.png')
        btn=await pg.query_selector('#ohzImpulse .ohz-btn')
        if btn:
            await btn.hover(); await pg.wait_for_timeout(450)
            await pg.screenshot(path='shots/t4-btn-hover.png')
        # Stats section parallax — sample colA/colB transforms at two scroll depths
        await pg.evaluate("()=>{const g=document.querySelector('.ohx-grid'); if(g) g.scrollIntoView({block:'center'});}")
        await pg.wait_for_timeout(700)
        t1=await pg.evaluate("()=>({a:(document.querySelector('.ohx-stats-col--a')||{}).style&&document.querySelector('.ohx-stats-col--a').style.transform, b:(document.querySelector('.ohx-stats-col--b')||{}).style&&document.querySelector('.ohx-stats-col--b').style.transform})")
        await pg.evaluate("window.scrollBy(0,500)"); await pg.wait_for_timeout(600)
        t2=await pg.evaluate("()=>({a:document.querySelector('.ohx-stats-col--a').style.transform, b:document.querySelector('.ohx-stats-col--b').style.transform})")
        print('stats transforms @center:', t1)
        print('stats transforms @+500:', t2)
        await pg.evaluate("()=>{const g=document.querySelector('.ohx-grid'); if(g) g.scrollIntoView({block:'center'});}")
        await pg.wait_for_timeout(500)
        await pg.screenshot(path='shots/t3-stats.png')
        await pg.close()
        # Mobile: contact button visible + stats parallax
        m=await b.new_page(viewport={'width':380,'height':820},device_scale_factor=2,is_mobile=True)
        await m.goto(f'http://127.0.0.1:{PORT}/',wait_until='load'); await m.wait_for_timeout(2500)
        await m.evaluate("()=>{const p=document.getElementById('ohPreloader');if(p)p.remove();}")
        await m.wait_for_timeout(500)
        await m.screenshot(path='shots/t2-mobile-nav.png', clip={'x':0,'y':0,'width':380,'height':110})
        await b.close()
asyncio.run(main())
