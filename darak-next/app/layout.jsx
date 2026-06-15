import HeadAssets from "@/components/HeadAssets";
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
