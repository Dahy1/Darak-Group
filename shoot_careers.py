import asyncio, threading, functools, http.server, socketserver, os
from playwright.async_api import async_playwright
ROOT=os.path.join(os.getcwd(),'site'); PORT=8860
def serve():
    h=functools.partial(http.server.SimpleHTTPRequestHandler,directory=ROOT)
    socketserver.TCPServer.allow_reuse_address=True
    with socketserver.TCPServer(('127.0.0.1',PORT),h) as s: s.serve_forever()
async def main():
    threading.Thread(target=serve,daemon=True).start(); await asyncio.sleep(1)
    os.makedirs('shots',exist_ok=True)
    async with async_playwright() as p:
        b=await p.chromium.launch()
        pg=await b.new_page(viewport={'width':1440,'height':1000})
        r=await pg.goto(f'http://127.0.0.1:{PORT}/careers/',wait_until='load')
        print('careers status', r.status)
        await pg.wait_for_timeout(1200)
        await pg.evaluate("()=>{const p=document.getElementById('ohPreloader');if(p)p.remove();}")
        await pg.wait_for_timeout(500)
        await pg.screenshot(path='shots/careers-top.png')
        await pg.evaluate("()=>{const r=document.querySelector('.ohk-roles'); if(r) r.scrollIntoView();}")
        await pg.wait_for_timeout(500)
        await pg.screenshot(path='shots/careers-roles.png')
        rs=await pg.goto(f'http://127.0.0.1:{PORT}/services/',wait_until='load')
        print('services status', rs.status)
        await b.close()
asyncio.run(main())
