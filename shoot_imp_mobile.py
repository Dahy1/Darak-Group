import asyncio, threading, functools, http.server, socketserver, os
from playwright.async_api import async_playwright
ROOT=os.path.join(os.getcwd(),'site'); PORT=8841
def serve():
    h=functools.partial(http.server.SimpleHTTPRequestHandler,directory=ROOT)
    socketserver.TCPServer.allow_reuse_address=True
    with socketserver.TCPServer(('127.0.0.1',PORT),h) as s: s.serve_forever()
async def main():
    threading.Thread(target=serve,daemon=True).start(); await asyncio.sleep(1)
    async with async_playwright() as p:
        b=await p.chromium.launch()
        m=await b.new_page(viewport={'width':390,'height':844},device_scale_factor=2,is_mobile=True)
        await m.goto(f'http://127.0.0.1:{PORT}/',wait_until='load'); await m.wait_for_timeout(2500)
        await m.evaluate("()=>{const p=document.getElementById('ohPreloader');if(p)p.remove();document.dispatchEvent(new Event('oh:preloaded'));}")
        await m.wait_for_timeout(800)
        await m.evaluate("()=>{document.getElementById('ohzImpulse').scrollIntoView();}")
        await m.wait_for_timeout(900)
        chk=await m.evaluate("""()=>{const s3=document.querySelector('.ohz-step3'); const cnt=document.querySelector('.ohz-stack-count'); const img=document.querySelector('#ohzImpulse .ohz-stack-img'); return {step3disp:s3?getComputedStyle(s3).display:'-', countDisp:cnt?getComputedStyle(cnt).display:'-', imgH:img?Math.round(img.getBoundingClientRect().height):0};}""")
        print('mobile impulse:', chk)
        await m.screenshot(path='shots/imp-mobile.png')
        await b.close()
asyncio.run(main())
