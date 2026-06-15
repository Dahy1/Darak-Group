import asyncio, threading, functools, http.server, socketserver, os
from playwright.async_api import async_playwright
ROOT=os.path.join(os.getcwd(),'_pagesdist'); PORT=8899; PREFIX='/Darak-Group'
class H(http.server.SimpleHTTPRequestHandler):
    def translate_path(self, path):
        # strip the /Darak-Group prefix so requests resolve inside _pagesdist
        if path.startswith(PREFIX):
            path = path[len(PREFIX):] or '/'
        return super().translate_path(path)
def serve():
    functools.partial  # noop
    handler=functools.partial(H, directory=ROOT)
    socketserver.TCPServer.allow_reuse_address=True
    with socketserver.TCPServer(('127.0.0.1',PORT),handler) as s: s.serve_forever()
async def main():
    threading.Thread(target=serve,daemon=True).start(); await asyncio.sleep(1)
    fails=[]
    async with async_playwright() as p:
        b=await p.chromium.launch()
        pg=await b.new_page(viewport={'width':1440,'height':900})
        pg.on('requestfailed', lambda r: fails.append(r.url))
        pg.on('response', lambda r: fails.append('HTTP%d %s'%(r.status,r.url)) if r.status>=400 else None)
        for path,tag in [('/Darak-Group/','home'),('/Darak-Group/about-us/','about'),('/Darak-Group/homes-projects/','projects'),('/Darak-Group/blog/','blog')]:
            del fails[:]
            await pg.goto(f'http://127.0.0.1:{PORT}{path}',wait_until='load'); await pg.wait_for_timeout(1500)
            await pg.evaluate("()=>{const p=document.getElementById('ohPreloader');if(p)p.remove();}")
            await pg.wait_for_timeout(500)
            await pg.screenshot(path=f'shots/pg-{tag}.png')
            bad=[u for u in fails if ('/wp-content' in u or '/wp-includes' in u or u.startswith('HTTP4') or u.startswith('HTTP5'))]
            print(tag, 'asset/4xx failures:', len(bad))
            for u in bad[:6]: print('   ', u)
        await b.close()
asyncio.run(main())
