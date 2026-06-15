import asyncio
from playwright.async_api import async_playwright
BASE='http://localhost:3000'
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch()
        m=await b.new_page(viewport={'width':390,'height':844},device_scale_factor=2,is_mobile=True)
        await m.goto(f'{BASE}/', wait_until='load'); await m.wait_for_timeout(2500)
        await m.evaluate("()=>{const p=document.getElementById('ohPreloader');if(p)p.remove();document.dispatchEvent(new Event('oh:preloaded'));}")
        await m.wait_for_timeout(700)
        await m.evaluate("()=>{const s=document.getElementById('ohzImpulse'); if(s) s.scrollIntoView();}")
        await m.wait_for_timeout(700)
        info=await m.evaluate("""()=>{const im=document.querySelector('#ohzImpulse .ohz-stack-img');
          const inlineH = im.style.height; 
          // which rules set height? walk matched via getMatchedCSSRules not avail; just report
          const before = im.getBoundingClientRect().height;
          im.style.setProperty('height','590px','important');
          const after = im.getBoundingClientRect().height;
          return {inlineStyleHeight: inlineH, rectBefore: Math.round(before), rectAfterForce: Math.round(after), naturalH: im.naturalHeight, naturalW: im.naturalWidth};
        }""")
        print(info)
        await b.close()
asyncio.run(main())
