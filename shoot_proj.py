import asyncio, threading, functools, http.server, socketserver, os
from playwright.async_api import async_playwright

ROOT = os.path.join(os.getcwd(), 'site')
PORT = 8799

def serve():
    h = functools.partial(http.server.SimpleHTTPRequestHandler, directory=ROOT)
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(('127.0.0.1', PORT), h) as httpd:
        httpd.serve_forever()

async def main():
    threading.Thread(target=serve, daemon=True).start()
    await asyncio.sleep(1)
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await b.new_page(viewport={'width':1440,'height':900})
        await pg.goto(f'http://127.0.0.1:{PORT}/projects/normandy-shores/', wait_until='load', timeout=60000)
        # kill preloader if present
        await pg.evaluate("()=>{const e=document.getElementById('ohPreloader'); if(e) e.remove(); document.dispatchEvent(new Event('oh:preloaded'));}")
        await pg.wait_for_timeout(2500)
        docH = await pg.evaluate("document.body.scrollHeight"); vh = 900
        print('docH', docH)
        n = 0; y = 0
        os.makedirs('shots', exist_ok=True)
        while y < docH and n < 22:
            await pg.evaluate(f"window.scrollTo(0,{y})"); await pg.wait_for_timeout(700)
            await pg.screenshot(path=f'shots/p-{n:02d}.png')
            docH = await pg.evaluate("document.body.scrollHeight"); y += int(vh*0.9); n += 1
        print('captured', n, 'finalDocH', docH)
        await b.close()

asyncio.run(main())
