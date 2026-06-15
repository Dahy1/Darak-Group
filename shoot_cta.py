import asyncio, threading, functools, http.server, socketserver, os
from playwright.async_api import async_playwright
ROOT=os.path.join(os.getcwd(),'site'); PORT=8814
def serve():
    h=functools.partial(http.server.SimpleHTTPRequestHandler,directory=ROOT)
    socketserver.TCPServer.allow_reuse_address=True
    with socketserver.TCPServer(('127.0.0.1',PORT),h) as s: s.serve_forever()
async def main():
    threading.Thread(target=serve,daemon=True).start(); await asyncio.sleep(1)
    os.makedirs('shots',exist_ok=True)
    async with async_playwright() as p:
        b=await p.chromium.launch()
        pg=await b.new_page(viewport={'width':1440,'height':900},device_scale_factor=2)
        await pg.goto(f'http://127.0.0.1:{PORT}/',wait_until='load'); await pg.wait_for_timeout(1500)
        await pg.evaluate("()=>{const p=document.getElementById('ohPreloader');if(p)p.remove(); const n=document.getElementById('ztNav'); if(n){n.style.background='#0a0a0a';n.style.zIndex='99999';}}")
        await pg.wait_for_timeout(500)
        cta=await pg.query_selector('.zt-contact')
        if not cta:
            print('NO .zt-contact'); await b.close(); return
        box=await cta.bounding_box()
        print('cta box', box)
        cx=box['x']+box['width']/2
        clip={'x':max(0,cx-130),'y':max(0,box['y']-22),'width':260,'height':70}
        # pause CSS animations and step through fixed delays to land on each state
        for i,frac in enumerate([0.10,0.30,0.45,0.55,0.66,0.80,0.94]):
            await pg.evaluate("""(d)=>{document.querySelectorAll('.ztc-ar,.ztc-hand').forEach(e=>{e.style.animationDelay=(-d)+'s'; e.style.animationPlayState='paused';});}""", frac*2.4)
            await pg.wait_for_timeout(120)
            await pg.screenshot(path=f'shots/cta-{i}.png', clip=clip)
        await b.close()
asyncio.run(main())
