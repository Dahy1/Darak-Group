import asyncio, threading, functools, http.server, socketserver, os
from playwright.async_api import async_playwright
ROOT=os.path.join(os.getcwd(),'site'); PORT=8884
def serve():
    h=functools.partial(http.server.SimpleHTTPRequestHandler,directory=ROOT)
    socketserver.TCPServer.allow_reuse_address=True
    with socketserver.TCPServer(('127.0.0.1',PORT),h) as s: s.serve_forever()
async def shoot(p, vp, dsf, tag):
    b=await p.chromium.launch()
    pg=await b.new_page(viewport=vp, device_scale_factor=dsf)
    await pg.goto(f'http://127.0.0.1:{PORT}/about-us/',wait_until='load'); await pg.wait_for_timeout(1400)
    await pg.evaluate("()=>{const p=document.getElementById('ohPreloader');if(p)p.remove();}")
    await pg.wait_for_timeout(500)
    sw=await pg.evaluate("document.documentElement.scrollWidth"); iw=await pg.evaluate("window.innerWidth")
    print(tag,'overflow',{'sw':sw,'iw':iw})
    top=await pg.evaluate("()=>{const e=document.querySelector('.ohst');return e?e.getBoundingClientRect().top+window.scrollY:0;}")
    for i,off in enumerate([0, int(vp['height']*0.55), int(vp['height']*1.05)]):
        await pg.evaluate(f"window.scrollTo(0,{int(top)+off})"); await pg.wait_for_timeout(450)
        await pg.screenshot(path=f'shots/story-{tag}-{i}.png')
    await b.close()
async def main():
    threading.Thread(target=serve,daemon=True).start(); await asyncio.sleep(1)
    async with async_playwright() as p:
        await shoot(p, {'width':1440,'height':900}, 1, 'd')
        await shoot(p, {'width':390,'height':844}, 2, 'm')
asyncio.run(main())
