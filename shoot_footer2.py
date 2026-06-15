import asyncio, threading, functools, http.server, socketserver, os
from playwright.async_api import async_playwright
ROOT=os.path.join(os.getcwd(),'site'); PORT=8889
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
    # screenshot just the footer element in full
    el = await pg.query_selector('.elementor-738')
    await el.scroll_into_view_if_needed(); await pg.wait_for_timeout(400)
    await el.screenshot(path=f'shots/footfull-{tag}.png')
    await b.close()
async def main():
    threading.Thread(target=serve,daemon=True).start(); await asyncio.sleep(1)
    async with async_playwright() as p:
        await shoot(p, {'width':1440,'height':2200}, 'd')
        await shoot(p, {'width':390,'height':1400}, 'm', 2)
asyncio.run(main())
