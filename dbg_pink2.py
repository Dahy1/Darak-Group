import asyncio, threading, functools, http.server, socketserver, os
from playwright.async_api import async_playwright
ROOT=os.path.join(os.getcwd(),'site'); PORT=8809
def serve():
    h=functools.partial(http.server.SimpleHTTPRequestHandler,directory=ROOT)
    socketserver.TCPServer.allow_reuse_address=True
    with socketserver.TCPServer(('127.0.0.1',PORT),h) as s: s.serve_forever()
SCAN="""()=>{
  function parse(c){const m=c&&c.match(/(-?\d+),\s*(-?\d+),\s*(-?\d+)/);return m?[+m[1],+m[2],+m[3]]:null;}
  function saturated(rgb){if(!rgb)return false;const[r,g,b]=rgb;const mx=Math.max(r,g,b),mn=Math.min(r,g,b);return (mx-mn)>40;}
  const hits=[];
  for(const ss of document.styleSheets){let rs;try{rs=ss.cssRules}catch(e){continue;}if(!rs)continue;
    for(const r of rs){const sel=r.selectorText||'';const t=r.cssText||'';
      if(!/:hover|:active|:focus/.test(sel))continue;
      // pull color/background/border-color values
      const props=['color','background-color','border-color','background','fill','stroke'];
      if(r.style){for(const p of props){const v=r.style.getPropertyValue(p);const rgb=parse(v);if(saturated(rgb)){hits.push((ss.href||'inline').split('/').pop()+' | '+sel.slice(0,70)+' | '+p+':'+v.slice(0,40));}
        // also hex
        if(/#[0-9a-f]{3,6}/i.test(v)){const hex=v.match(/#[0-9a-f]{3,6}/i)[0];const h=hex.replace('#','');const f=h.length===3?h.split('').map(x=>x+x).join(''):h;const rr=parseInt(f.slice(0,2),16),gg=parseInt(f.slice(2,4),16),bb=parseInt(f.slice(4,6),16);if(saturated([rr,gg,bb]))hits.push((ss.href||'inline').split('/').pop()+' | '+sel.slice(0,70)+' | '+p+':'+v.slice(0,40));}
      }}
    }}
  return [...new Set(hits)].slice(0,40);
}"""
async def main():
    threading.Thread(target=serve,daemon=True).start(); await asyncio.sleep(1)
    async with async_playwright() as p:
        b=await p.chromium.launch()
        for route in ['/services/','/homes-projects/','/']:
            pg=await b.new_page(viewport={'width':1440,'height':900})
            await pg.goto(f'http://127.0.0.1:{PORT}{route}',wait_until='load'); await pg.wait_for_timeout(2200)
            hits=await pg.evaluate(SCAN)
            print('==== ',route,' saturated hover/active/focus rules ====')
            for h in hits: print('  ',h)
            await pg.close()
        await b.close()
asyncio.run(main())
