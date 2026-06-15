"use client";
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
