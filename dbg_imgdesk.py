import asyncio, threading, functools, http.server, socketserver, os
from playwright.async_api import async_playwright
ROOT=os.path.join(os.getcwd(),'site'); PORT=8843
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
        top=await pg.evaluate("()=>Math.round(window.scrollY+document.getElementById('ohzImpulse').getBoundingClientRect().top)")
        await pg.evaluate(f"window.scrollTo(0,{top})"); await pg.wait_for_timeout(700)
        info=await pg.evaluate("""()=>{const st=document.querySelector('#ohzImpulse .ohz-stack'); const imgs=[...document.querySelectorAll('#ohzImpulse .ohz-stack-img')];
          const r=e=>Math.round(e.getBoundingClientRect().height); return {stack:r(st), imgs:imgs.map(r)};}""")
        print(info)
        # scroll to last image revealed
        await pg.evaluate(f"window.scrollTo(0,{top+3000})"); await pg.wait_for_timeout(700)
        await pg.screenshot(path='shots/desk-fill.png')
        await b.close()
asyncio.run(main())
