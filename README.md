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
stays private, and release assets don't count toward this repo's size, so a
511 MB installer here doesn't bloat the clone or the Pages deploy.

**v1.0.0 is published** — `YapTr-1.0.0-setup.exe`, 511 MB, with the SHA-256 in
the release notes.

## Shipping a new app version

1. Update the `RELEASE` constant in `index.html` — it drives the version and size
   shown in all three places on the page — and the matching literals in the
   `[data-app]` spans, which are the no-JS fallback.
2. Attach the installer to a new release **without renaming it**. The download
   URL is built as `YapTr-<version>-setup.exe`; any other name 404s every
   download button on the site.
3. Click the download button once afterwards and confirm it actually downloads.

## Conventions

- Everything lives in `index.html`. Don't split the CSS/JS out until there's a
  second page that shares them.
- **No third-party requests.** No CDNs, no hosted fonts, no analytics, no
  embeds — fonts are self-hosted and it stays that way. If something needs an
  external file, vendor it into `assets/`.
- Every animation needs a `prefers-reduced-motion` answer, and every interactive
  element needs a visible `:focus-visible` state.
- Copy stays plain-spoken, and the "Before you download" section is load-bearing
  rather than filler — never soften the machine-translation caveat.
