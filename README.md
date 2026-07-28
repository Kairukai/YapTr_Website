# YapTr_Website

The public website for **YapTr** — a free, fully-local Japanese→English live
subtitle translator for Windows. The app itself lives in a separate repo
(`TranslateJP_EN`); this repo is only the site.

**Live at <https://kairukai.github.io/YapTr_Website/>**

It's a single static page with **no build step and no dependencies**:
`index.html` holds the markup, CSS, and JS inline, and `assets/` holds the
mascot art, fonts, and social card. The page makes **no third-party requests** —
fonts are self-hosted and there is no analytics of any kind, matching the app's
own privacy posture.

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

## Downloads live here too

The YapTr installer is published as a **GitHub Release on this repo**, and the
site's download buttons link straight to that asset. The app's own source repo
stays private, and release assets don't count toward this repo's size — see
**[PLAN.md](PLAN.md) §0 and §4d** for why it's set up this way.

## Still a test run

The site is deployed, but no release has been published yet, so every download
button 404s. The About section also still contains placeholder copy. See
**[PLAN.md](PLAN.md) §5** for the short list of what's left.

## Shipping a new app version

Update the `RELEASE` constant in `index.html` — it drives the version and size
shown in all three places on the page. Full checklist in **[PLAN.md](PLAN.md) §7**.

## Plan and conventions

[PLAN.md](PLAN.md) covers the site's scope and non-goals, the design tokens
(inherited from the app), why each section exists, the roadmap, and the editing
conventions. Read §0 and §4 before changing copy — the honest "Before you
download" section is load-bearing, not filler.
