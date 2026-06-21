# Motion

Motion at Darak is **slow, smooth, and intentional** — it should feel like things
*settle into place*, never bounce or rush. One signature easing carries most of
the work.

---

## 1 · Easing tokens

| Token | Curve | Use |
|-------|-------|-----|
| `--ease-signature` | `cubic-bezier(.16, 1, .3, 1)` | **default** — reveals, hovers, image scales, most transitions ("expo-out") |
| `--ease-nav` | `cubic-bezier(.22, .61, .36, 1)` | nav cluster slide-in, header state changes |
| `--ease-overshoot` | `cubic-bezier(.34, 1.56, .64, 1)` | a gentle pop for small accents — use *sparingly* |
| `--ease-inout` | `cubic-bezier(.76, 0, .24, 1)` | symmetric moves (clip wipes, full-bleed scales) |

When in doubt, use `--ease-signature`.

## 2 · Duration tokens

| Token | Value | Use |
|-------|-------|-----|
| `--dur-fast` | `0.25s` | hover color/border, small UI |
| `--dur-base` | `0.4s` | buttons, arrows, toggles |
| `--dur-slow` | `0.7s` | card overlays, panel slides |
| `--dur-reveal` | `1.1s` | scroll reveals, image transforms |

---

## 3 · Core patterns

### Reveal on scroll
Elements start translated down + transparent; an `IntersectionObserver` adds
`.is-in`. CSS does the transition.

```css
.reveal { opacity: 0; transform: translateY(26px);
  transition: opacity var(--dur-reveal) var(--ease-signature),
              transform var(--dur-reveal) var(--ease-signature); }
.reveal.is-in { opacity: 1; transform: none; }
```
```js
const io = new IntersectionObserver((es) => {
  es.forEach(e => { if (e.isIntersecting) { e.target.classList.add('is-in'); io.unobserve(e.target); } });
}, { rootMargin: '-8% 0px' });
document.querySelectorAll('.reveal').forEach(el => io.observe(el));
```

### Masked line reveal (headings)
Each line sits in an `overflow:hidden` mask and slides up from `translateY(112%)`.
Stagger with small `transition-delay` per line.

### Hover — link underline grow
```css
.link-underline { background-image: linear-gradient(currentColor, currentColor);
  background-repeat: no-repeat; background-position: 0 100%; background-size: 0% 1px;
  padding-bottom: 2px; transition: background-size var(--dur-base) var(--ease-signature); }
.link-underline:hover { background-size: 100% 1px; }
```

### Hover — image zoom
```css
.media img { transition: transform 1.1s var(--ease-signature); }
.card:hover .media img { transform: scale(1.05); }
```

### Parallax & pinned sequences (desktop only)
GSAP + ScrollTrigger drive vertical drift, full-bleed image scaling, and pinned
step sequences. **Gate all scroll-driven effects to desktop and reduced-motion:**

```js
const canAnimate = window.matchMedia('(min-width:1024px)').matches
  && !window.matchMedia('(prefers-reduced-motion: reduce)').matches;
if (canAnimate) { /* register parallax / pin timelines */ }
```
On mobile/tablet these fall back to static or simple layouts (see
`03-layout-spacing.md`).

### Marquees
Infinite horizontal loops (brand name, statement words, image rows). Two
techniques in use:
- **CSS** — duplicate the content, animate the track `transform: translateX(0)`
  → `translateX(-50%)` with a linear `infinite` keyframe. Use uniform per-item
  `margin-right` (not `gap`) so `-50%` lands seamlessly.
- **JS scroll-reactive** — `requestAnimationFrame` advances `translate3d` x; the
  *direction follows scroll* (down → left, up → right), clamped so it never lurches.

Always duplicate content for a seamless wrap and `aria-hidden` the decorative copy.

---

## 4 · Reduced motion (required)

Every animation must degrade gracefully. The token file already collapses
durations under `prefers-reduced-motion`, but also:

```css
@media (prefers-reduced-motion: reduce) {
  .reveal { opacity: 1 !important; transform: none !important; }
  .marquee-track { animation: none !important; }
}
```
And in JS, bail out of GSAP/RAF loops when `(prefers-reduced-motion: reduce)`
matches. Never trap content in a permanently-hidden reveal state.

---

## 5 · Principles
- **One easing** (`--ease-signature`) unifies the feel; reach for others only for
  their specific job.
- **Slow > snappy.** Reveals ~1.1s, hovers ~0.25–0.4s.
- **Subtle distances.** Reveal offsets ~20–30px, image zoom ≤1.06, parallax drift
  small. Luxury reads as restraint.
- **Decorative motion is `aria-hidden`** and never blocks interaction
  (`pointer-events: none` on marquees/cursors).
