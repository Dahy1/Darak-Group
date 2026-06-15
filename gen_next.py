# Generate Next.js layout, shared components, and one page.jsx per route
# from the extracted content/ files.
import json, pathlib, re

OUT = pathlib.Path('darak-next')
CONT = OUT / 'content'
PAGES = CONT / 'pages'
(OUT / 'app').mkdir(parents=True, exist_ok=True)
(OUT / 'components').mkdir(parents=True, exist_ok=True)
(OUT / 'lib').mkdir(parents=True, exist_ok=True)

def dec(s):  # %3D -> = so versioned asset URLs match the files on disk
    return s.replace('%3D', '=').replace('%3d', '=')

# decode every content file in place
for p in list(CONT.glob('*.html')) + list(PAGES.glob('*.html')):
    p.write_text(dec(p.read_text(encoding='utf-8')), encoding='utf-8')
for p in list(CONT.glob('*.json')) + list(PAGES.glob('*.json')):
    p.write_text(dec(p.read_text(encoding='utf-8')), encoding='utf-8')

routes = json.loads((CONT / 'routes.json').read_text(encoding='utf-8'))

# lib/content.js
(OUT / 'lib' / 'content.js').write_text('''import fs from 'fs';
import path from 'path';
const dir = path.join(process.cwd(), 'content');
export function read(name){ try { return fs.readFileSync(path.join(dir, name), 'utf8'); } catch { return ''; } }
export function readJSON(name){ try { return JSON.parse(read(name) || '[]'); } catch { return []; } }
''', encoding='utf-8')

# components/SiteScripts.jsx
(OUT / 'components' / 'SiteScripts.jsx').write_text('''"use client";
import { useEffect } from "react";
export default function SiteScripts({ scripts, k, kick }) {
  useEffect(() => {
    if (!scripts || !scripts.length) return;
    const key = "__loaded_" + (k || "x");
    if (window[key]) return;
    window[key] = true;
    const JS = ["", "text/javascript", "application/javascript", "module", "text/babel"];
    let cancelled = false;
    (async () => {
      for (const s of scripts) {
        if (cancelled) return;
        if (s.src) {
          await new Promise((res) => {
            const el = document.createElement("script");
            if (s.type) el.type = s.type;
            el.src = s.src; el.async = false; el.onload = res; el.onerror = res;
            document.body.appendChild(el);
          });
        } else if (s.code) {
          const t = (s.type || "").toLowerCase();
          if (JS.indexOf(t) === -1) continue;          // skip JSON-LD / templates / config
          const el = document.createElement("script");
          if (s.type) el.type = s.type;
          el.text = s.code;
          document.body.appendChild(el);
        }
      }
      if (kick && !cancelled) {
        const refresh = () => {
          try { window.ScrollTrigger && window.ScrollTrigger.refresh(); } catch (e) {}
          try { window.dispatchEvent(new Event("resize")); } catch (e) {}
        };
        try { document.dispatchEvent(new Event("oh:preloaded")); } catch (e) {}
        refresh();
        setTimeout(refresh, 400);
        setTimeout(refresh, 1200);
        if (document.readyState === "complete") refresh();
        else window.addEventListener("load", refresh);
      }
    })();
    return () => { cancelled = true; };
  }, []);
  return null;
}
''', encoding='utf-8')

# components/Nav.jsx + Footer.jsx + HeadAssets.jsx
(OUT / 'components' / 'Nav.jsx').write_text('''import { read } from "@/lib/content";
export default function Nav(){
  return <div suppressHydrationWarning dangerouslySetInnerHTML={{ __html: read("_nav.html") }} />;
}
''', encoding='utf-8')
(OUT / 'components' / 'Footer.jsx').write_text('''import { read } from "@/lib/content";
export default function Footer(){
  return <div suppressHydrationWarning dangerouslySetInnerHTML={{ __html: read("_footer.html") }} />;
}
''', encoding='utf-8')
(OUT / 'components' / 'HeadAssets.jsx').write_text('''import { read } from "@/lib/content";
export default function HeadAssets(){
  return <div suppressHydrationWarning style={{ display: "contents" }} dangerouslySetInnerHTML={{ __html: read("_head.html") }} />;
}
''', encoding='utf-8')

# components/PageTransition.jsx — left->right feathered gradient page transition.
# #oh-reveal sweeps off on page load (pure CSS, no-JS fallback, runs at first paint).
# This client component sweeps #oh-cover in to cover the old page before navigating
# (full-reload <a> links). TRANSITION is the single source of truth for timing/look.
(OUT / 'components' / 'PageTransition.jsx').write_text('''"use client";
import { useEffect } from "react";

const TRANSITION = {
  duration: 0.6,                          // seconds per half-sweep
  ease: "cubic-bezier(0.76, 0, 0.24, 1)", // power3.inOut feel
  color: "#0A0A0A",                       // curtain core
  featherVW: 18,                          // soft edge width (vw)
};

export default function PageTransition(){
  useEffect(() => {
    const root = document.documentElement;
    root.style.setProperty("--oht-dur", TRANSITION.duration + "s");
    root.style.setProperty("--oht-ease", TRANSITION.ease);
    root.style.setProperty("--oht-color", TRANSITION.color);
    root.style.setProperty("--oht-feather", TRANSITION.featherVW + "vw");

    const cover = document.getElementById("oh-cover");
    if (!cover) return;
    const reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    let leaving = false;
    function leave(href){
      if (leaving) return; leaving = true;
      if (reduce) { window.location.assign(href); return; }
      cover.classList.add("on");                                  // sweep dark band L->R to cover
      window.setTimeout(() => { window.location.assign(href); }, TRANSITION.duration * 1000);
    }
    function onClick(e){
      if (e.defaultPrevented || e.button !== 0 || e.metaKey || e.ctrlKey || e.shiftKey || e.altKey) return;
      const a = e.target.closest && e.target.closest("a");
      if (!a) return;
      const href = a.getAttribute("href");
      if (!href) return;
      if (a.target && a.target !== "_self") return;
      if (a.hasAttribute("download")) return;
      if (/^(mailto:|tel:|javascript:)/i.test(href) || href.charAt(0) === "#") return;
      let url; try { url = new URL(a.href, window.location.href); } catch (_) { return; }
      if (url.origin !== window.location.origin) return;
      if (url.href === window.location.href) return;
      if (url.pathname === window.location.pathname && url.hash) return; // in-page anchor
      e.preventDefault();
      leave(url.href);
    }
    function onShow(){ leaving = false; cover.classList.remove("on"); } // bfcache restore
    document.addEventListener("click", onClick, true);
    window.addEventListener("pageshow", onShow);
    return () => {
      document.removeEventListener("click", onClick, true);
      window.removeEventListener("pageshow", onShow);
    };
  }, []);
  return null;
}
''', encoding='utf-8')

# app/layout.jsx
(OUT / 'app' / 'layout.jsx').write_text('''import HeadAssets from "@/components/HeadAssets";
import Nav from "@/components/Nav";
import Footer from "@/components/Footer";
import SiteScripts from "@/components/SiteScripts";
import PageTransition from "@/components/PageTransition";
import { readJSON } from "@/lib/content";

export const metadata = { title: "Olivia Harper Homes" };

/* Left -> right feathered gradient page transition. Each layer clips an over-wide
   band so the soft edge sweeps horizontally without adding page scroll. Defaults
   live here; PageTransition mirrors them into the same vars (single source). */
const TRANSITION_CSS = `
:root{--oht-dur:.6s;--oht-ease:cubic-bezier(0.76,0,0.24,1);--oht-color:#0A0A0A;--oht-feather:18vw;}
.oh-tlayer{position:fixed;inset:0;overflow:hidden;pointer-events:none;}
.oh-tlayer .oh-band{position:absolute;top:0;left:0;height:100%;width:calc(100vw + var(--oht-feather));will-change:transform;}
#oh-reveal{z-index:2147483646;}
#oh-reveal .oh-band{
  background:linear-gradient(90deg,rgba(10,10,10,0) 0,var(--oht-color) var(--oht-feather),var(--oht-color) 100%);
  transform:translateX(calc(-1 * var(--oht-feather)));
  animation:ohReveal var(--oht-dur) var(--oht-ease) forwards;
}
@keyframes ohReveal{to{transform:translateX(calc(100vw + var(--oht-feather)));}}
#oh-cover{z-index:2147483647;}
#oh-cover .oh-band{
  background:linear-gradient(90deg,var(--oht-color) 0,var(--oht-color) calc(100% - var(--oht-feather)),rgba(10,10,10,0) 100%);
  transform:translateX(calc(-100vw - var(--oht-feather)));
  transition:transform var(--oht-dur) var(--oht-ease);
}
#oh-cover.on .oh-band{transform:translateX(0);}
@media (prefers-reduced-motion:reduce){
  #oh-reveal .oh-band{animation-duration:1ms;}
  #oh-cover .oh-band{transition:none;}
}
`;

export default function RootLayout({ children }) {
  const scripts = readJSON("_scripts.json");
  return (
    <html lang="en">
      <body>
        <style dangerouslySetInnerHTML={{ __html: TRANSITION_CSS }} />
        <div id="oh-reveal" className="oh-tlayer" aria-hidden="true"><i className="oh-band" /></div>
        <div id="oh-cover" className="oh-tlayer" aria-hidden="true"><i className="oh-band" /></div>
        <HeadAssets />
        <Nav />
        {children}
        <Footer />
        <PageTransition />
        <SiteScripts scripts={scripts} k="global" kick={true} />
      </body>
    </html>
  );
}
''', encoding='utf-8')

# one page.jsx per route
def page_jsx(file):
    return ('''import SiteScripts from "@/components/SiteScripts";
import { read, readJSON } from "@/lib/content";
export const dynamic = "force-static";
export default function Page(){
  const content = read("pages/%s.html");
  const style = read("pages/%s.style.html");
  const scripts = readJSON("pages/%s.scripts.json");
  return (
    <>
      {style ? <div suppressHydrationWarning dangerouslySetInnerHTML={{ __html: style }} /> : null}
      <div suppressHydrationWarning className="oh-page-content" dangerouslySetInnerHTML={{ __html: content }} />
      <SiteScripts scripts={scripts} k="page-%s" />
    </>
  );
}
''' % (file, file, file, file))

for r in routes:
    route = r['route']; file = r['file']
    appdir = OUT / 'app' if route == '' else OUT / 'app' / route
    appdir.mkdir(parents=True, exist_ok=True)
    (appdir / 'page.jsx').write_text(page_jsx(file), encoding='utf-8')

print('generated', len(routes), 'pages + layout + components')
