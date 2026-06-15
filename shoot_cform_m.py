import asyncio, threading, functools, http.server, socketserver, os
from playwright.async_api import async_playwright
ROOT=os.path.join(os.getcwd(),'site'); PORT=8807
def serve():
    h=functools.partial(http.server.SimpleHTTPRequestHandler,directory=ROOT)
    socketserver.TCPServer.allow_reuse_address=True
    with socketserver.TCPServer(('127.0.0.1',PORT),h) as s: s.serve_forever()
async def main():
    threading.Thread(target=serve,daemon=True).start(); await asyncio.sleep(1)
    async with async_playwright() as p:
        b=await p.chromium.launch()
        m=await b.new_page(viewport={'width':390,'height':844},is_mobile=True)
        await m.goto(f'http://127.0.0.1:{PORT}/contact/',wait_until='load'); await m.wait_for_timeout(1800)
        await m.evaluate("()=>{const p=document.getElementById('ohPreloader');if(p)p.remove();}")
        await m.wait_for_timeout(600)
        await m.evaluate("()=>{const f=document.querySelector('.ohc-form'); if(f) f.scrollIntoView();}")
        await m.wait_for_timeout(500)
        await m.screenshot(path='shots/ohc-m-1.png')
        await m.evaluate("window.scrollBy(0,560)"); await m.wait_for_timeout(400)
        await m.screenshot(path='shots/ohc-m-2.png')
        await b.close()
asyncio.run(main())
