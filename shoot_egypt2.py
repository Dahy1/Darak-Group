import asyncio, threading, functools, http.server, socketserver, os
from playwright.async_api import async_playwright
ROOT=os.path.join(os.getcwd(),'site'); PORT=8850
def serve():
    h=functools.partial(http.server.SimpleHTTPRequestHandler,directory=ROOT)
    socketserver.TCPServer.allow_reuse_address=True
    with socketserver.TCPServer(('127.0.0.1',PORT),h) as s: s.serve_forever()
async def main():
    threading.Thread(target=serve,daemon=True).start(); await asyncio.sleep(1)
    async with async_playwright() as p:
        b=await p.chromium.launch()
        pg=await b.new_page(viewport={'width':1440,'height':900})
        await pg.goto(f'http://127.0.0.1:{PORT}/',wait_until='load'); await pg.wait_for_timeout(2600)
        await pg.evaluate("()=>{const p=document.getElementById('ohPreloader');if(p)p.remove();document.dispatchEvent(new Event('oh:preloaded'));}")
        await pg.wait_for_timeout(1000)
        # reveal the expansion map directly for a clean shot
        await pg.evaluate("""()=>{
          const exp=document.getElementById('ohzExpansion'); if(exp) exp.scrollIntoView();
          const sf=document.querySelector('[data-ohz-scale]'); if(sf){sf.style.opacity='0';}
          const head=document.querySelector('[data-ohz-exphead]'); const map=document.querySelector('.ohz-exp-map');
          [head,map].forEach(e=>{if(e){e.style.transform='none';e.style.opacity='1';}});
          document.querySelectorAll('.exp-pin').forEach(p=>{p.style.opacity='1';p.style.transform='translate(-50%,-50%)';p.style.visibility='visible';});
        }""")
        await pg.wait_for_timeout(700)
        await pg.screenshot(path='shots/egypt-section.png')
        # hover a pin
        await pg.evaluate("()=>{const p=document.querySelector('.exp-pin[aria-label=\"Cairo\"]'); if(p) p.dispatchEvent(new MouseEvent('mouseover',{bubbles:true}));}")
        await pg.wait_for_timeout(400)
        await pg.screenshot(path='shots/egypt-pin.png')
        await b.close()
asyncio.run(main())
