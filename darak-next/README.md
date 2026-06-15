# Olivia Harper Homes — Next.js

The static site (`../site`) converted to a Next.js 14 App-Router app. Every page reuses
the **homepage's** nav, mobile menu, and footer.

## Run
```bash
npm install
npm run dev      # http://localhost:3000
npm run build    # static export of all 16 routes
npm start
```

## How it's structured
- `app/layout.jsx` — the shared shell: injects the homepage's `<head>` CSS, then renders
  `<Nav/>`, the page, `<Footer/>`, and the global scripts.
- `components/Nav.jsx` / `Footer.jsx` — the homepage's `zt-nav` + `zt-overlay` menu and the
  homepage footer, reused on **every** route (this is the "repetitive components" requirement).
- `components/SiteScripts.jsx` — loads the original site scripts (jQuery, GSAP, ScrollTrigger,
  Lenis, Elementor, the nav + animation boots) in order on the client, skipping non-JS
  (JSON-LD) blocks, and refreshes ScrollTrigger after assets load.
- `app/<route>/page.jsx` — one per page; injects that page's unique content + page-specific CSS
  + page-specific scripts.
- `content/` — extracted HTML/CSS/script data (generated, see below).
- `public/` — all original assets (`wp-content`, `wp-includes`, `cdnjs`).

## Regenerating from the static site
The `content/` files and `app/*/page.jsx` are produced by two scripts in the parent folder:
```bash
python ../build_next.py   # extract shared chrome + per-page content from ../site
python ../gen_next.py     # write layout, components, and page.jsx files
```
Edit the static `../site` pages, re-run both, and the Next app updates.

## Notes
- Versioned asset URLs (`…_ver%3D1.0.css`) are decoded to `=` so they resolve from `public/`.
- Navigation uses plain `<a>` (full reloads), which keeps each Elementor/GSAP page self-contained.
- `next.config.mjs` uses `trailingSlash` + unoptimized images to mirror the original URLs/assets.
