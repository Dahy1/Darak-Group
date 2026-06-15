import asyncio
from playwright.async_api import async_playwright
BASE='http://localhost:3000'
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch()
        pg=await b.new_page(viewport={'width':1440,'height':900})
        await pg.goto(BASE+'/about-us/', wait_until='commit')
        await pg.wait_for_timeout(120)
        info=await pg.evaluate("""()=>{
          const layer=document.getElementById('oh-reveal');
          const band=layer&&layer.querySelector('.oh-band');
          const cs=band&&getComputedStyle(band);
          const anims=band&&band.getAnimations?band.getAnimations().map(a=>({name:a.animationName,state:a.playState,t:Math.round(a.currentTime)})):'n/a';
          const dur=getComputedStyle(document.documentElement).getPropertyValue('--oht-dur');
          return {
            layer:!!layer, band:!!band,
            rect: band&&band.getBoundingClientRect(),
            transform: cs&&cs.transform,
            bg: cs&&cs.backgroundImage&&cs.backgroundImage.slice(0,60),
            width: cs&&cs.width, zlayer: layer&&getComputedStyle(layer).zIndex,
            dur, anims
          };
        }""")
        print(info)
        await b.close()
asyncio.run(main())
