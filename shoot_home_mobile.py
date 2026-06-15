import asyncio, threading, functools, http.server, socketserver, os
from playwright.async_api import async_playwright
ROOT = os.path.join(os.getcwd(), 'site'); PORT = 8802
def serve():
    h = functools.partial(http.server.SimpleHTTPRequestHandler, directory=ROOT)
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(('127.0.0.1', PORT), h) as s: s.serve_forever()
async def main():
    threading.Thread(target=serve, daemon=True).start(); await asyncio.sleep(1)
    os.makedirs('shots', exist_ok=True)
    async with async_playwright() as p:
        b = await p.chromium.launch()
        m = await b.new_page(viewport={'width':390,'height':844}, device_scale_factor=2, is_mobile=True)
        await m.goto(f'http://127.0.0.1:{PORT}/', wait_until='load'); await m.wait_for_timeout(2500)
        await m.evaluate("()=>{const p=document.getElementById('ohPreloader'); if(p) p.remove(); document.dispatchEvent(new Event('oh:preloaded'));}")
        await m.wait_for_timeout(800)
        H = await m.evaluate("document.body.scrollHeight")
        print('home docH', H)
        positions = [600, 1500, 2600, 3700, 4800, 5900, 7000, 8000]
        for i, y in enumerate(positions):
            await m.evaluate(f"window.scrollTo(0,{y})"); await m.wait_for_timeout(700)
            ov = await m.evaluate("()=>({sw:document.documentElement.scrollWidth, iw:window.innerWidth})")
            flag = ' OVERFLOW' if ov['sw']>ov['iw']+1 else ''
            print(f"  y={y} scrollW={ov['sw']}{flag}")
            await m.screenshot(path=f'shots/mh-{i}-{y}.png')
        await b.close()
asyncio.run(main())
