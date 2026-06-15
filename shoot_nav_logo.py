import asyncio
from playwright.async_api import async_playwright
BASE='http://localhost:3000'
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch()
        pg=await b.new_page(viewport={'width':1440,'height':900})
        # nav across pages — capture top strip
        for r,name in [('','home'),('about-us','about'),('services','services'),('projects/normandy-shores','project'),('contact','contact')]:
            await pg.goto(f'{BASE}/{r}/' if r else f'{BASE}/', wait_until='load'); await pg.wait_for_timeout(2000)
            await pg.evaluate("()=>{const p=document.getElementById('ohPreloader');if(p)p.remove();}")
            await pg.wait_for_timeout(600)
            info=await pg.evaluate("""()=>{const i=document.querySelector('.zt-logo-img'); const r=i&&i.getBoundingClientRect(); return {found:!!i, w:r?Math.round(r.width):0, h:r?Math.round(r.height):0, src:i?i.getAttribute('src'):null};}""")
            print(f"{name:9} logo {info}")
            await pg.screenshot(path=f'shots/nav-{name}.png', clip={'x':0,'y':0,'width':1440,'height':96})
        # footer logo (scroll to bottom of about-us)
        await pg.goto(f'{BASE}/about-us/', wait_until='load'); await pg.wait_for_timeout(1500)
        await pg.evaluate("()=>{const p=document.getElementById('ohPreloader');if(p)p.remove(); window.scrollTo(0,document.body.scrollHeight);}")
        await pg.wait_for_timeout(1200)
        await pg.screenshot(path='shots/footer-logo.png', clip={'x':0,'y':300,'width':1440,'height':560})
        await pg.close()
        # mobile impulse image fill
        m=await b.new_page(viewport={'width':390,'height':844},device_scale_factor=2,is_mobile=True)
        await m.goto(f'{BASE}/', wait_until='load'); await m.wait_for_timeout(2500)
        await m.evaluate("()=>{const p=document.getElementById('ohPreloader');if(p)p.remove();document.dispatchEvent(new Event('oh:preloaded'));}")
        await m.wait_for_timeout(900)
        await m.evaluate("()=>{const s=document.getElementById('ohzImpulse'); if(s) s.scrollIntoView();}")
        await m.wait_for_timeout(900)
        dims=await m.evaluate("""()=>{const st=document.querySelector('#ohzImpulse .ohz-stack'); const im=document.querySelector('#ohzImpulse .ohz-stack-img'); const r=e=>e?Math.round(e.getBoundingClientRect().height):0; return {stack:r(st), img:r(im)};}""")
        print('mobile impulse heights:', dims)
        await m.screenshot(path='shots/impulse-m2.png')
        await b.close()
asyncio.run(main())
