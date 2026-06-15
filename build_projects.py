# -*- coding: utf-8 -*-
"""Replace the homepage 'Our Projects' JetEngine grid (and the projects-page
listing) with a bespoke, tabbed project showcase inspired by tatweermisr.com,
using Olivia Harper Homes' own projects, copy and imagery (grayscale to match)."""
import re

U = "/wp-content/uploads/2026/02/"

PROJECTS = [
    dict(name="The Address New Cairo", loc="New Cairo", region="newcairo",
         img=U+"1716-S.-Bayshore-Drive2-scaled.jpg", url="/projects/1716-s-bayshore-drive/",
         tag="Modern living in the heart of New Cairo",
         facilities=["Crystal Lagoons", "Clubhouse", "Sports Club", "Commercial Strip"],
         props=[("Land Area", "85 feddans"), ("Delivery", "2027"),
                ("Unit Sizes", "135 – 320 m²"), ("Type", "Apartments & Villas")]),
    dict(name="Zayed Dunes", loc="Sheikh Zayed", region="zayed",
         img=U+"1710-S.-Bayshore-Drive1-scaled.jpg", url="/projects/1710-s-bayshore-drive/",
         tag="Serene standalone living in Sheikh Zayed",
         facilities=["Central Park", "Clubhouse", "Retail Avenue", "Jogging Tracks"],
         props=[("Land Area", "60 feddans"), ("Delivery", "2026"),
                ("Unit Sizes", "200 – 450 m²"), ("Type", "Twin Houses & Villas")]),
    dict(name="Marsa Sahel Residences", loc="North Coast", region="coast",
         img=U+"112-West-Palm-Ave_1oakstudios_12.jpg", url="/projects/hibiscus-island-estate/",
         tag="Lagoon-front living on the North Coast",
         facilities=["Private Beach", "Crystal Lagoons", "Marina", "Beach Club"],
         props=[("Land Area", "120 feddans"), ("Delivery", "2028"),
                ("Unit Sizes", "90 – 300 m²"), ("Type", "Chalets & Cabins")]),
    dict(name="Capital Heights", loc="New Capital", region="capital",
         img=U+"Florida-Luxury-Real-Estate3-scaled.jpg", url="/projects/1000-89-st-surfside/",
         tag="Skyline residences in the New Capital",
         facilities=["Sky Lounge", "Business Hub", "Central Park", "Smart Homes"],
         props=[("Land Area", "40 feddans"), ("Delivery", "2027"),
                ("Unit Sizes", "110 – 260 m²"), ("Type", "Apartments")]),
    dict(name="Katameya Greens", loc="New Cairo", region="newcairo",
         img=U+"4489-N-Michigan-Ave_1OAKStudios040-scaled.jpg", url="/projects/miami-beach-residence/",
         tag="Golf-side villas in New Cairo",
         facilities=["Golf Views", "Clubhouse", "Wellness Spa", "Kids' Area"],
         props=[("Land Area", "70 feddans"), ("Delivery", "2025"),
                ("Unit Sizes", "250 – 600 m²"), ("Type", "Standalone Villas")]),
    dict(name="Almaza Bay Chalets", loc="North Coast", region="coast",
         img=U+"Normandy-Shores_02_Staircase_011.png", url="/projects/normandy-shores/",
         tag="Beachfront chalets at Almaza Bay",
         facilities=["Private Beach", "Lagoon", "Marina Walk", "Beach Bar"],
         props=[("Land Area", "95 feddans"), ("Delivery", "2026"),
                ("Unit Sizes", "80 – 180 m²"), ("Type", "Chalets")]),
]

FILTERS = [("all", "All"), ("newcairo", "New Cairo"), ("zayed", "Sheikh Zayed"),
           ("coast", "North Coast"), ("capital", "New Capital")]

PIN = ('<svg class="ohpr-pin" viewBox="0 0 24 24" fill="none" aria-hidden="true">'
       '<path d="M12 21s6.5-5.8 6.5-10.5a6.5 6.5 0 1 0-13 0C5.5 15.2 12 21 12 21z" '
       'stroke="currentColor" stroke-width="1.5"/>'
       '<circle cx="12" cy="10.5" r="2.2" stroke="currentColor" stroke-width="1.5"/></svg>')
ARR = ('<svg viewBox="0 0 14 14" fill="none" aria-hidden="true">'
       '<path d="M2 12L12 2M12 2H5M12 2V9" stroke="currentColor" stroke-width="1.5" '
       'stroke-linecap="round" stroke-linejoin="round"/></svg>')
NAV = ('<svg viewBox="0 0 16 14" fill="none" aria-hidden="true">'
       '<path d="M9 1l6 6-6 6M15 7H1" stroke="currentColor" stroke-width="1.6" '
       'stroke-linecap="round" stroke-linejoin="round"/></svg>')


def card_html(p, i):
    idx = "%02d" % (i + 1)
    fac = "".join('<span class="ohpr-chip">%s</span>' % f for f in p["facilities"])
    props = "".join(
        '<div class="ohpr-prop"><span class="ohpr-prop-k">%s</span>'
        '<span class="ohpr-prop-v">%s</span></div>' % (k, v) for k, v in p["props"])
    return ('''
      <article class="ohpr-card" data-region="%(region)s">
        <div class="ohpr-card-media">
          <img class="ohpr-card-img" src="%(img)s" alt="%(name)s" loading="lazy">
          <div class="ohpr-card-grad"></div>
          <div class="ohpr-card-top">
            <span class="ohpr-card-loc">%(pin)s %(loc)s</span>
            <span class="ohpr-card-idx">%(idx)s</span>
          </div>
          <div class="ohpr-card-info">
            <h3 class="ohpr-card-name">%(name)s</h3>
            <p class="ohpr-card-tag">%(tag)s</p>
            <div class="ohpr-card-actions">
              <button type="button" class="ohpr-preview" data-ohpr-open>Preview</button>
            </div>
          </div>
          <div class="ohpr-card-detail" data-ohpr-detail>
            <button type="button" class="ohpr-detail-close" data-ohpr-close aria-label="Close">
              <svg viewBox="0 0 13 13" fill="none"><path d="M1 1l11 11M12 1L1 12" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg>
            </button>
            <div class="ohpr-chips">%(fac)s</div>
            <h3 class="ohpr-detail-name">%(name)s</h3>
            <p class="ohpr-detail-tag">%(tag)s</p>
            <div class="ohpr-detail-border"></div>
            <div class="ohpr-props">%(props)s</div>
            <a class="ohpr-detail-cta" href="%(url)s">View project %(arr)s</a>
          </div>
        </div>
      </article>''' % dict(region=p["region"], img=p["img"], name=p["name"], pin=PIN,
                           loc=p["loc"], idx=idx, tag=p["tag"], url=p["url"], arr=ARR,
                           fac=fac, props=props))


def section_html(with_header=True, mode='carousel'):
    grid = (mode == 'grid')
    tabs = "".join(
        '<button type="button" class="ohpr-tab%s" data-filter="%s">'
        '<span class="ohpr-tab-dot"></span><span>%s</span></button>'
        % (" is-active" if k == "all" else "", k, label) for k, label in FILTERS)
    cards = "".join(card_html(p, i) for i, p in enumerate(PROJECTS))
    all_link = '' if grid else '<a class="ohpr-all" href="/homes-projects/">See all projects %(nav)s</a>' % dict(nav=NAV)
    header = ('''
    <div class="ohpr-head">
      <div class="ohpr-headtop">
        <div>
          <span class="ohpr-eyebrow"><span class="ohpr-eyebrow-dot"></span>Darak Group Developments</span>
          <h2 class="ohpr-title">Our Projects</h2>
        </div>
        %(all)s
      </div>
      <nav class="ohpr-tabs" aria-label="Filter projects">%(tabs)s</nav>
    </div>''' % dict(all=all_link, tabs=tabs)) if with_header else ('''
    <div class="ohpr-head ohpr-head--bare">
      <nav class="ohpr-tabs" aria-label="Filter projects">%(tabs)s</nav>
    </div>''' % dict(tabs=tabs))

    return '''
<section class="ohpr%(cls)s" id="ohProjects">
%(style)s''' % dict(cls=(' ohpr--grid' if grid else ''), style=STYLE) + '''
  <div class="ohpr-wrap">%(header)s
    <div class="ohpr-progress" aria-hidden="true"><span class="ohpr-prog-fill" data-ohpr-prog></span></div>
    <div class="ohpr-viewport" data-ohpr-viewport>
      <div class="ohpr-track" data-ohpr-track>%(cards)s</div>
    </div>
    <div class="ohpr-controls">
      <div class="ohpr-count"><span data-ohpr-cur>01</span><span class="ohpr-count-sep">/</span><span data-ohpr-total>06</span></div>
      <div class="ohpr-arrows">
        <button type="button" class="ohpr-arrow" data-ohpr-prev aria-label="Previous">%(nav)s</button>
        <button type="button" class="ohpr-arrow" data-ohpr-next aria-label="Next">%(nav)s</button>
      </div>
    </div>
  </div>
%(script)s
</section>''' % dict(style=STYLE, header=header, cards=cards, nav=NAV, script=SCRIPT)


STYLE = '''<style>
  .ohpr{position:relative;background:#ffffff;color:#111111;z-index:3;overflow:hidden;
    font-family:'Helvetica Neue',Arial,sans-serif;padding:clamp(72px,12vh,150px) 0 clamp(72px,12vh,150px);}
  .ohpr *{box-sizing:border-box;}
  .ohpr-wrap{width:100%;max-width:1560px;margin:0 auto;padding:0 clamp(22px,5vw,80px);}

  /* head */
  .ohpr-headtop{display:flex;justify-content:space-between;align-items:flex-end;gap:24px;flex-wrap:wrap;}
  .ohpr-eyebrow{display:inline-flex;align-items:center;gap:11px;font-size:12px;letter-spacing:.22em;
    text-transform:uppercase;color:rgba(17,17,17,.5);}
  .ohpr-eyebrow-dot{width:7px;height:7px;border-radius:50%;background:#111;flex:0 0 auto;}
  .ohpr-title{margin:14px 0 0;font-family:'Gallient',Georgia,serif;font-weight:400;line-height:1;
    letter-spacing:-.02em;font-size:clamp(40px,6vw,92px);}
  .ohpr-all{display:inline-flex;align-items:center;gap:10px;text-decoration:none;color:#111;
    font-size:12px;letter-spacing:.16em;text-transform:uppercase;padding-bottom:6px;
    border-bottom:1px solid rgba(0,0,0,.25);transition:gap .35s ease,border-color .35s ease;}
  .ohpr-all svg{width:16px;height:14px;}
  .ohpr-all:hover{gap:16px;border-color:#111;}

  /* tabs */
  .ohpr-tabs{display:flex;flex-wrap:wrap;gap:10px;margin-top:clamp(28px,4vw,48px);}
  .ohpr-head--bare .ohpr-tabs{margin-top:0;}
  .ohpr-tab{display:inline-flex;align-items:center;gap:9px;cursor:pointer;
    border:1px solid rgba(0,0,0,.16);border-radius:999px;background:transparent;
    padding:10px 20px;font:inherit;font-size:12px;letter-spacing:.14em;text-transform:uppercase;
    color:rgba(17,17,17,.6);transition:color .4s ease,border-color .4s ease,background .4s ease;}
  .ohpr-tab-dot{width:6px;height:6px;border-radius:50%;background:currentColor;opacity:0;
    transform:scale(.4);transition:opacity .4s ease,transform .4s ease;}
  .ohpr-tab:hover{color:#111;border-color:rgba(0,0,0,.4);}
  .ohpr-tab.is-active{background:#111;border-color:#111;color:#fff;}
  .ohpr-tab.is-active .ohpr-tab-dot{opacity:1;transform:scale(1);}

  /* progress */
  .ohpr-progress{position:relative;height:1px;background:rgba(0,0,0,.12);margin:clamp(34px,5vw,56px) 0 clamp(28px,3vw,40px);}
  .ohpr-prog-fill{position:absolute;left:0;top:-0.5px;height:2px;background:#111;width:0;transition:width .15s linear;}

  /* slider */
  .ohpr-viewport{overflow-x:auto;overflow-y:hidden;scroll-snap-type:x mandatory;
    -ms-overflow-style:none;scrollbar-width:none;scroll-behavior:smooth;}
  .ohpr-viewport::-webkit-scrollbar{display:none;}
  .ohpr-track{display:flex;gap:clamp(18px,2vw,30px);width:max-content;}
  .ohpr-card{flex:0 0 auto;width:clamp(280px,38vw,430px);scroll-snap-align:start;}
  .ohpr-card.is-hidden{display:none;}

  .ohpr-card-media{position:relative;aspect-ratio:4/5;overflow:hidden;background:#e9e9e7;border-radius:3px;}
  .ohpr-card-img{position:absolute!important;inset:0;width:100%!important;height:100%!important;
    max-width:none!important;object-fit:cover;transition:transform 1.1s cubic-bezier(.16,1,.3,1);}
  .ohpr-card:hover .ohpr-card-img{transform:scale(1.05);}
  .ohpr-card-grad{position:absolute;inset:0;pointer-events:none;
    background:linear-gradient(180deg,rgba(8,8,8,.34) 0%,rgba(8,8,8,0) 26%,rgba(8,8,8,0) 50%,rgba(8,8,8,.78) 100%);}
  .ohpr-card-top{position:absolute;top:0;left:0;right:0;z-index:2;display:flex;justify-content:space-between;
    align-items:center;padding:clamp(16px,1.6vw,24px);color:#fff;}
  .ohpr-card-loc{display:inline-flex;align-items:center;gap:7px;font-size:11px;letter-spacing:.16em;
    text-transform:uppercase;}
  .ohpr-pin{width:14px;height:14px;flex:0 0 auto;}
  .ohpr-card-idx{font-size:11px;letter-spacing:.16em;color:rgba(255,255,255,.7);}
  .ohpr-card-info{position:absolute;left:0;right:0;bottom:0;z-index:2;padding:clamp(18px,1.8vw,30px);color:#fff;}
  .ohpr-card-name{margin:0;font-family:'Gallient',Georgia,serif;font-weight:400;line-height:1.04;
    letter-spacing:-.01em;font-size:clamp(23px,2.1vw,34px);}
  .ohpr-card-tag{margin:9px 0 0;font-size:13.5px;line-height:1.45;color:rgba(255,255,255,.82);}
  .ohpr-card-actions{display:flex;align-items:center;gap:18px;margin-top:clamp(16px,1.6vw,22px);}
  .ohpr-learn{display:inline-flex;align-items:center;gap:8px;color:#fff;text-decoration:none;
    font-size:12px;letter-spacing:.12em;text-transform:uppercase;padding-bottom:4px;
    border-bottom:1px solid rgba(255,255,255,.45);transition:gap .35s ease,border-color .35s ease;}
  .ohpr-learn svg{width:13px;height:13px;}
  .ohpr-learn:hover{gap:13px;border-color:#fff;}
  .ohpr-preview{cursor:pointer;background:transparent;border:1px solid rgba(255,255,255,.5);
    color:#fff;border-radius:999px;padding:9px 16px;font:inherit;font-size:11px;letter-spacing:.12em;
    text-transform:uppercase;transition:background .35s ease,color .35s ease,border-color .35s ease;}
  .ohpr-preview:hover{background:#fff;color:#111;border-color:#fff;}

  /* expandable detail panel */
  .ohpr-card-detail{position:absolute;inset:0;z-index:3;background:#111111;color:#fff;
    padding:clamp(22px,2vw,38px);display:flex;flex-direction:column;
    transform:translateY(101%);transition:transform .7s cubic-bezier(.16,1,.3,1);}
  .ohpr-card.is-open .ohpr-card-detail{transform:translateY(0);}
  .ohpr-detail-close{position:absolute;top:clamp(16px,1.4vw,22px);right:clamp(16px,1.4vw,22px);
    width:34px;height:34px;border-radius:50%;border:1px solid rgba(255,255,255,.3);background:transparent;
    color:#fff;cursor:pointer;display:inline-flex;align-items:center;justify-content:center;transition:.35s;}
  .ohpr-detail-close svg{width:12px;height:12px;}
  .ohpr-detail-close:hover{background:#fff;color:#111;border-color:#fff;}
  .ohpr-chips{display:flex;flex-wrap:wrap;gap:8px;margin-top:8px;}
  .ohpr-chip{font-size:10.5px;letter-spacing:.1em;text-transform:uppercase;color:rgba(255,255,255,.74);
    border:1px solid rgba(255,255,255,.22);border-radius:999px;padding:6px 12px;}
  .ohpr-detail-name{margin:auto 0 0;font-family:'Gallient',Georgia,serif;font-weight:400;line-height:1.02;
    letter-spacing:-.01em;font-size:clamp(24px,2.2vw,38px);}
  .ohpr-detail-tag{margin:10px 0 0;font-size:13px;letter-spacing:.04em;text-transform:uppercase;color:rgba(255,255,255,.6);}
  .ohpr-detail-border{height:1px;background:rgba(255,255,255,.16);margin:clamp(16px,1.6vw,22px) 0;}
  .ohpr-props{display:grid;grid-template-columns:1fr 1fr;gap:14px clamp(16px,2vw,30px);}
  .ohpr-prop{display:flex;flex-direction:column;gap:4px;}
  .ohpr-prop-k{font-size:10.5px;letter-spacing:.14em;text-transform:uppercase;color:rgba(255,255,255,.5);}
  .ohpr-prop-v{font-size:15px;color:#fff;}
  .ohpr-detail-cta{display:inline-flex;align-items:center;gap:9px;margin-top:clamp(18px,2vw,26px);
    align-self:flex-start;color:#fff;text-decoration:none;font-size:12px;letter-spacing:.14em;
    text-transform:uppercase;border-bottom:1px solid rgba(255,255,255,.4);padding-bottom:5px;
    transition:gap .35s ease,border-color .35s ease;}
  .ohpr-detail-cta svg{width:14px;height:13px;}
  .ohpr-detail-cta:hover{gap:14px;border-color:#fff;}

  /* controls */
  .ohpr-controls{display:flex;justify-content:space-between;align-items:center;
    margin-top:clamp(28px,3.4vw,44px);}
  .ohpr-count{font-size:13px;letter-spacing:.18em;color:rgba(17,17,17,.5);}
  .ohpr-count [data-ohpr-cur]{color:#111;}
  .ohpr-count-sep{margin:0 9px;color:rgba(17,17,17,.3);}
  .ohpr-arrows{display:flex;gap:12px;}
  .ohpr-arrow{width:52px;height:52px;border-radius:50%;border:1px solid rgba(0,0,0,.2);
    background:transparent;color:#111;cursor:pointer;display:inline-flex;align-items:center;justify-content:center;
    transition:background .35s ease,color .35s ease,border-color .35s ease,opacity .3s ease;}
  .ohpr-arrow svg{width:17px;height:15px;}
  .ohpr-arrow[data-ohpr-prev] svg{transform:scaleX(-1);}
  .ohpr-arrow:hover{background:#111;color:#fff;border-color:#111;}
  .ohpr-arrow[disabled]{opacity:.3;cursor:default;pointer-events:none;}

  /* grid mode (projects page): no carousel, cards wrap in a grid */
  .ohpr--grid .ohpr-progress,.ohpr--grid .ohpr-controls{display:none;}
  .ohpr--grid .ohpr-viewport{overflow:visible;margin-top:clamp(36px,5vw,60px);}
  .ohpr--grid .ohpr-track{display:grid;grid-template-columns:repeat(3,1fr);
    gap:clamp(22px,2.4vw,42px);width:auto;}
  .ohpr--grid .ohpr-card{width:auto;}

  @media (max-width:980px){ .ohpr--grid .ohpr-track{grid-template-columns:1fr 1fr;} }
  @media (max-width:820px){
    .ohpr-headtop{align-items:flex-start;}
    .ohpr-all{display:none;}
    .ohpr-card{width:clamp(250px,80vw,330px);}
  }
  @media (max-width:600px){ .ohpr--grid .ohpr-track{grid-template-columns:1fr;} .ohpr--grid .ohpr-card{width:auto;} }
</style>'''

SCRIPT = '''<script>
(function(){
  if (window.__ohprInit) return; window.__ohprInit = true;
  function boot(){
    var sec = document.getElementById('ohProjects');
    if (!sec || sec.__booted) return; sec.__booted = true;
    var grid = sec.classList.contains('ohpr--grid');
    var vp = sec.querySelector('[data-ohpr-viewport]');
    var track = sec.querySelector('[data-ohpr-track]');
    var cards = Array.prototype.slice.call(track.querySelectorAll('.ohpr-card'));
    var prog = sec.querySelector('[data-ohpr-prog]');
    var curEl = sec.querySelector('[data-ohpr-cur]');
    var totEl = sec.querySelector('[data-ohpr-total]');
    var prev = sec.querySelector('[data-ohpr-prev]');
    var next = sec.querySelector('[data-ohpr-next]');
    var tabs = Array.prototype.slice.call(sec.querySelectorAll('.ohpr-tab'));

    function pad(n){ return (n<10?'0':'')+n; }
    function step(){
      var c = cards.find(function(x){ return !x.classList.contains('is-hidden'); });
      if (!c) return 1;
      var gap = parseFloat(getComputedStyle(track).columnGap || getComputedStyle(track).gap || 0) || 0;
      return c.getBoundingClientRect().width + gap;
    }
    function visible(){ return cards.filter(function(x){ return !x.classList.contains('is-hidden'); }); }

    function update(){
      if (grid) return;
      var max = vp.scrollWidth - vp.clientWidth;
      var p = max > 2 ? vp.scrollLeft / max : 0;
      prog.style.width = Math.max(0, Math.min(1, p)) * 100 + '%';
      var tot = visible().length;
      var idx = Math.round(vp.scrollLeft / step()) + 1;
      idx = Math.max(1, Math.min(tot, idx));
      curEl.textContent = pad(idx); totEl.textContent = pad(tot);
      var atStart = vp.scrollLeft <= 2, atEnd = vp.scrollLeft >= max - 2 || max <= 2;
      prev.disabled = atStart; next.disabled = atEnd;
    }
    function go(dir){ vp.scrollBy({ left: dir * step(), behavior: 'smooth' }); }

    if (!grid){
      prev.addEventListener('click', function(){ go(-1); });
      next.addEventListener('click', function(){ go(1); });
      vp.addEventListener('scroll', function(){ window.requestAnimationFrame(update); });
      window.addEventListener('resize', update);
    }

    tabs.forEach(function(t){
      t.addEventListener('click', function(){
        tabs.forEach(function(x){ x.classList.remove('is-active'); });
        t.classList.add('is-active');
        var f = t.getAttribute('data-filter');
        cards.forEach(function(c){
          var show = (f === 'all') || (c.getAttribute('data-region') === f);
          c.classList.toggle('is-hidden', !show);
          if (!show) c.classList.remove('is-open');
        });
        vp.scrollTo({ left: 0, behavior: 'auto' });
        update();
      });
    });

    /* expandable quick-preview */
    cards.forEach(function(c){
      var openBtn = c.querySelector('[data-ohpr-open]');
      var closeBtn = c.querySelector('[data-ohpr-close]');
      if (openBtn) openBtn.addEventListener('click', function(e){ e.preventDefault(); c.classList.add('is-open'); });
      if (closeBtn) closeBtn.addEventListener('click', function(e){ e.preventDefault(); c.classList.remove('is-open'); });
    });

    update();
    if (document.fonts && document.fonts.ready) document.fonts.ready.then(update);
    setTimeout(update, 500);
  }
  if (document.readyState !== 'loading') boot();
  else document.addEventListener('DOMContentLoaded', boot);
  document.addEventListener('oh:preloaded', boot);
})();
</script>'''


def _replace_existing(html, new_section):
    """If an ohpr section already exists, replace it in place. Returns (html, done)."""
    s = html.find('<section class="ohpr')
    if s == -1:
        return html, False
    e = html.find('</section>', s)
    if e == -1:
        return html, False
    e += len('</section>')
    return html[:s] + new_section + html[e:], True


def splice_homepage(path):
    with open(path, encoding='utf-8') as f:
        html = f.read()
    new = section_html(True, mode='carousel').strip()
    html2, done = _replace_existing(html, new)
    if done:
        html = html2
    else:
        a = html.find('<div class="elementor-element elementor-element-f30738b')
        b = html.find('<div class="elementor-element elementor-element-4d79822')
        if a == -1 or b == -1:
            print('homepage markers not found'); return
        html = html[:a] + new + '\n\n\t\t' + html[b:]
    with open(path, 'w', encoding='utf-8') as f:
        f.write(html)
    print('homepage spliced (carousel)')


def splice_projects(path):
    with open(path, encoding='utf-8') as f:
        html = f.read()
    new = section_html(True, mode='grid').strip()
    html2, done = _replace_existing(html, new)
    if done:
        html = html2
    else:
        m = re.search(r'<main id="content"[^>]*>.*?</main>', html, re.S)
        if not m:
            print('projects <main> not found'); return
        inner = '\n<div class="page-content">\n' + new + '\n</div>\n'
        new_main = '<main id="content" class="site-main post-37 page type-page status-publish hentry">' + inner + '</main>'
        html = html[:m.start()] + new_main + html[m.end():]
    with open(path, 'w', encoding='utf-8') as f:
        f.write(html)
    print('projects page spliced (grid)')


if __name__ == '__main__':
    splice_homepage('site/index.html')
    splice_projects('site/homes-projects/index.html')
