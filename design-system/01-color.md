# Color

White is the canvas; emerald is the brand. The system is **two-tier**: raw
*primitives* (the palette) feed role-based *semantic* tokens. **Components only
ever consume semantic tokens** — that's what keeps every page coherent and makes
re-theming a one-line change.

---

## 1 · Brand palette (primitives)

The four bold steps are the canonical Darak brand colors. The intermediate steps
are derived bridges used for tints, hovers, and functional states.

| Token | Hex | Swatch | Role |
|-------|-----|:------:|------|
| `--emerald-50`  | `#EEF4F3` | 🟩 lightest | faint section wash, hover bg |
| `--emerald-100` | `#D7E6E4` | 🟩 | tint surfaces, chips |
| `--emerald-200` | `#AECECB` | 🟩 | borders on tint, disabled |
| **`--emerald-300`** | **`#69C9C4`** | 🟩 | **BRAND · light aqua** — highlights, accent *on dark*, decorative |
| `--emerald-400` | `#4F9D98` | 🟩 | bridge / hover |
| **`--emerald-500`** | **`#407B78`** | 🟩 | **BRAND · mid teal** — secondary accent, UI, links |
| `--emerald-600` | `#295E5B` | 🟩 | inline links on white (better contrast) |
| `--emerald-700` | `#16403E` | 🟩 | pressed / deep accent |
| **`--emerald-800`** | **`#002D2B`** | 🟩 | **BRAND · deep emerald** — primary actions, dark fills |
| **`--emerald-900`** | **`#001F1D`** | 🟩 | **BRAND · darkest** — dark backgrounds, body ink |

### Meaning (from the brand brief)
- **Deep emerald** (`800`/`900`) → trust, exclusivity, weight. Anchors the brand.
- **Mid teal** (`500`) → the calm working accent.
- **Light aqua** (`300`) → softness, care, hospitality; the "reflection."

### Neutrals (white-dominant)
Off-whites carry a faint emerald cast so light surfaces feel intentional, not gray.

| Token | Hex | Role |
|-------|-----|------|
| `--white` / `--paper-1` | `#FFFFFF` | base page background (the dominant color) |
| `--paper-2` | `#F4F8F7` | alternating sections, subtle wash *(replaces old `#f2f2f2`)* |
| `--paper-3` | `#E4EFED` | media placeholders, inset fills *(replaces `#e9e9e7`)* |

### Ink (text)
All text tones are **alpha variants of emerald-900**, so muted text reads as a
soft emerald-gray rather than a foreign neutral.

| Token | Value | Role |
|-------|-------|------|
| `--ink` | `#001F1D` | primary text |
| `--ink-soft` | `rgba(0,31,29,.64)` | secondary text, body on busy pages |
| `--ink-muted` | `rgba(0,31,29,.46)` | captions, meta, eyebrow on light |
| `--ink-faint` | `rgba(0,31,29,.30)` | placeholders, disabled |
| `--hairline` | `rgba(0,31,29,.12)` | borders, dividers |
| `--hairline-strong` | `rgba(0,31,29,.26)` | hovered borders |

---

## 2 · Semantic tokens (use these)

| Token | Light default | Use for |
|-------|---------------|---------|
| `--color-bg` | white | page / section background |
| `--color-surface` | `#F4F8F7` | alternating section, raised panel |
| `--color-surface-sunk` | `#E4EFED` | image placeholder, inset |
| `--color-text` | `#001F1D` | primary text & headings |
| `--color-text-soft` | ink 64% | secondary text |
| `--color-text-muted` | ink 46% | meta, captions, eyebrows |
| `--color-border` | ink 12% | hairlines, dividers |
| `--color-border-strong` | ink 26% | hover/active borders |
| `--color-primary` | `#002D2B` | solid buttons, dark fills |
| `--color-primary-hover` | `#001F1D` | primary hover |
| `--color-on-primary` | white | text/icon on a primary fill |
| `--color-secondary` | `#407B78` | secondary accents, UI |
| `--color-accent` | `#69C9C4` | highlights, decorative marks |
| `--color-link` | `#295E5B` | inline links on white |
| `--color-link-hover` | `#002D2B` | link hover |
| `--color-focus` | `#407B78` | focus ring |

---

## 3 · Dark sections — the `.on-dark` scope

Darak uses full deep-emerald "moment" sections (nav overlay, hero captions,
philosophy, leaders, CTAs). Don't restyle each element — wrap the section in
`.on-dark` and every semantic token flips:

```html
<section class="on-dark" style="background: var(--color-bg);">
  <span class="eyebrow">Our philosophy</span>   <!-- becomes light aqua -->
  <h2>Built to endure</h2>                       <!-- becomes off-white -->
  <a class="btn btn--primary">View projects</a>  <!-- light fill, emerald text -->
</section>
```

Inside `.on-dark`: `--color-bg` → `#001F1D`, text → off-white, accents/links →
light aqua `#69C9C4`, and the "primary" button inverts to a light fill with
emerald text.

---

## 4 · Pairings & accessibility

Measured WCAG contrast ratios. **Honor these — they're the guardrails that keep
the palette legible.**

| Foreground | Background | Ratio | Verdict |
|-----------|------------|------:|---------|
| `--ink` `#001F1D` | white | **17.3:1** | ✅ AAA — default body & headings |
| `#002D2B` | white | **14.9:1** | ✅ AAA |
| `--emerald-600` `#295E5B` | white | **7.4:1** | ✅ AAA — preferred for inline links |
| `--emerald-500` `#407B78` | white | **4.8:1** | ✅ AA (normal text) — links, secondary text, UI |
| `--emerald-300` `#69C9C4` | white | **1.95:1** | ⛔ **decorative / borders only — never text** |
| white | `#002D2B` | **14.9:1** | ✅ AAA — text on primary buttons |
| white | `#001F1D` | **17.3:1** | ✅ AAA |
| `--emerald-300` `#69C9C4` | `#001F1D` | **8.8:1** | ✅ AAA — the accent voice on dark |
| `--on-dark` `#F4F8F7` | `#001F1D` | ~16:1 | ✅ AAA — text on dark sections |

### Rules of thumb
- **Body & long-form text:** always `--color-text` (`--ink`). Never set body in
  `--emerald-500` and never in `--emerald-300`.
- **Mid teal `#407B78`** is fine for links, labels, and UI on white (AA), but
  prefer `--emerald-600` for small inline links to clear AAA.
- **Light aqua `#69C9C4`** on white is for *fills, rules, dots, and decoration
  only*. As **text it must sit on deep emerald** (`800`/`900`).
- Every interactive element needs a visible focus ring — use `--color-focus`
  (`2px` solid + `2px` offset).

---

## 5 · Where each color shows up

- **White `--color-bg`** — the default everywhere; project grid, journal, news,
  forms, most sections.
- **`#F4F8F7` `--color-surface`** — alternating sections to create rhythm without
  harsh contrast.
- **Deep emerald `#002D2B`/`#001F1D`** — primary buttons, the nav overlay menu,
  dark "moment" sections, card detail overlays, image gradient scrims.
- **Mid teal `#407B78`** — links, active filter accents, focus, small UI marks,
  the expansion-map pins.
- **Light aqua `#69C9C4`** — eyebrow dots and accents *on dark*, hover
  highlights, decorative underlines, marquee separators.

---

## 6 · Don'ts

- ❌ Don't introduce new grays — use the ink alphas.
- ❌ Don't put `#69C9C4` text on white or `#F4F8F7`.
- ❌ Don't use pure black `#000` for text or fills — use `--ink` / `--emerald-900`.
- ❌ Don't fill large areas with emerald "just because"; white must stay dominant.
- ❌ Don't hard-code hex in components — go through semantic tokens.
