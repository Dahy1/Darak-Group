import asyncio
from playwright.async_api import async_playwright
BASE='http://localhost:3000'
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch()
        pg=await b.new_page(viewport={'width':1440,'height':900},device_scale_factor=2)
        await pg.goto(BASE+'/about-us/',wait_until='load'); await pg.wait_for_timeout(2500)
        cta=await pg.query_selector('.zt-contact'); box=await cta.bounding_box()
        cx=box['x']+box['width']/2
        clip={'x':max(0,cx-130),'y':max(0,box['y']-24),'width':260,'height':72}
        # restart animations together for a known t0
        await pg.evaluate("()=>{document.querySelectorAll('.ztc-ar,.ztc-hand').forEach(e=>{e.style.animation='none';}); void document.body.offsetWidth; document.querySelectorAll('.ztc-ar-l').forEach(e=>e.style.animation='ztcArrowL 2.4s ease-in-out infinite'); document.querySelectorAll('.ztc-ar-r').forEach(e=>e.style.animation='ztcArrowR 2.4s ease-in-out infinite'); document.querySelectorAll('.ztc-hand').forEach(e=>e.style.animation='ztcHand 2.4s ease-in-out infinite');}")
        import time
        for i in range(16):
            await pg.screenshot(path=f'shots/seq-{i:02d}.png', clip=clip)
            await pg.wait_for_timeout(150)
        print('done', box)
        await b.close()
asyncio.run(main())
