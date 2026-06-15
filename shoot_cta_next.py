import asyncio
from playwright.async_api import async_playwright
BASE='http://localhost:3000'
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch()
        pg=await b.new_page(viewport={'width':1440,'height':900},device_scale_factor=2)
        await pg.goto(BASE+'/about-us/',wait_until='load'); await pg.wait_for_timeout(2500)
        cta=None
        for _ in range(20):
            cta=await pg.query_selector('.zt-contact')
            if cta:
                box=await cta.bounding_box()
                if box and box['width']>10: break
            await pg.wait_for_timeout(400)
        box=await cta.bounding_box(); print('cta box', box)
        cx=box['x']+box['width']/2
        clip={'x':max(0,cx-130),'y':max(0,box['y']-24),'width':260,'height':72}
        for i,frac in enumerate([0.10,0.32,0.45,0.55,0.66,0.80,0.95]):
            await pg.evaluate("(d)=>{document.querySelectorAll('.ztc-ar,.ztc-hand').forEach(e=>{e.style.animationDelay=(-d)+'s'; e.style.animationPlayState='paused';});}", frac*2.4)
            await pg.wait_for_timeout(140)
            await pg.screenshot(path=f'shots/ctan-{i}.png', clip=clip)
        print('done')
        await b.close()
asyncio.run(main())
