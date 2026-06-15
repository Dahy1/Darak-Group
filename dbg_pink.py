import asyncio, threading, functools, http.server, socketserver, os
from playwright.async_api import async_playwright
ROOT=os.path.join(os.getcwd(),'site'); PORT=8808
def serve():
    h=functools.partial(http.server.SimpleHTTPRequestHandler,directory=ROOT)
    socketserver.TCPServer.allow_reuse_address=True
    with socketserver.TCPServer(('127.0.0.1',PORT),h) as s: s.serve_forever()
async def main():
    threading.Thread(target=serve,daemon=True).start(); await asyncio.sleep(1)
    async with async_playwright() as p:
        b=await p.chromium.launch()
        pg=await b.new_page(viewport={'width':1440,'height':900})
        await pg.goto(f'http://127.0.0.1:{PORT}/services/',wait_until='load'); await pg.wait_for_timeout(2500)
        await pg.evaluate("()=>{const p=document.getElementById('ohPreloader');if(p)p.remove();}")
        # find a link, get normal + hover color
        res=await pg.evaluate("""()=>{
          const out=[];
          const links=[...document.querySelectorAll('a')].slice(0,60);
          for(const a of links){const c=getComputedStyle(a).color; out.push(c);}
          // tally
          const tally={}; out.forEach(c=>tally[c]=(tally[c]||0)+1);
          return tally;
        }""")
        print('link colors (normal):', res)
        # hover the first nav link and footer link
        for sel in ['header a','.elementor-button','footer a','.zt-inline a']:
            el=await pg.query_selector(sel)
            if not el: continue
            try:
                await el.hover(); await pg.wait_for_timeout(250)
                info=await pg.evaluate("(s)=>{const e=document.querySelector(s); const cs=getComputedStyle(e); return {sel:s, color:cs.color, bg:cs.backgroundColor, txt:(e.textContent||'').trim().slice(0,24)};}", sel)
                print('HOVER', info)
            except Exception as ex: print('hover err', sel, str(ex)[:60])
        # scan stylesheets for rules mentioning pink-ish colors
        rules=await pg.evaluate("""()=>{
          const hits=[]; const want=/(255, ?0, ?|236, ?72, ?153|233, ?30, ?99|255, ?20, ?147|231, ?84, ?128|#e91e63|#ec4899|#ff1493|pink|magenta|crimson|#d6336c|#e83e8c)/i;
          for(const ss of document.styleSheets){ let rs; try{rs=ss.cssRules}catch(e){continue;} if(!rs)continue;
            for(const r of rs){ const t=r.cssText||''; if(want.test(t)) hits.push((ss.href||'inline').split('/').pop()+' :: '+t.slice(0,160)); }
          }
          return hits.slice(0,30);
        }""")
        print('--- stylesheet rules with pink-ish colors ---')
        for h in rules: print(h)
        await b.close()
asyncio.run(main())
