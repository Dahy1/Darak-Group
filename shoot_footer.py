import asyncio, threading, functools, http.server, socketserver, os
from playwright.async_api import async_playwright
ROOT=os.path.join(os.getcwd(),'site'); PORT=8887
def serve():
    h=functools.partial(http.server.SimpleHTTPRequestHandler,directory=ROOT)
    socketserver.TCPServer.allow_reuse_address=True
    with socketserver.TCPServer(('127.0.0.1',PORT),h) as s: s.serve_forever()
async def shoot(p, vp, tag, dsf=1):
    b=await p.chromium.launch()
    pg=await b.new_page(viewport=vp, device_scale_factor=dsf)
    await pg.goto(f'http://127.0.0.1:{PORT}/about-us/',wait_until='load'); await pg.wait_for_timeout(1400)
    await pg.evaluate("()=>{const p=document.getElementById('ohPreloader');if(p)p.remove();}")
    await pg.wait_for_timeout(500)
    sw=await pg.evaluate("document.documentElement.scrollWidth"); iw=await pg.evaluate("window.innerWidth")
    print(tag,'overflow',{'sw':sw,'iw':iw})
    top=await pg.evaluate("()=>{const e=document.querySelector('.elementor-738');return e?e.getBoundingClientRect().top+window.scrollY:0;}")
    await pg.evaluate(f"window.scrollTo(0,{int(top)-20})"); await pg.wait_for_timeout(500)
    await pg.screenshot(path=f'shots/foot-{tag}-a.png')
    await pg.evaluate(f"window.scrollTo(0,{int(top)+ (vp['height']*0.7)})"); await pg.wait_for_timeout(400)
    await pg.screenshot(path=f'shots/foot-{tag}-b.png')
    await b.close()
async def main():
    threading.Thread(target=serve,daemon=True).start(); await asyncio.sleep(1)
    async with async_playwright() as p:
        await shoot(p, {'width':1440,'height':900}, 'd')
        await shoot(p, {'width':390,'height':844}, 'm', 2)
asyncio.run(main())
