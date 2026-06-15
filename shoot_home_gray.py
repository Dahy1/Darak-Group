import asyncio, threading, functools, http.server, socketserver, os
from playwright.async_api import async_playwright
ROOT=os.path.join(os.getcwd(),'site'); PORT=8811
def serve():
    h=functools.partial(http.server.SimpleHTTPRequestHandler,directory=ROOT)
    socketserver.TCPServer.allow_reuse_address=True
    with socketserver.TCPServer(('127.0.0.1',PORT),h) as s: s.serve_forever()
FORCE="""()=>{const p=document.getElementById('ohPreloader');if(p)p.remove();
  const ui=document.getElementById('ohsUI');if(ui){ui.hidden=false;document.body.appendChild(ui);}
  const f=document.querySelector('.ohs-finder');if(f){f.style.opacity='1';f.style.pointerEvents='auto';}
  document.dispatchEvent(new Event('oh:preloaded'));}"""
async def main():
    threading.Thread(target=serve,daemon=True).start(); await asyncio.sleep(1)
    async with async_playwright() as p:
        b=await p.chromium.launch()
        pg=await b.new_page(viewport={'width':1440,'height':900})
        await pg.goto(f'http://127.0.0.1:{PORT}/',wait_until='load'); await pg.wait_for_timeout(2500)
        await pg.evaluate(FORCE); await pg.wait_for_timeout(700)
        await pg.screenshot(path='shots/g-home-finder.png', clip={'x':0,'y':520,'width':1440,'height':380})
        await pg.evaluate("window.scrollTo(0,1500)"); await pg.wait_for_timeout(900)
        await pg.screenshot(path='shots/g-home-stats.png')
        await b.close()
asyncio.run(main())
