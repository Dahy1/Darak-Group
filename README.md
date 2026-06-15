# Darak Group

Marketing website for **Darak Group**, an Egyptian real-estate developer.

The project ships in two forms:

- **`site/`** — the static site (HTML/CSS/JS, GSAP + Lenis), served as-is.
- **`darak-next/`** — a Next.js 14 (App Router) mirror generated from `site/` via the build scripts. Run `npm install` then `npm run build` / `npm run start` inside this folder.

## Build pipeline

The Python scripts in the repo root regenerate parts of the site and the Next mirror:

- `build_projects.py` — the tabbed "Our Projects" showcase (homepage carousel + projects-page grid).
- `build_blog.py` — the Journal (blog) listing and article pages.
- `footer_redesign.py` — the site-wide footer.
- `rewrite_copy.py` — site-wide copy.
- `build_next.py` + `gen_next.py` — convert `site/` into the `darak-next/` Next app.

## Pages

Home · About · Projects (+ project details) · Journal (+ articles) · Careers · Contact · legal pages.
