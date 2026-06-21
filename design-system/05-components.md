# Components

Patterns distilled from the live site, rewritten against the tokens. Copy these
as starting points; they already adapt to `.on-dark`. Class names use a neutral
`ds-` prefix here — map them onto the existing `.oh*` classes as you migrate.

---

## Buttons

Three variants. All share a base; pick by emphasis.

```css
.ds-btn {
  display: inline-flex; align-items: center; gap: 10px;
  font-family: var(--font-sans); font-size: 13px; font-weight: var(--fw-semibold);
  letter-spacing: var(--tracking-wide); text-transform: uppercase;
  padding: 16px 28px; border-radius: var(--radius-lg); cursor: pointer;
  border: 1px solid transparent; text-decoration: none;
  transition: background var(--dur-base) var(--ease-signature),
              color var(--dur-base) var(--ease-signature),
              border-color var(--dur-base) var(--ease-signature);
}
/* Primary — solid emerald */
.ds-btn--primary { background: var(--color-primary); color: var(--color-on-primary); }
.ds-btn--primary:hover { background: var(--color-primary-hover); }

/* Secondary — outline */
.ds-btn--outline { background: transparent; color: var(--color-text);
  border-color: var(--color-border-strong); }
.ds-btn--outline:hover { border-color: var(--color-text); }

/* Quiet — text + arrow */
.ds-btn--ghost { padding: 0 0 5px; border-radius: 0; gap: 9px;
  border-bottom: 1px solid var(--color-border-strong); }
.ds-btn--ghost:hover { gap: 14px; border-color: var(--color-text); }
```
Inside `.on-dark`, `--primary` inverts to a light fill with emerald text — no extra
code needed. Icon arrow: a 13–14px SVG `→` that nudges right on hover (`gap` grows).

---

## Links
```css
.ds-link { color: var(--color-link); text-decoration: none;
  transition: color var(--dur-fast) var(--ease-signature); }
.ds-link:hover { color: var(--color-link-hover); }
```
For underline-grow on hover use the `.link-underline` pattern in `04-motion.md`.

---

## Eyebrow / label
```css
.ds-eyebrow { display: inline-flex; align-items: center; gap: 11px;
  font-size: var(--fs-eyebrow); letter-spacing: var(--tracking-eyebrow);
  text-transform: uppercase; color: var(--color-text-muted); }
.ds-eyebrow::before { content: ""; width: 7px; height: 7px; border-radius: var(--radius-round);
  background: var(--color-secondary); }     /* dot → light aqua inside .on-dark */
```
Variants seen on site: leading dot (•), parenthetical index `(01)`, or split
wordmark (`Our` / `News`).

---

## Tag & badge
```css
/* Tag — filter pill / category */
.ds-tag { display: inline-flex; align-items: center; gap: 9px;
  font-size: var(--fs-eyebrow); letter-spacing: var(--tracking-wide); text-transform: uppercase;
  color: var(--color-text-soft); border: 1px solid var(--color-border);
  border-radius: var(--radius-pill); padding: 10px 20px;
  transition: color var(--dur-base) var(--ease-signature),
              background var(--dur-base) var(--ease-signature),
              border-color var(--dur-base) var(--ease-signature); }
.ds-tag.is-active { background: var(--color-primary); border-color: var(--color-primary);
  color: var(--color-on-primary); }

/* Status badge — overlaid on media (e.g. "Coming Soon") */
.ds-badge { font-size: 10.5px; letter-spacing: var(--tracking-wide); text-transform: uppercase;
  padding: 6px 12px; border-radius: var(--radius-pill);
  background: rgba(var(--ink-rgb), .82); color: var(--on-dark);
  -webkit-backdrop-filter: blur(6px); backdrop-filter: blur(6px); }
```
> Overlay badges must clear other overlaid info (place a status badge *below* a
> location label, not on top of it).

---

## Media card (overlay style — News / Journal / Projects)
Image fills the card; a dark gradient anchors the title at the bottom; an optional
square arrow button bottom-right.

```css
.ds-card { position: relative; display: block; overflow: hidden;
  border-radius: var(--radius-md); aspect-ratio: 3/4; color: var(--on-dark);
  text-decoration: none; }
.ds-card img { position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover;
  transition: transform 1.1s var(--ease-signature); }
.ds-card:hover img { transform: scale(1.05); }
.ds-card::after { content: ""; position: absolute; inset: 0; z-index: 1;
  background: linear-gradient(to top, rgba(0,0,0,.9) 0%, rgba(0,0,0,.72) 40%,
              rgba(0,0,0,.34) 72%, rgba(0,0,0,0) 100%); }   /* readable on bright photos */
.ds-card__body { position: absolute; inset: auto 0 0 0; z-index: 2;
  padding: clamp(20px, 2vw, 30px); }
.ds-card__title { font-family: var(--font-display); font-weight: 400;
  font-size: var(--fs-h3); line-height: var(--lh-snug); }
.ds-card__arrow { position: absolute; right: clamp(20px,2vw,30px); bottom: clamp(20px,2vw,30px);
  z-index: 3; width: 45px; height: 45px; border-radius: var(--radius-md);
  display: grid; place-items: center; background: var(--color-on-primary); color: var(--color-primary); }
```

## Content card (light, text below image — alt project/unit style)
```css
.ds-card-light { display: block; text-decoration: none; color: var(--color-text); }
.ds-card-light .media { aspect-ratio: 4/5; border-radius: var(--radius-sm);
  overflow: hidden; background: var(--color-surface-sunk); }
.ds-card-light__title { font-family: var(--font-display); font-size: var(--fs-h3);
  margin-top: var(--space-16); }
.ds-card-light__meta { color: var(--color-text-muted); font-size: var(--fs-caption);
  letter-spacing: .06em; margin-top: var(--space-12); }
```

---

## Navigation
- **Fixed top bar**, transparent over heroes; gains a solid/condensed state on
  scroll (`.is-scrolled`). Logotype left; inline indexed links + Contact + burger
  right (the cluster slides in on scroll via `--ease-nav`).
- **Full-screen overlay menu** on a deep-emerald background (`.on-dark`):
  oversized indexed links (`01–05`), close button, featured link, socials.
- Z-index: bar `--z-nav`, overlay `--z-overlay`.

```css
.ds-nav { position: fixed; inset: 0 0 auto 0; z-index: var(--z-nav);
  display: flex; align-items: center; justify-content: space-between;
  padding: clamp(18px,3vw,28px) var(--gutter); }
.ds-nav__overlay { position: fixed; inset: 0; z-index: var(--z-overlay);
  background: var(--color-dark-bg); }   /* add .on-dark on this element */
```

---

## Forms
```css
.ds-field { display: flex; flex-direction: column; gap: 10px; }
.ds-field label { font-size: 13px; letter-spacing: .04em; color: var(--color-text); }
.ds-field input, .ds-field textarea, .ds-field select {
  width: 100%; font-family: inherit; font-size: 15px; color: var(--color-text);
  background: var(--color-surface); border: 1px solid var(--color-border);
  border-radius: var(--radius-xs); padding: 15px 17px; outline: none;
  transition: border-color var(--dur-fast) var(--ease-signature),
              background var(--dur-fast) var(--ease-signature); }
.ds-field input::placeholder { color: var(--color-text-muted); }
.ds-field input:focus, .ds-field textarea:focus, .ds-field select:focus {
  border-color: var(--color-text); background: var(--color-bg); }
.ds-field--error input { border-color: var(--fn-error); }

.ds-submit { /* extends .ds-btn--primary, full-width */ width: 100%; justify-content: center; }
```
Focus ring for keyboard users (all interactive elements):
```css
:where(a, button, input, select, textarea):focus-visible {
  outline: 2px solid var(--color-focus); outline-offset: 2px; }
```

---

## Marquee
```css
.ds-marquee { overflow: hidden; width: 100%; }
.ds-marquee__track { display: flex; width: max-content; animation: ds-mq 28s linear infinite; }
.ds-marquee__item { flex: 0 0 auto; margin-right: var(--space-16); }   /* uniform → seamless -50% */
@keyframes ds-mq { from { transform: translateX(0); } to { transform: translateX(-50%); } }
@media (prefers-reduced-motion: reduce) { .ds-marquee__track { animation: none; } }
```
Duplicate the items (one real set + one `aria-hidden` clone) so `-50%` wraps
seamlessly.

---

## Section scaffold (putting it together)
```html
<section class="section section--alt">
  <div class="wrap">
    <span class="ds-eyebrow">Our projects</span>
    <h2 class="h2">Built to endure</h2>
    <div class="grid"> … .ds-card … </div>
  </div>
</section>

<section class="on-dark" style="background: var(--color-bg)">
  <div class="wrap"> … inverts automatically … </div>
</section>
```

---

## Component checklist (before shipping a new component)
- [ ] Colors come from semantic tokens only.
- [ ] Works on white **and** inside `.on-dark`.
- [ ] Text meets the contrast rules in `01-color.md`.
- [ ] Uses `--radius-*`, `--space-*`, `--ease-*`, `--dur-*` (no magic numbers).
- [ ] Visible `:focus-visible` ring.
- [ ] Hover/scroll motion respects `prefers-reduced-motion`.
- [ ] Reflows correctly at 820px and 600px.
