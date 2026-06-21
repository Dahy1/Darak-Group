# Darak Group — Design System

A single, coherent visual language for the Darak Group website. This is the
reference any developer or designer should read before building or editing a
page, so that every screen looks like it belongs to the same brand.

> Inspired by the depth and rarity of emerald stones, Darak's identity is
> **premium, calm, and quietly luxurious**. Deep emerald tones express *trust*
> and *exclusivity*; the lighter aqua reflections bring *softness, care, and
> hospitality*. White is the canvas that lets both breathe.

---

## The four principles

1. **White-dominant.** White (`#ffffff`) is the default canvas for ~80% of every
   page. Emerald is used with intent — as ink, as accents, and for full dark
   "moment" sections — never as wallpaper. Restraint *is* the luxury.
2. **Emerald with hierarchy.** Deep emerald (`#002D2B` / `#001F1D`) carries
   weight and trust (text, primary actions, dark sections). Mid teal (`#407B78`)
   is the working accent (links, secondary UI). Light aqua (`#69C9C4`) is a
   highlight and the accent voice *on dark* — it is never small text on white.
3. **Serif headlines, sans body.** Oversized **Gallient** serif headlines against
   quiet **Helvetica Neue** body text. Generous whitespace and a fluid type scale.
4. **Slow, intentional motion.** One signature easing (`cubic-bezier(.16,1,.3,1)`),
   reveal-on-scroll, gentle parallax and marquees. Motion is calm, never busy, and
   always respects `prefers-reduced-motion`.

---

## How to use this system

1. Link the tokens once, globally, before any other CSS:

   ```html
   <link rel="stylesheet" href="/design-system/tokens.css">
   ```

2. In component CSS, **only** reference semantic tokens — never raw hex:

   ```css
   /* ✅ do this */
   .card { background: var(--color-bg); color: var(--color-text);
           border: 1px solid var(--color-border); border-radius: var(--radius-md); }

   /* ❌ never this */
   .card { background: #fff; color: #111; border: 1px solid #e2e2e2; }
   ```

3. For a section on a deep-emerald background, wrap it in `.on-dark`. Every
   semantic token flips automatically; child components need no changes:

   ```html
   <section class="on-dark" style="background: var(--color-bg)"> … </section>
   ```

4. Animate with the motion tokens (`--ease-signature`, `--dur-*`) so timing is
   consistent everywhere.

---

## Files

| File | What's inside |
|------|---------------|
| [`tokens.css`](./tokens.css) | **The source of truth.** All CSS custom properties (color, type, spacing, radii, elevation, motion, z-index). |
| [`01-color.md`](./01-color.md) | Palette, semantic roles, the `.on-dark` scope, pairings, accessibility/contrast. |
| [`02-typography.md`](./02-typography.md) | Fonts, fluid type scale, headings, eyebrows, prose. |
| [`03-layout-spacing.md`](./03-layout-spacing.md) | Spacing scale, containers, grid, breakpoints, radii, elevation, z-index. |
| [`04-motion.md`](./04-motion.md) | Easings, durations, reveal / parallax / marquee patterns, reduced-motion. |
| [`05-components.md`](./05-components.md) | Buttons, links, eyebrows, tags, cards, nav, forms, marquees — with ready CSS. |
| [`06-migration.md`](./06-migration.md) | Map from the current hard-coded values to tokens, for retrofitting existing pages. |

---

## At a glance

| | Value |
|---|---|
| **Dominant background** | `#ffffff` |
| **Brand deep** | `#002D2B` |
| **Brand darkest / ink** | `#001F1D` |
| **Brand mid (accent/links)** | `#407B78` |
| **Brand light (highlight, on-dark accent)** | `#69C9C4` |
| **Display font** | Gallient (serif) |
| **Body / UI font** | Helvetica Neue (sans) |
| **Signature easing** | `cubic-bezier(.16, 1, .3, 1)` |
| **Default radius** | `6px` (`--radius-md`) |
| **Page gutter** | `clamp(20px, 5vw, 80px)` |
| **Section rhythm** | `clamp(72px, 12vh, 150px)` |

---

## Scope & status

These docs describe the bespoke Darak component layer (`.oh*` / `.zt*` styles).
The site also still ships legacy WordPress/Elementor CSS (Roboto, `#676767`,
`15px` radii, etc.) inherited from the original template — that layer is **not**
part of this system and should be migrated toward these tokens over time. See
[`06-migration.md`](./06-migration.md).
