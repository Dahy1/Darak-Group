# Layout, Spacing & Foundations

Generous, calm whitespace is part of the luxury feel. Use the scale and the
fluid section tokens rather than ad-hoc pixel values.

---

## 1 · Spacing scale (4px base)

| Token | px | Typical use |
|-------|----|-------------|
| `--space-2` | 2 | hairline nudges |
| `--space-4` | 4 | icon gaps |
| `--space-8` | 8 | tight gaps, chips |
| `--space-12` | 12 | label↔control |
| `--space-16` | 16 | card inner gaps |
| `--space-20` | 20 | small padding |
| `--space-24` | 24 | card padding |
| `--space-32` | 32 | block spacing |
| `--space-40` | 40 | group spacing |
| `--space-56` | 56 | large block gaps |
| `--space-72` | 72 | section sub-rhythm |
| `--space-96` | 96 | section rhythm |

### Fluid layout tokens
| Token | Value | Use |
|-------|-------|-----|
| `--gutter` | `clamp(20px, 5vw, 80px)` | left/right page padding (every wrap) |
| `--section-y` | `clamp(72px, 12vh, 150px)` | standard vertical section padding |
| `--section-y-lg` | `clamp(96px, 16vh, 210px)` | hero / statement sections |
| `--content-gap` | `clamp(28px, 4vw, 68px)` | grid/column gaps |

---

## 2 · Containers

```css
.wrap        { width: 100%; max-width: var(--container);      margin-inline: auto; padding-inline: var(--gutter); }
.wrap--wide  { max-width: var(--container-wide); }   /* 1560px — galleries, project grids */
.wrap--text  { max-width: var(--container-text); }   /* 720px — centered prose */
```

| Token | Value |
|-------|-------|
| `--container` | `1480px` (default) |
| `--container-wide` | `1560px` |
| `--container-text` | `720px` (prose measure) |

A section is: full-bleed background → `.wrap` for content → `--section-y` vertical
padding.

```css
.section   { padding-block: var(--section-y); background: var(--color-bg); }
.section--alt { background: var(--color-surface); }   /* alternating rhythm */
```

---

## 3 · Breakpoints

The site is fluid-first (clamp does most of the work). Use these few breakpoints
only for layout reflows.

| Name | Query | Reflow |
|------|-------|--------|
| Phone | `max-width: 600px` | single column; grids → 1 col |
| Mobile/Tablet | `max-width: 820px` | stacked layouts; **parallax/sticky effects turn off here** |
| Tablet | `max-width: 1023px` | desktop scroll-pinned sequences fall back to static |
| Desktop | `min-width: 1024px` | full pinned / parallax experiences |

> **Convention:** mobile-specific behavior lives in `max-width` blocks; never edit
> the desktop rules to fix a mobile issue, and vice-versa. Scroll-driven GSAP
> effects are gated to `min-width: 1024px` in JS — keep new effects consistent.

---

## 4 · Grid patterns

- **Card grids** (projects, journal): `display: grid; grid-template-columns:
  repeat(3, 1fr); gap: var(--content-gap);` → 2 cols `≤980px` → 1 col `≤600px`.
- **Carousels** (news, leaders on mobile): horizontal `display: flex; overflow-x:
  auto; scroll-snap-type: x mandatory;` with `scrollbar-width: none`.
- **Editorial split** (about story): 12-col grid with asymmetric placement on
  desktop; single column (or marquee) on mobile.

---

## 5 · Radii

| Token | px | Use |
|-------|----|-----|
| `--radius-xs` | 2 | form inputs |
| `--radius-sm` | 3 | media / image frames |
| `--radius-md` | 6 | **default** — cards, buttons, panels |
| `--radius-lg` | 10 | large buttons, finder |
| `--radius-xl` | 14 | feature panels, frosted bars |
| `--radius-pill` | 999 | filter tabs, chips, icon buttons |
| `--radius-round` | 50% | arrow buttons, dots, avatars |

---

## 6 · Elevation

Shadows are subtle; depth comes mostly from layering and frosted glass, not heavy
drop shadows.

| Token | Value | Use |
|-------|-------|-----|
| `--shadow-sm` | `0 5px 15px rgba(0,31,29,.10)` | resting cards |
| `--shadow-md` | `0 16px 44px rgba(0,31,29,.16)` | tooltips, popovers |
| `--shadow-lg` | `0 26px 64px -22px rgba(0,0,0,.55)` | dropdowns, modals |
| `--backdrop-blur` | `16px` | frosted panels (property finder, dropdowns, leader cards) |

Frosted-glass panel:
```css
.glass { background: rgba(255,255,255,.55);
  -webkit-backdrop-filter: blur(var(--backdrop-blur)); backdrop-filter: blur(var(--backdrop-blur));
  border: 1px solid var(--color-border); }
/* inside .on-dark, use rgba(0,31,29,.38) as the tint */
```

---

## 7 · Z-index

| Token | Value | Layer |
|-------|-------|-------|
| `--z-base` | 1 | content |
| `--z-raised` | 3 | section above siblings |
| `--z-sticky` | 40 | sticky captions/headers |
| `--z-nav` | 900 | fixed top nav |
| `--z-overlay` | 1000 | full-screen menu / modal |
| `--z-cursor` | 99990 | custom cursor |

Never invent z-index values outside this scale.
