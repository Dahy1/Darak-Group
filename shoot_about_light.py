import asyncio, threading, functools, http.server, socketserver, os
from playwright.async_api import async_playwright
ROOT=os.path.join(os.getcwd(),'site'); PORT=8885
def serve():
    h=functools.partial(http.server.SimpleHTTPRequestHandler,directory=ROOT)
    socketserver.TCPServer.allow_reuse_address=True
    with socketserver.TCPServer(('127.0.0.1',PORT),h) as s: s.serve_forever()
async def main():
    threading.Thread(target=serve,daemon=True).start(); await asyncio.sleep(1)
    async with async_playwright() as p:
        b=await p.chromium.launch()
        pg=await b.new_page(viewport={'width':1440,'height':900})
        await pg.goto(f'http://127.0.0.1:{PORT}/about-us/',wait_until='load'); await pg.wait_for_timeout(1500)
        await pg.evaluate("()=>{const p=document.getElementById('ohPreloader');if(p)p.remove();}")
        await pg.wait_for_timeout(700)
        H=await pg.evaluate("document.body.scrollHeight")
        # capture each named section top
        for tag,sel in [('story','.ohst'),('phil','.ohf-stage'),('philmv','.ohf-mv'),
                        ('board','.ohb'),('sub','.ohs2'),('cul','.ohc2')]:
            top=await pg.evaluate(f"()=>{{const e=document.querySelector('{sel}');return e?e.getBoundingClientRect().top+window.scrollY:0;}}")
            await pg.evaluate(f"window.scrollTo(0,{int(top)})"); await pg.wait_for_timeout(500)
            await pg.screenshot(path=f'shots/lt-{tag}.png')
        await b.close()
asyncio.run(main())
