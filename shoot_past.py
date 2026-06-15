import asyncio, threading, functools, http.server, socketserver, os
from playwright.async_api import async_playwright
ROOT=os.path.join(os.getcwd(),'site'); PORT=8842
def serve():
    h=functools.partial(http.server.SimpleHTTPRequestHandler,directory=ROOT)
    socketserver.TCPServer.allow_reuse_address=True
    with socketserver.TCPServer(('127.0.0.1',PORT),h) as s: s.serve_forever()
async def main():
    threading.Thread(target=serve,daemon=True).start(); await asyncio.sleep(1)
    async with async_playwright() as p:
        b=await p.chromium.launch()
        pg=await b.new_page(viewport={'width':1440,'height':900})
        await pg.goto(f'http://127.0.0.1:{PORT}/',wait_until='load'); await pg.wait_for_timeout(2800)
        await pg.evaluate("()=>{const p=document.getElementById('ohPreloader');if(p)p.remove();document.dispatchEvent(new Event('oh:preloaded'));}")
        await pg.wait_for_timeout(1000)
        H=await pg.evaluate("document.body.scrollHeight"); print('docH',H)
        # scroll well past impulse pin into format2 and beyond
        for i,y in enumerate([6800, 8200, 10500, 12500]):
            await pg.evaluate(f"window.scrollTo(0,{y})"); await pg.wait_for_timeout(800)
            ov=await pg.evaluate("()=>({sw:document.documentElement.scrollWidth,iw:window.innerWidth})")
            print(f'  y={y} sw={ov["sw"]}{" OVERFLOW" if ov["sw"]>ov["iw"]+1 else ""}')
            await pg.screenshot(path=f'shots/past-{i}.png')
        await b.close()
asyncio.run(main())
