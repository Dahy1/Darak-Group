import asyncio, threading, functools, http.server, socketserver, os
from playwright.async_api import async_playwright
ROOT=os.path.join(os.getcwd(),'site'); PORT=8871
def serve():
    h=functools.partial(http.server.SimpleHTTPRequestHandler,directory=ROOT)
    socketserver.TCPServer.allow_reuse_address=True
    with socketserver.TCPServer(('127.0.0.1',PORT),h) as s: s.serve_forever()
async def main():
    threading.Thread(target=serve,daemon=True).start(); await asyncio.sleep(1)
    os.makedirs('shots',exist_ok=True)
    async with async_playwright() as p:
        b=await p.chromium.launch()
        pg=await b.new_page(viewport={'width':1440,'height':900})
        await pg.goto(f'http://127.0.0.1:{PORT}/about-us/',wait_until='load'); await pg.wait_for_timeout(1500)
        await pg.evaluate("()=>{const p=document.getElementById('ohPreloader');if(p)p.remove();}")
        await pg.wait_for_timeout(900)
        # scroll to the philosophy stage
        await pg.evaluate("()=>{document.querySelector('.ohf-stage').scrollIntoView();}")
        await pg.wait_for_timeout(900)
        await pg.screenshot(path='shots/ohf-stage.png')
        # marquee direction: sample x while scrolling down then up
        await pg.evaluate("window.scrollBy(0,400)"); await pg.wait_for_timeout(120)
        x1=await pg.evaluate("()=>{const t=document.querySelector('[data-ohf-marquee]');return new DOMMatrix(getComputedStyle(t).transform).m41;}")
        await pg.evaluate("window.scrollBy(0,-400)"); await pg.wait_for_timeout(120)
        x2=await pg.evaluate("()=>{const t=document.querySelector('[data-ohf-marquee]');return new DOMMatrix(getComputedStyle(t).transform).m41;}")
        print('marquee x after down:',round(x1,1),'after up:',round(x2,1))
        # floating cards
        await pg.evaluate("()=>{document.querySelector('.ohf-mv').scrollIntoView();}")
        await pg.wait_for_timeout(900)
        await pg.screenshot(path='shots/ohf-cards.png')
        await b.close()
asyncio.run(main())
