import asyncio, threading, functools, http.server, socketserver, os
from playwright.async_api import async_playwright

ROOT = os.path.join(os.getcwd(), 'site'); PORT = 8801
def serve():
    h = functools.partial(http.server.SimpleHTTPRequestHandler, directory=ROOT)
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(('127.0.0.1', PORT), h) as s: s.serve_forever()

FORCE_FINDER = """()=>{
  const p=document.getElementById('ohPreloader'); if(p) p.remove();
  const ui=document.getElementById('ohsUI'); if(ui){ ui.hidden=false; document.body.appendChild(ui); }
  const f=document.querySelector('.ohs-finder'); if(f){ f.style.opacity='1'; f.style.pointerEvents='auto'; }
  document.dispatchEvent(new Event('oh:preloaded'));
}"""

async def overflow(pg):
    return await pg.evaluate("()=>({sw:document.documentElement.scrollWidth, iw:window.innerWidth, h:document.body.scrollHeight})")

async def main():
    threading.Thread(target=serve, daemon=True).start(); await asyncio.sleep(1)
    os.makedirs('shots', exist_ok=True)
    async with async_playwright() as p:
        b = await p.chromium.launch()
        # ---------- DESKTOP: custom select ----------
        pg = await b.new_page(viewport={'width':1440,'height':900})
        await pg.goto(f'http://127.0.0.1:{PORT}/', wait_until='load'); await pg.wait_for_timeout(1800)
        await pg.evaluate(FORCE_FINDER); await pg.wait_for_timeout(600)
        await pg.screenshot(path='shots/sel-closed.png', clip={'x':0,'y':560,'width':1440,'height':340})
        # open first custom select
        await pg.evaluate("()=>{const t=document.querySelector('.ohs-finder .ohs-select-trigger'); if(t) t.click();}")
        await pg.wait_for_timeout(700)
        await pg.screenshot(path='shots/sel-open.png', clip={'x':0,'y':300,'width':1440,'height':600})
        await pg.close()

        # ---------- MOBILE audit ----------
        pages = ['/', '/about-us/', '/projects/normandy-shores/', '/services/', '/vision/', '/contact/']
        m = await b.new_page(viewport={'width':390,'height':844}, device_scale_factor=2, is_mobile=True)
        for route in pages:
            await m.goto(f'http://127.0.0.1:{PORT}{route}', wait_until='load'); await m.wait_for_timeout(1500)
            await m.evaluate("()=>{const p=document.getElementById('ohPreloader'); if(p) p.remove();}")
            await m.wait_for_timeout(400)
            ov = await overflow(m)
            tag = route.strip('/').replace('/','_') or 'home'
            flag = '  <-- HORIZONTAL OVERFLOW' if ov['sw'] > ov['iw']+1 else ''
            print(f"{tag:24} scrollW={ov['sw']} innerW={ov['iw']} docH={ov['h']}{flag}")
            await m.screenshot(path=f'shots/m-{tag}-top.png')
        # home finder on mobile
        await m.goto(f'http://127.0.0.1:{PORT}/', wait_until='load'); await m.wait_for_timeout(1600)
        await m.evaluate(FORCE_FINDER); await m.wait_for_timeout(500)
        await m.screenshot(path='shots/m-home-finder.png')
        await m.evaluate("()=>{const t=document.querySelector('.ohs-finder .ohs-select-trigger'); if(t) t.click();}")
        await m.wait_for_timeout(600)
        await m.screenshot(path='shots/m-home-finder-open.png')
        await b.close()

asyncio.run(main())
