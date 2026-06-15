import asyncio, threading, functools, http.server, socketserver, os
from playwright.async_api import async_playwright
ROOT=os.path.join(os.getcwd(),'site'); PORT=8820
def serve():
    h=functools.partial(http.server.SimpleHTTPRequestHandler,directory=ROOT)
    socketserver.TCPServer.allow_reuse_address=True
    with socketserver.TCPServer(('127.0.0.1',PORT),h) as s: s.serve_forever()
async def main():
    threading.Thread(target=serve,daemon=True).start(); await asyncio.sleep(1)
    os.makedirs('shots',exist_ok=True)
    async with async_playwright() as p:
        b=await p.chromium.launch()
        m=await b.new_page(viewport={'width':390,'height':844},device_scale_factor=2,is_mobile=True)
        await m.goto(f'http://127.0.0.1:{PORT}/',wait_until='load'); await m.wait_for_timeout(2500)
        await m.evaluate("()=>{const p=document.getElementById('ohPreloader');if(p)p.remove();document.dispatchEvent(new Event('oh:preloaded'));}")
        await m.wait_for_timeout(900)
        await m.evaluate("()=>{const s=document.getElementById('ohzImpulse'); if(s) s.scrollIntoView();}")
        await m.wait_for_timeout(900)
        info=await m.evaluate("""()=>{
          const st=document.querySelector('#ohzImpulse .ohz-stack');
          const im=document.querySelector('#ohzImpulse .ohz-stack-img');
          const md=document.querySelector('#ohzImpulse .ohz-card-media');
          const r=e=>e?{w:Math.round(e.getBoundingClientRect().width),h:Math.round(e.getBoundingClientRect().height)}:null;
          const cs=im?getComputedStyle(im):null;
          return {stack:r(st), media:r(md), img:r(im), imgCss: cs?{height:cs.height,objectFit:cs.objectFit,position:cs.position}:null};
        }""")
        print(info)
        await m.screenshot(path='shots/impulse-m.png')
        await b.close()
asyncio.run(main())
