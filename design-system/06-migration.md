# Migration Guide

How to retrofit the existing pages onto the design system. The site currently
hard-codes values inline; move them to tokens incrementally — page by page,
section by section. Nothing breaks if old and new coexist during the transition.

---

## 1 · Color find-and-replace

The bespoke Darak components use a small, consistent set of literals. Map them:

| Current literal | → Token | Notes |
|-----------------|---------|-------|
| `#ffffff`, `#fff` (bg) | `var(--color-bg)` | the dominant white |
| `#f2f2f2` (light fill / alt section) | `var(--color-surface)` | now a faint emerald wash `#F4F8F7` |
| `#f2f2f2` (text **on dark**) | `var(--color-text)` *(within `.on-dark`)* or `var(--on-dark)` | |
| `#e9e9e7` (media placeholder) | `var(--color-surface-sunk)` | |
| `#111111`, `#1a1a1a` (text) | `var(--color-text)` | now emerald-ink `#001F1D` |
| `#0e0e0e`, `#000000` (dark bg) | `var(--color-dark-bg)` | now `#001F1D`; wrap section in `.on-dark` |
| `#9a9a9a`, `#6e6e6e` (muted) | `var(--color-text-muted)` | |
| `rgba(17,17,17,.5/.6/.62)` | `var(--color-text-soft/-muted)` | ink alphas |
| `rgba(0,0,0,.12/.16)` (borders) | `var(--color-border)` | |
| `#5e5e5e` (map pins / "accent") | `var(--color-secondary)` `#407B78` | promote these to real emerald accent |
| any new accent | `var(--color-accent)` `#69C9C4` (on dark) / `--color-secondary` (on light) | |

> The biggest visible shift: text goes from neutral `#111` to emerald-ink
> `#001F1D`, and the old neutral grays become emerald-tinted. This is intentional
> — it ties the whole site to the brand.

## 2 · Typography
- Replace inline `font-family:'Gallient',Georgia,serif` → `var(--font-display)`.
- Replace `'Helvetica Neue',Arial,sans-serif` → `var(--font-sans)`.
- Swap bespoke `clamp(...)` font sizes for the nearest `--fs-*` token where it
  matches; keep one-off display sizes if a section needs a unique scale, but pull
  line-height/tracking from tokens.
- **Legacy WordPress/Elementor** type (`var(--e-global-typography-*)`, Roboto) is
  not part of the system — replace with `--font-sans`/`--font-display` when you
  touch those blocks.

## 3 · Spacing, radii, motion
- `clamp(72px,12vh,150px)` section padding → `var(--section-y)`.
- side padding `clamp(20px,3.2vw,48px)` / `clamp(22px,5vw,80px)` → `var(--gutter)`.
- `border-radius: 6px/10px/3px/999px/50%` → `--radius-md/lg/sm/pill/round`.
- Replace inline `cubic-bezier(.16,1,.3,1)` → `var(--ease-signature)`; durations
  `.3s/.4s/.7s/1.1s` → `--dur-fast/base/slow/reveal`.
- Note: the site contains several one-off easings (overshoot, etc.) from the
  template — consolidate toward the four motion tokens.

## 4 · Dark sections → `.on-dark`
Find sections with a dark background and inverted text (nav overlay, hero
captions, philosophy, leaders, pinned video, CTA) and:
1. Set their background to `var(--color-dark-bg)` / `var(--color-dark-surface)`.
2. Add `class="on-dark"`.
3. Delete the per-element light-color overrides (`color:#f2f2f2`,
   `rgba(242,242,242,.x)`, etc.) — the scope handles them.

## 5 · Suggested order
1. Drop in `tokens.css` globally (no visual change yet).
2. Migrate **shared chrome** first: nav, footer, buttons, eyebrows, forms.
3. Then page by page: Home → Projects → Journal → About → Contact → legal.
4. Convert dark sections to `.on-dark` as you reach them.
5. Delete dead legacy CSS once a page is fully on tokens.

## 6 · Guardrails
- After migrating a section, re-check contrast against `01-color.md` (especially
  anything that was gray text and is now emerald-tinted).
- Don't leave `#69C9C4` as text on a light background.
- Keep white dominant — migration is about *recoloring ink and accents*, not
  flooding pages with emerald.
- Verify `.on-dark` sections didn't lose focus-ring visibility (`--color-focus`
  becomes light aqua there).
