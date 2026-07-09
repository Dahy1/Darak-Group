# -*- coding: utf-8 -*-
"""Replace the Vision page with a Journal (blog) — listing page + per-article
pages sharing one article template. Reuses the Vision page's full HTML shell
(head / nav / footer / scripts) and swaps the <main> content."""
import re, glob, shutil, pathlib

U = "/wp-content/uploads/linkedin/"

ARTICLES = [
    dict(slug="urban-zen-by-azur", cat="Hospitality", date="Jun 12, 2026", read="5 min read",
         title="Urban Zen by Azur: A New Chapter in Hospitality",
         cover=U+"blog-azur.jpg",
         excerpt="Darak Group brings service and leisure into its communities with Urban Zen by Azur — extending its craft from architecture into the way a place is lived.",
         dek="Great communities are not only built — they are hosted. With the launch of Urban Zen by Azur, Darak Group carries its standard beyond the building line and into the daily experience of living.",
         body=[
            ("p", "For most of its history a developer's job ended at handover. The keys changed hands, and whatever happened next — the upkeep, the amenities, the sense of belonging — belonged to someone else. We came to see that as the wrong place to stop."),
            ("p", "Urban Zen by Azur is our answer: a dedicated hospitality identity that takes responsibility for how a Darak community actually feels once people are living in it. It was introduced at a gathering that brought our partners and teams together around a single idea — that the experience of a place deserves the same care as its architecture."),
            ("h2", "From developer to host"),
            ("p", "Through our affiliated hospitality venture, Urban Zen by Azur shapes the parts of a development you cannot draw on a floor plan: the welcome at the gate, the rhythm of the beach club, the quiet competence of a team that keeps everything running. It is the difference between owning an address and being looked after at one."),
            ("quote", "We do not just hand over a home — we host a way of life."),
            ("h2", "Designed around the guest"),
            ("p", "Amenities are planned as hospitality from the first sketch, not added once the towers are sold. Pools, lounges, dining and waterfront leisure are programmed and serviced to a consistent standard across our coastal communities, so a resident and a guest meet the same calm, considered Darak."),
            ("p", "It is early, and we intend to grow it carefully. But the direction is set: the home is the beginning of the relationship with Darak, not the end of it."),
         ]),
    dict(slug="crystal-alamein", cat="Projects", date="May 30, 2026", read="6 min read",
         title="Crystal Alamein: Hospitality-Led Living on the New Alamein Coast",
         cover=U+"li2-hero.jpg",
         excerpt="On the Mediterranean at New Alamein, Crystal Alamein pairs coastal architecture with a hospitality-led way of living — designed, like all our work, to endure.",
         dek="At New Alamein, the sea is the architecture. Crystal Alamein is composed around it — a coastal community where design, leisure and service are conceived as one.",
         body=[
            ("p", "New Alamein has become one of the most ambitious stretches of the Egyptian Mediterranean, and it asks a great deal of anything built there. The light is enormous, the season is generous, and the sea is a constant, beautiful, corrosive presence that every decision has to respect."),
            ("h2", "Built outward from the water"),
            ("p", "Crystal Alamein — delivered through our affiliated company Crystal Global — is designed from the shoreline back. Principal spaces open toward the sea; terraces and pool decks extend the living area into the view; services and structure are kept quiet and to the rear. The coast does the talking."),
            ("quote", "On this coast, the view is the architecture — everything else gets out of its way."),
            ("h2", "A place to be hosted"),
            ("p", "What sets Crystal Alamein apart is that it is hospitality-led: leisure, dining and waterfront amenities are planned and serviced as part of the experience, not bolted on afterwards. It is a place to own, and equally a place to be looked after."),
            ("p", "And because it is a Darak development, it is detailed for the long horizon — corrosion-grade where the salt reaches, finished to the same standard at the beach club as in the residences, made to feel this considered after a decade of sun and sea."),
         ]),
    dict(slug="marina-eye-residence", cat="Projects", date="May 16, 2026", read="5 min read",
         title="Marina Eye Residence: Life on the Lagoon",
         cover=U+"li2-a2.jpg",
         excerpt="At the Marina, Marina Eye Residence frames water from every angle — a calm, lagoon-front address built to the single Darak standard.",
         dek="Some homes have a view of the water. Marina Eye Residence is arranged so the water is never out of sight — a residence composed entirely around the lagoon.",
         body=[
            ("p", "The Marina is one of the North Coast's most established destinations, and waterfront land there is rare and unforgiving. Marina Eye Residence makes the most of it by treating the lagoon not as a backdrop but as the organising idea of the whole building."),
            ("h2", "Framing the water"),
            ("p", "Layouts are turned toward the lagoon so that the view reaches deep into each home. Living spaces open to terraces over the water; glazing is tuned to keep interiors cool and luminous without drawing the curtains on the very thing you came for."),
            ("quote", "A home on the water should never make you choose between light and shade, or comfort and the view."),
            ("h2", "The single standard"),
            ("p", "Like everything we build, Marina Eye Residence is delivered to one exacting standard, by a team that carries the project from groundbreaking to handover. The finishes are chosen for coastal life, the details resolved where the sea is hardest on them, and the home handed over genuinely complete."),
            ("p", "The result is a quiet, considered address where the lagoon is part of the architecture — a place to live by the water, the way the coast was meant to be lived.")
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
    filter:contrast(1.03);transition:transform 1.1s cubic-bezier(.16,1,.3,1);}
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
    <p class="ohj-intro">Field notes on craft, design and the long view &mdash; from the team behind Darak Group. Fewer, more considered pieces, the way we build.</p>

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
  .ohart-cover img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;filter:contrast(1.03);}
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
    filter:contrast(1.03);transition:transform 1s cubic-bezier(.16,1,.3,1);}
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
    <div class="ohart-byline">Written by Darak Group</div>
  </div>

  <div class="ohart-cover ohart-wide"><div class="ohart-frame"><img src="%(cover)s" alt="%(title)s"></div></div>

  <div class="ohart-body ohart-col">%(body)s</div>

  <div class="ohart-end">
    <span class="ohart-end-by">Darak Group &middot; The Journal</span>
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
    listing = settitle(assemble(listing_inner(), 'Journal - Darak Group'), 'Journal - Darak Group')
    pathlib.Path('site/blog/index.html').write_text(listing, encoding='utf-8')

    # articles
    n = len(ARTICLES)
    for i, a in enumerate(ARTICLES):
        nxt = ARTICLES[(i + 1) % n]
        more = [ARTICLES[(i + 1) % n], ARTICLES[(i + 2) % n], ARTICLES[(i + 3) % n]]
        inner = article_inner(a, nxt, more)
        title = '%s - Journal - Darak Group' % a["title"]
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
