import asyncio, threading, functools, http.server, socketserver, os
from playwright.async_api import async_playwright
ROOT=os.path.join(os.getcwd(),'site'); PORT=8895
def serve():
    h=functools.partial(http.server.SimpleHTTPRequestHandler,directory=ROOT)
    socketserver.TCPServer.allow_reuse_address=True
    with socketserver.TCPServer(('127.0.0.1',PORT),h) as s: s.serve_forever()
async def full(p, url, vp, tag, dsf=1):
    b=await p.chromium.launch()
    pg=await b.new_page(viewport=vp, device_scale_factor=dsf)
    await pg.goto(f'http://127.0.0.1:{PORT}{url}',wait_until='load'); await pg.wait_for_timeout(1400)
    await pg.evaluate("()=>{const p=document.getElementById('ohPreloader');if(p)p.remove();}")
    await pg.wait_for_timeout(600)
    sw=await pg.evaluate("document.documentElement.scrollWidth"); iw=await pg.evaluate("window.innerWidth")
    print(tag,'overflow',{'sw':sw,'iw':iw})
    await pg.screenshot(path=f'shots/blog-{tag}.png', full_page=True)
    await b.close()
async def main():
    threading.Thread(target=serve,daemon=True).start(); await asyncio.sleep(1)
    async with async_playwright() as p:
        await full(p, '/blog/', {'width':1440,'height':1000}, 'list-d')
        await full(p, '/blog/building-by-hand/', {'width':1440,'height':1000}, 'art-d')
        await full(p, '/blog/', {'width':390,'height':844}, 'list-m', 2)
        await full(p, '/blog/building-by-hand/', {'width':390,'height':844}, 'art-m', 2)
asyncio.run(main())
