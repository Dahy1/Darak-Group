# Typography

Two typefaces, used with a clear division of labor: an oversized serif for
expression, a quiet sans for everything functional.

---

## 1 · Typefaces

| Role | Family | Token | Notes |
|------|--------|-------|-------|
| **Display** | **Gallient** (serif) | `--font-display` | Headlines, hero wordmarks, card titles, the logotype. `400` weight only. Fallback: `Georgia, 'Times New Roman', serif`. |
| **Body / UI** | **Helvetica Neue** (sans) | `--font-sans` | Body copy, labels, buttons, form fields, navigation, captions. Fallback: `Arial, Helvetica, sans-serif`. |

`@font-face` for Gallient (already in the pages):

```css
@font-face {
  font-family: 'Gallient';
  font-style: normal;
  font-weight: 400;
  font-display: swap;                 /* `block` is acceptable for the wordmark */
  src: url('/wp-content/uploads/2026/02/Gallient.woff2') format('woff2');
}
```

> Gallient ships in a single weight (400). Never fake bold it — use size and
> color for emphasis. Helvetica Neue carries the weight range (400/500/600/700).

---

## 2 · Type scale (fluid)

All sizes are `clamp(min, viewport, max)` so they scale smoothly between mobile
and desktop without breakpoints. Tokens live in `tokens.css`.

| Token | clamp() | Font | Use |
|-------|---------|------|-----|
| `--fs-display` | `clamp(54px, 12vw, 200px)` | display | hero wordmarks (Our News, Contact, Journal, About) |
| `--fs-h1` | `clamp(40px, 6vw, 92px)` | display | page / section title |
| `--fs-h2` | `clamp(32px, 4.6vw, 76px)` | display | sub-section headline |
| `--fs-h3` | `clamp(22px, 2.1vw, 34px)` | display | card titles |
| `--fs-h4` | `clamp(20px, 1.9vw, 27px)` | display | small card titles |
| `--fs-lead` | `clamp(16px, 1.3vw, 20px)` | sans | intros / standfirst |
| `--fs-body` | `clamp(15px, 1.2vw, 19px)` | sans | body copy |
| `--fs-small` | `14px` | sans | secondary / dense UI |
| `--fs-eyebrow` | `12px` | sans | uppercase labels |
| `--fs-caption` | `11px` | sans | meta, counters |

### Line-height & tracking tokens
| Token | Value | For |
|-------|-------|-----|
| `--lh-tight` | `0.9` | display wordmarks |
| `--lh-snug` | `1.06` | headings |
| `--lh-normal` | `1.5` | body |
| `--lh-relaxed` | `1.6` | long prose |
| `--tracking-display` | `-0.02em` | display |
| `--tracking-tight` | `-0.01em` | headings |
| `--tracking-eyebrow` | `0.22em` | uppercase labels (range 0.14–0.28em) |
| `--tracking-wide` | `0.14em` | buttons, small caps UI |

---

## 3 · Roles

### Display / headings
```css
.h-display { font-family: var(--font-display); font-weight: 400;
  font-size: var(--fs-display); line-height: var(--lh-tight);
  letter-spacing: var(--tracking-display); color: var(--color-text); }

.h2 { font-family: var(--font-display); font-weight: 400;
  font-size: var(--fs-h2); line-height: var(--lh-snug);
  letter-spacing: var(--tracking-tight); color: var(--color-text); }
```

Some headlines (e.g. the "A HOME — A LIFETIME STORY" block) use **uppercase
sans, 700** instead of serif — that's an intentional alternate voice for
statement headings. Pick one voice per section; don't mix within a heading.

### Eyebrow / label
The recurring small uppercase tag, usually with a leading dot or `(01)` index.
```css
.eyebrow { font-family: var(--font-sans); font-size: var(--fs-eyebrow);
  letter-spacing: var(--tracking-eyebrow); text-transform: uppercase;
  color: var(--color-text-muted); display: inline-flex; align-items: center; gap: 11px; }
.eyebrow::before { content: ""; width: 7px; height: 7px; border-radius: 50%;
  background: currentColor; }     /* dot — turns light-aqua inside .on-dark */
```

### Body & lead
```css
.lead { font-size: var(--fs-lead); line-height: var(--lh-relaxed); color: var(--color-text-soft); }
.body { font-size: var(--fs-body); line-height: var(--lh-relaxed); color: var(--color-text-soft);
        max-width: 46ch; }                      /* keep prose to ~46–60ch */
```

### Meta / caption
```css
.meta { font-size: var(--fs-caption); letter-spacing: .06em; color: var(--color-text-muted); }
```

---

## 4 · Rules

- **One display family.** Gallient for expressive headings; never use it for body.
- **Measure.** Cap prose at `~46–60ch` for readability (`--container-text` = 720px
  for centered prose blocks).
- **Hierarchy by size & color, not weight** (Gallient is single-weight). Use
  `--color-text` → `--color-text-soft` → `--color-text-muted` to step down.
- **Tracking:** tighten display (`-0.02em`), open uppercase labels (`0.14–0.28em`).
- **Numerals** in counters/specs: `font-variant-numeric: tabular-nums`.
- Headings inherit color from `--color-text`, so they invert automatically inside
  `.on-dark`.
