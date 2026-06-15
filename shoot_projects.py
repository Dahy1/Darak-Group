import asyncio, threading, functools, http.server, socketserver, os
from playwright.async_api import async_playwright
ROOT=os.path.join(os.getcwd(),'site'); PORT=8893
def serve():
    h=functools.partial(http.server.SimpleHTTPRequestHandler,directory=ROOT)
    socketserver.TCPServer.allow_reuse_address=True
    with socketserver.TCPServer(('127.0.0.1',PORT),h) as s: s.serve_forever()
async def shoot(p, url, vp, tag, dsf=1, expand=False, tabidx=None):
    b=await p.chromium.launch()
    pg=await b.new_page(viewport=vp, device_scale_factor=dsf)
    await pg.goto(f'http://127.0.0.1:{PORT}{url}',wait_until='load'); await pg.wait_for_timeout(1500)
    await pg.evaluate("()=>{const p=document.getElementById('ohPreloader');if(p)p.remove();}")
    await pg.wait_for_timeout(700)
    sw=await pg.evaluate("document.documentElement.scrollWidth"); iw=await pg.evaluate("window.innerWidth")
    if tabidx is not None:
        await pg.evaluate(f"()=>{{document.querySelectorAll('#ohProjects .ohpr-tab')[{tabidx}].click();}}")
        await pg.wait_for_timeout(600)
    if expand:
        await pg.evaluate("()=>{const b=document.querySelector('#ohProjects .ohpr-card:not(.is-hidden) [data-ohpr-open]');if(b)b.click();}")
        await pg.wait_for_timeout(900)
    el=await pg.query_selector('#ohProjects')
    await el.screenshot(path=f'shots/proj-{tag}.png')
    print(tag,'overflow',{'sw':sw,'iw':iw})
    await b.close()
async def main():
    threading.Thread(target=serve,daemon=True).start(); await asyncio.sleep(1)
    async with async_playwright() as p:
        await shoot(p, '/', {'width':1440,'height':2000}, 'home-d')
        await shoot(p, '/', {'width':1440,'height':2000}, 'home-expand', expand=True)
        await shoot(p, '/', {'width':1440,'height':2000}, 'home-filter', tabidx=1)
        await shoot(p, '/homes-projects/', {'width':1440,'height':2000}, 'page-d')
        await shoot(p, '/', {'width':390,'height':2200}, 'home-m', 2)
asyncio.run(main())
