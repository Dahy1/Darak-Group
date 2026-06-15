import asyncio, threading, functools, http.server, socketserver, os
from playwright.async_api import async_playwright
ROOT=os.path.join(os.getcwd(),'site'); PORT=8814
def serve():
    h=functools.partial(http.server.SimpleHTTPRequestHandler,directory=ROOT)
    socketserver.TCPServer.allow_reuse_address=True
    with socketserver.TCPServer(('127.0.0.1',PORT),h) as s: s.serve_forever()
async def main():
    threading.Thread(target=serve,daemon=True).start(); await asyncio.sleep(1)
    async with async_playwright() as p:
        b=await p.chromium.launch()
        m=await b.new_page(viewport={'width':380,'height':820},device_scale_factor=2,is_mobile=True)
        await m.goto(f'http://127.0.0.1:{PORT}/about-us/',wait_until='load'); await m.wait_for_timeout(2000)
        await m.evaluate("()=>{const p=document.getElementById('ohPreloader');if(p)p.remove();}")
        await m.wait_for_timeout(1200)
        info=await m.evaluate("""()=>{const c=document.querySelector('.zt-contact'); if(!c) return 'NO CONTACT'; const cs=getComputedStyle(c); const r=c.getBoundingClientRect(); return {display:cs.display, color:cs.color, fontSize:cs.fontSize, x:Math.round(r.x), w:Math.round(r.width), visible:r.width>0};}""")
        print('zt-contact @380px:', info)
        await m.screenshot(path='shots/t2-contact-dark.png', clip={'x':0,'y':0,'width':380,'height':100})
        await b.close()
asyncio.run(main())
