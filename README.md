# YapTr_Website

The public website for **YapTr** — a free, fully-local Japanese→English live
subtitle translator for Windows. The app itself lives in a separate repo
(`TranslateJP_EN`); this repo is only the site.

It's a single static page with **no build step and no dependencies**:
`index.html` holds the markup, CSS, and JS inline, and `assets/` holds the
mascot art extracted from the app's own icon.

## Run it locally

```powershell
start .\index.html                       # simplest — just open the file
python -m http.server 8000 --directory . # matches how GitHub Pages serves it
```

Edit `index.html`, refresh the browser. There is nothing to compile or restart.

## Deploy

Push to `main`. GitHub Pages serves from the repo root and redeploys
automatically — no workflow file involved.

One-time setup: **Settings → Pages → Source: Deploy from a branch → `main` /
(root)**. The site then lives at `https://kairukai.github.io/YapTr_Website/`.

## Before this goes live

The download buttons point at the app's GitHub Releases page, which doesn't
exist publicly yet, and the About section still contains placeholder copy.
See **[PLAN.md](PLAN.md) §5** for the full launch checklist.

## Plan and conventions

[PLAN.md](PLAN.md) covers the site's scope and non-goals, the design tokens
(inherited from the app), why each section exists, the roadmap, and the editing
conventions. Read §0 and §4 before changing copy — the honest "Before you
download" section is load-bearing, not filler.
