"use client";
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
