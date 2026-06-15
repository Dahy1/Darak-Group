# -*- coding: utf-8 -*-
"""Replace the Vision page with a Journal (blog) — listing page + per-article
pages sharing one article template. Reuses the Vision page's full HTML shell
(head / nav / footer / scripts) and swaps the <main> content."""
import re, glob, shutil, pathlib

U = "/wp-content/uploads/2026/02/"

ARTICLES = [
    dict(slug="building-by-hand", cat="Craft", date="May 28, 2026", read="5 min read",
         title="Why We Build by Hand",
         cover=U+"4489-N-Michigan-Ave_1OAKStudios028-scaled.jpg",
         excerpt="A single in-house team carries every development from groundbreaking to handover — and why that changes the result.",
         dek="A home is only as good as the hands that make it. At Darak Group we keep construction in-house so design intent survives all the way to the last fixture.",
         body=[
            ("p", "Most developers in Egypt hand a project off a dozen times before it is finished. Drawings pass to a main contractor, who passes them to subcontractors, who interpret them on site with no one from the design team in the room. By the time a decision reaches the wall, the reasoning behind it is long gone."),
            ("h2", "One team, one standard"),
            ("p", "We work differently. The people who detail a junction are the people who build it. Structure, envelope, joinery and finish are delivered by a single in-house team held to one exacting standard — so nothing is value-engineered away when no one is looking."),
            ("quote", "A home's worth is not measured by the day it is delivered, but by how it endures."),
            ("p", "That continuity is slow by design. We deliver a limited number of homes each phase because craft does not scale the way a spreadsheet wants it to. What it buys is a residence that still reads as considered in ten years as it did on the day of handover."),
            ("h2", "Where it shows"),
            ("p", "It shows in the places you do not photograph: the way a stone return lines up with a reveal, the silence of a door that was hung twice until it was right, the services laid out as carefully as the kitchen. The details no one asks about are the ones that decide whether a home feels built or merely assembled."),
         ]),
    dict(slug="designing-for-light", cat="Design", date="May 12, 2026", read="4 min read",
         title="Designing for the Egyptian Sun",
         cover=U+"112-West-Palm-Ave_1oakstudios_9.jpg",
         excerpt="Orientation, shading and glass studied room by room — so every home stays cool and luminous from Cairo to the coast.",
         dek="Light is the first material we work with. Long before a finish is chosen, we study how the Egyptian sun will move through every room across the year.",
         body=[
            ("p", "Egyptian light is generous and unforgiving in equal measure. Handled well, it makes a room feel alive; handled carelessly, it bleaches finishes, overheats glass and turns a living room into an oven by midday."),
            ("h2", "Studied room by room"),
            ("p", "We model orientation and shading space by space, not building by building. A morning room wants low eastern sun; a majlis wants none of the harsh afternoon glare. Deep reveals, mashrabiya-inspired screens and tuned glazing keep each home cool without drawing the curtains on its own view."),
            ("quote", "We do not fight the climate. We compose with it."),
            ("p", "The result is a home that changes character through the day rather than holding one fixed mood — bright and open at breakfast, quiet and shaded through the heat, warm at the edges as the desert sun drops."),
         ]),
    dict(slug="materials-that-endure", cat="Materials", date="Apr 30, 2026", read="6 min read",
         title="Choosing Materials That Endure",
         cover=U+"4489-N-Michigan-Ave_1OAKStudios031-scaled.jpg",
         excerpt="From structural glass to hand-finished stone — how we select for Egypt's desert heat and coastal salt, not the day of delivery.",
         dek="The most expensive material is the one you replace in five years. We choose for the long horizon, and detail so the good choices last.",
         body=[
            ("p", "Egyptian homes live a hard life: desert dust and heat inland, salt air and humidity on the North Coast. Materials that look flawless in a showroom can fail quietly within a few seasons. Selecting well means asking not how something looks on day one, but how it will weather a decade of it."),
            ("h2", "What we look for"),
            ("ul", ["Stone and metal that patina gracefully rather than corrode",
                    "Glass and hardware rated for coastal, high-salt environments",
                    "Finishes that shrug off dust, heat and strong sun",
                    "Surfaces that can be maintained, not only replaced"]),
            ("quote", "Durability is a design decision, made long before anything is installed."),
            ("p", "Just as important as the material is the detail around it. A beautiful stone fails at its weakest joint; a fine timber splits where heat was allowed to build. We detail the transitions as carefully as we choose the surfaces, because endurance lives in the junctions."),
         ]),
    dict(slug="inside-a-waterfront-build", cat="Projects", date="Apr 15, 2026", read="7 min read",
         title="Inside a North Coast Build: Almaza Bay",
         cover=U+"1716-S.-Bayshore-Drive2-scaled.jpg",
         excerpt="A look behind the scenes of one of our North Coast developments — from raw sand to beachfront chalet.",
         dek="Building on the Mediterranean rewards patience and punishes shortcuts. Here is how one Almaza Bay development came together, from first survey to handover.",
         body=[
            ("p", "A North Coast site gives you everything — light, breeze, an endless horizon — and asks for everything in return. The sand shifts, the season is short, and the sea is a constant, corrosive presence every building must be made to live alongside."),
            ("h2", "Starting from the water"),
            ("p", "We designed this development outward from the lagoon. The principal rooms open fully to the beach and pool deck, sliding walls of glass retracting so the living space and terrace become one. Services and structure were kept to the rear, quiet and unseen."),
            ("quote", "On the coast, the view is the architecture. Everything else gets out of its way."),
            ("h2", "Detailed for the long term"),
            ("p", "Every exposed fixing is corrosion-grade; the marina walk, decks and beach club are built to the same standard as the chalets. The development was not finished when the photographs were taken — it was finished when we were confident it would still feel this way after a decade of salt and sun."),
         ]),
    dict(slug="what-turnkey-should-mean", cat="Process", date="Mar 27, 2026", read="4 min read",
         title="What “Turnkey” Should Really Mean",
         cover=U+"Florida-Luxury-Real-Estate-Olvia-Harper1-scaled.jpg",
         excerpt="The word gets used loosely across Egypt. For us it means a home that is genuinely finished — and a client who never had to manage the build.",
         dek="Turnkey should mean more than a key in your hand. It should mean a home that is truly complete, delivered by a team that carried the weight so you did not have to.",
         body=[
            ("p", "“Turnkey” has become a marketing word across the Egyptian market. Too often it means the obvious things work and the rest is left for you to discover. We hold it to a higher bar: a home is not turnkey until it is genuinely, quietly finished."),
            ("h2", "Carrying the weight"),
            ("p", "From permits to the final clean, the build is never handed to the client to manage. One team owns the schedule, the trades and the standard — so the only decisions you make are the ones you want to make."),
            ("quote", "You should arrive to a finished home, not a list of things still to chase."),
            ("p", "When we hand over the keys, the home is complete to the last fixture and the last walkthrough. That is the standard our clients return to, trust, and recommend — and the only definition of turnkey we are willing to use."),
         ]),
]

ARR = ('<svg viewBox="0 0 14 14" fill="none" aria-hidden="true"><path d="M2 12L12 2M12 2H5M12 2V9" '
       'stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg>')
BACK = ('<svg viewBox="0 0 16 14" fill="none" aria-hidden="true"><path d="M7 1L1 7l6 6M1 7h14" '
        'stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/></svg>')


# ---------------- listing ----------------
LIST_STYLE = '''<style>
  .ohj{background:#fff;color:#111;font-family:'Helvetica Neue',Arial,sans-serif;
    padding:clamp(120px,17vh,210px) 0 clamp(80px,12vh,150px);}
  .ohj *{box-sizing:border-box;}
  .ohj-wrap{width:100%;max-width:1340px;margin:0 auto;padding:0 clamp(22px,5vw,80px);}
  .ohj-eyebrow{display:inline-flex;align-items:center;gap:11px;font-size:12px;letter-spacing:.22em;
    text-transform:uppercase;color:rgba(17,17,17,.5);}
  .ohj-eyebrow::before{content:'';width:7px;height:7px;border-radius:50%;background:#111;}
  .ohj-title{margin:16px 0 0;font-family:'Gallient',Georgia,serif;font-weight:400;line-height:1;
    letter-spacing:-.02em;font-size:clamp(46px,8vw,118px);}
  .ohj-intro{margin:clamp(22px,3vw,32px) 0 0;max-width:60ch;font-size:clamp(16px,1.3vw,20px);
    line-height:1.6;color:rgba(17,17,17,.62);}

  .ohj-featured{display:grid;grid-template-columns:1.12fr 1fr;gap:clamp(28px,4vw,68px);
    align-items:center;margin-top:clamp(54px,8vh,104px);}
  .ohj-link{text-decoration:none;color:inherit;display:block;}
  .ohj-media{position:relative;overflow:hidden;background:#e9e9e7;border-radius:3px;}
  .ohj-featured .ohj-media{aspect-ratio:4/3;}
  .ohj-media img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;
    filter:grayscale(1) contrast(1.05);transition:transform 1.1s cubic-bezier(.16,1,.3,1);}
  .ohj-link:hover .ohj-media img{transform:scale(1.04);}
  .ohj-tag{font-size:11px;letter-spacing:.18em;text-transform:uppercase;color:rgba(17,17,17,.5);}
  .ohj-ftitle{margin:16px 0 0;font-family:'Gallient',Georgia,serif;font-weight:400;line-height:1.04;
    letter-spacing:-.01em;font-size:clamp(30px,3.6vw,56px);}
  .ohj-fexcerpt{margin:18px 0 0;font-size:clamp(15px,1.2vw,18px);line-height:1.6;color:rgba(17,17,17,.64);max-width:46ch;}
  .ohj-meta{margin-top:18px;font-size:12px;letter-spacing:.06em;color:rgba(17,17,17,.45);}
  .ohj-readmore{display:inline-flex;align-items:center;gap:9px;margin-top:22px;font-size:12px;
    letter-spacing:.14em;text-transform:uppercase;color:#111;border-bottom:1px solid rgba(0,0,0,.3);
    padding-bottom:5px;transition:gap .35s ease,border-color .35s ease;}
  .ohj-readmore svg{width:14px;height:13px;}
  .ohj-link:hover .ohj-readmore{gap:14px;border-color:#111;}

  .ohj-divider{height:1px;background:rgba(0,0,0,.12);margin:clamp(56px,9vh,110px) 0 0;}
  .ohj-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:clamp(30px,3vw,52px) clamp(24px,2.4vw,40px);
    margin-top:clamp(46px,6vh,72px);}
  .ohj-grid .ohj-media{aspect-ratio:3/2;}
  .ohj-card-title{margin:15px 0 0;font-family:'Gallient',Georgia,serif;font-weight:400;line-height:1.1;
    letter-spacing:-.01em;font-size:clamp(21px,1.7vw,27px);}
  .ohj-card-title span{background-image:linear-gradient(#111,#111);background-repeat:no-repeat;
    background-position:0 100%;background-size:0% 1px;padding-bottom:2px;
    transition:background-size .45s cubic-bezier(.16,1,.3,1);}
  .ohj-link:hover .ohj-card-title span{background-size:100% 1px;}
  .ohj-card-excerpt{margin:11px 0 0;font-size:14.5px;line-height:1.55;color:rgba(17,17,17,.6);}
  .ohj-card-meta{margin-top:13px;font-size:11.5px;letter-spacing:.06em;color:rgba(17,17,17,.45);}
  .ohj-card .ohj-tag{display:block;margin-top:16px;}

  @media (max-width:900px){
    .ohj-featured{grid-template-columns:1fr;gap:24px;}
    .ohj-grid{grid-template-columns:1fr 1fr;}
  }
  @media (max-width:560px){ .ohj-grid{grid-template-columns:1fr;} }
</style>'''


def listing_inner():
    feat = ARTICLES[0]
    rest = ARTICLES[1:]
    cards = ""
    for a in rest:
        cards += '''
        <a class="ohj-link ohj-card" href="/blog/%(slug)s/">
          <div class="ohj-media"><img src="%(cover)s" alt="%(title)s" loading="lazy"></div>
          <span class="ohj-tag">%(cat)s</span>
          <h3 class="ohj-card-title"><span>%(title)s</span></h3>
          <p class="ohj-card-excerpt">%(excerpt)s</p>
          <div class="ohj-card-meta">%(date)s &middot; %(read)s</div>
        </a>''' % a
    return '''
<section class="ohj">
%(style)s
  <div class="ohj-wrap">
    <span class="ohj-eyebrow">The Journal</span>
    <h1 class="ohj-title">Notes on<br>building well</h1>
    <p class="ohj-intro">Field notes on craft, design and the long view &mdash; from the team behind Olivia Harper Homes. Fewer, more considered pieces, the way we build.</p>

    <a class="ohj-link ohj-featured" href="/blog/%(fslug)s/">
      <div class="ohj-media"><img src="%(fcover)s" alt="%(ftitle)s" loading="lazy"></div>
      <div class="ohj-fbody">
        <span class="ohj-tag">Featured &middot; %(fcat)s</span>
        <h2 class="ohj-ftitle">%(ftitle)s</h2>
        <p class="ohj-fexcerpt">%(fexcerpt)s</p>
        <div class="ohj-meta">%(fdate)s &middot; %(fread)s</div>
        <span class="ohj-readmore">Read article %(arr)s</span>
      </div>
    </a>

    <div class="ohj-divider"></div>
    <div class="ohj-grid">%(cards)s</div>
  </div>
</section>''' % dict(style=LIST_STYLE, fslug=feat["slug"], fcover=feat["cover"], ftitle=feat["title"],
                     fcat=feat["cat"], fexcerpt=feat["excerpt"], fdate=feat["date"], fread=feat["read"],
                     arr=ARR, cards=cards)


# ---------------- article ----------------
ART_STYLE = '''<style>
  .ohart{background:#fff;color:#111;font-family:'Helvetica Neue',Arial,sans-serif;
    padding:clamp(108px,15vh,180px) 0 clamp(70px,11vh,130px);}
  .ohart *{box-sizing:border-box;}
  .ohart-col{width:100%;max-width:760px;margin:0 auto;padding:0 clamp(22px,5vw,40px);}
  .ohart-wide{width:100%;max-width:1200px;margin:0 auto;padding:0 clamp(22px,5vw,60px);}
  .ohart-back{display:inline-flex;align-items:center;gap:9px;text-decoration:none;color:rgba(17,17,17,.6);
    font-size:12px;letter-spacing:.14em;text-transform:uppercase;transition:gap .35s ease,color .3s ease;}
  .ohart-back svg{width:15px;height:13px;}
  .ohart-back:hover{color:#111;gap:13px;}
  .ohart-meta{margin:clamp(34px,5vh,56px) 0 0;font-size:12px;letter-spacing:.1em;text-transform:uppercase;color:rgba(17,17,17,.5);}
  .ohart-title{margin:18px 0 0;font-family:'Gallient',Georgia,serif;font-weight:400;line-height:1.02;
    letter-spacing:-.02em;font-size:clamp(34px,5.4vw,72px);}
  .ohart-dek{margin:clamp(20px,2.6vw,30px) 0 0;font-size:clamp(18px,1.6vw,24px);line-height:1.5;color:rgba(17,17,17,.7);}
  .ohart-byline{margin:clamp(20px,2.4vw,28px) 0 0;font-size:13px;letter-spacing:.04em;color:rgba(17,17,17,.5);}
  .ohart-cover{margin:clamp(40px,6vh,72px) auto 0;}
  .ohart-cover .ohart-frame{position:relative;aspect-ratio:16/9;overflow:hidden;background:#e9e9e7;border-radius:3px;}
  .ohart-cover img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;filter:grayscale(1) contrast(1.05);}
  .ohart-body{margin:clamp(44px,6vh,76px) auto 0;}
  .ohart-body p{margin:0 0 1.35em;font-size:clamp(16px,1.15vw,19px);line-height:1.78;color:rgba(17,17,17,.82);}
  .ohart-body h2{margin:1.7em 0 .5em;font-family:'Gallient',Georgia,serif;font-weight:400;line-height:1.1;
    letter-spacing:-.01em;font-size:clamp(26px,2.6vw,40px);color:#111;}
  .ohart-body ul{margin:0 0 1.35em;padding-left:0;list-style:none;}
  .ohart-body li{position:relative;padding-left:24px;margin:0 0 .6em;font-size:clamp(16px,1.15vw,19px);
    line-height:1.7;color:rgba(17,17,17,.82);}
  .ohart-body li::before{content:'';position:absolute;left:0;top:.7em;width:8px;height:1px;background:#111;}
  .ohart-quote{margin:1.7em 0;padding-left:26px;border-left:2px solid #111;
    font-family:'Gallient',Georgia,serif;font-weight:400;font-size:clamp(23px,2.6vw,36px);
    line-height:1.22;letter-spacing:-.01em;color:#111;}
  .ohart-end{max-width:760px;margin:clamp(56px,8vh,96px) auto 0;padding:clamp(28px,4vh,44px) clamp(22px,5vw,40px) 0;
    border-top:1px solid rgba(0,0,0,.14);display:flex;justify-content:space-between;align-items:center;gap:20px;flex-wrap:wrap;}
  .ohart-end-by{font-size:13px;letter-spacing:.04em;color:rgba(17,17,17,.55);}
  .ohart-next{display:inline-flex;align-items:center;gap:9px;text-decoration:none;color:#111;font-size:12px;
    letter-spacing:.14em;text-transform:uppercase;border-bottom:1px solid rgba(0,0,0,.3);padding-bottom:5px;
    transition:gap .35s ease,border-color .35s ease;}
  .ohart-next svg{width:14px;height:13px;}
  .ohart-next:hover{gap:14px;border-color:#111;}

  .ohart-more{margin:clamp(64px,9vh,120px) auto 0;}
  .ohart-more-h{font-size:12px;letter-spacing:.2em;text-transform:uppercase;color:rgba(17,17,17,.5);
    padding-bottom:22px;border-bottom:1px solid rgba(0,0,0,.12);}
  .ohart-more-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:clamp(24px,2.4vw,40px);margin-top:clamp(34px,4vh,52px);}
  .ohart-mcard{text-decoration:none;color:inherit;display:block;}
  .ohart-mmedia{position:relative;aspect-ratio:3/2;overflow:hidden;background:#e9e9e7;border-radius:3px;}
  .ohart-mmedia img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;
    filter:grayscale(1) contrast(1.05);transition:transform 1s cubic-bezier(.16,1,.3,1);}
  .ohart-mcard:hover .ohart-mmedia img{transform:scale(1.04);}
  .ohart-mtag{display:block;margin-top:14px;font-size:11px;letter-spacing:.18em;text-transform:uppercase;color:rgba(17,17,17,.5);}
  .ohart-mtitle{margin:9px 0 0;font-family:'Gallient',Georgia,serif;font-weight:400;line-height:1.1;
    font-size:clamp(19px,1.5vw,25px);}
  @media (max-width:760px){ .ohart-more-grid{grid-template-columns:1fr;} }
</style>'''


def render_body(parts):
    out = ""
    for kind, val in parts:
        if kind == "p":
            out += "\n        <p>%s</p>" % val
        elif kind == "h2":
            out += "\n        <h2>%s</h2>" % val
        elif kind == "quote":
            out += '\n        <blockquote class="ohart-quote">%s</blockquote>' % val
        elif kind == "ul":
            lis = "".join("<li>%s</li>" % x for x in val)
            out += "\n        <ul>%s</ul>" % lis
    return out


def article_inner(a, nxt, more):
    more_cards = ""
    for m in more:
        more_cards += '''
        <a class="ohart-mcard" href="/blog/%(slug)s/">
          <div class="ohart-mmedia"><img src="%(cover)s" alt="%(title)s" loading="lazy"></div>
          <span class="ohart-mtag">%(cat)s</span>
          <h3 class="ohart-mtitle">%(title)s</h3>
        </a>''' % m
    return '''
<article class="ohart">
%(style)s
  <div class="ohart-col">
    <a class="ohart-back" href="/blog/">%(back)s The Journal</a>
    <div class="ohart-meta">%(cat)s &nbsp;&middot;&nbsp; %(date)s &nbsp;&middot;&nbsp; %(read)s</div>
    <h1 class="ohart-title">%(title)s</h1>
    <p class="ohart-dek">%(dek)s</p>
    <div class="ohart-byline">Written by Olivia Harper Homes</div>
  </div>

  <div class="ohart-cover ohart-wide"><div class="ohart-frame"><img src="%(cover)s" alt="%(title)s"></div></div>

  <div class="ohart-body ohart-col">%(body)s</div>

  <div class="ohart-end">
    <span class="ohart-end-by">Olivia Harper Homes &middot; The Journal</span>
    <a class="ohart-next" href="/blog/%(nslug)s/">Next: %(ntitle)s %(arr)s</a>
  </div>

  <div class="ohart-more ohart-wide">
    <div class="ohart-more-h">More from the Journal</div>
    <div class="ohart-more-grid">%(more)s</div>
  </div>
</article>''' % dict(style=ART_STYLE, back=BACK, cat=a["cat"], date=a["date"], read=a["read"],
                     title=a["title"], dek=a["dek"], cover=a["cover"], body=render_body(a["body"]),
                     nslug=nxt["slug"], ntitle=nxt["title"], arr=ARR, more=more_cards)


# ---------------- shell + write ----------------
def build_page(shell, main_open, main_close, inner, title):
    page = shell[:main_open] + '<main id="content" class="site-main page type-page status-publish hentry">\n' \
           + inner + '\n</main>' + shell[main_close + len('</main>'):]
    page = re.sub(r'<title>.*?</title>', '<title>%s</title>' % title, page, count=1, flags=re.S)
    return page


def main():
    shell_src = 'site/blog/index.html' if pathlib.Path('site/blog/index.html').exists() else 'site/vision/index.html'
    shell = pathlib.Path(shell_src).read_text(encoding='utf-8')
    mo = shell.find('<main id="content"')
    mo_end = shell.find('>', mo) + 1
    mc = shell.find('</main>', mo_end)
    prefix, suffix = shell[:mo], shell[mc + len('</main>'):]

    def assemble(inner, title):
        return prefix + '<main id="content" class="site-main page type-page status-publish hentry">\n' \
               + inner + '\n</main>' + suffix

    def settitle(html, title):
        return re.sub(r'<title>.*?</title>', '<title>%s</title>' % title, html, count=1, flags=re.S)

    # listing
    pathlib.Path('site/blog').mkdir(parents=True, exist_ok=True)
    listing = settitle(assemble(listing_inner(), 'Journal - Olivia Harper Homes'), 'Journal - Olivia Harper Homes')
    pathlib.Path('site/blog/index.html').write_text(listing, encoding='utf-8')

    # articles
    n = len(ARTICLES)
    for i, a in enumerate(ARTICLES):
        nxt = ARTICLES[(i + 1) % n]
        more = [ARTICLES[(i + 1) % n], ARTICLES[(i + 2) % n], ARTICLES[(i + 3) % n]]
        inner = article_inner(a, nxt, more)
        title = '%s - Journal - Olivia Harper Homes' % a["title"]
        pathlib.Path('site/blog/%s' % a["slug"]).mkdir(parents=True, exist_ok=True)
        pathlib.Path('site/blog/%s/index.html' % a["slug"]).write_text(settitle(assemble(inner, title), title), encoding='utf-8')

    # remove the old Vision page
    if pathlib.Path('site/vision').exists():
        shutil.rmtree('site/vision')

    # update nav + footer links across every static page: /vision/ -> /blog/, "Vision" -> "Journal"
    cnt = 0
    for p in glob.glob('site/**/index.html', recursive=True):
        t = pathlib.Path(p).read_text(encoding='utf-8')
        o = t
        t = t.replace('href="/vision/"', 'href="/blog/"')
        t = t.replace('>Vision</a>', '>Journal</a>')
        t = t.replace('elementor-icon-list-text">Vision</span>', 'elementor-icon-list-text">Journal</span>')
        if t != o:
            pathlib.Path(p).write_text(t, encoding='utf-8')
            cnt += 1
    print('blog listing + %d articles written; vision removed; links updated on %d pages' % (n, cnt))


if __name__ == '__main__':
    main()
