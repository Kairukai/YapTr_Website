# YapTr Website — Plan

**Snapshot: 2026-07-28.** Living plan for the YapTr marketing/download site.
The app itself lives in a separate repo (`TranslateJP_EN`); this repo is only
the public website.

---

## 0. What this site is for (scope)

YapTr is a **free, unsigned, 535 MB Windows installer that captures desktop
audio**. That single sentence decides the whole design. This site is not a
product funnel, a docs portal, or a blog — it is a **download page plus a trust
page**, and its job is to remove the reasons a first-time visitor bails:

1. They don't know what the app looks like in use.
2. SmartScreen will call it unsafe.
3. A half-gigabyte download for a subtitle tool looks suspicious.
4. An app that listens to your audio needs its privacy story stated up front.

Every section on the page maps to one of those four. **Anything that doesn't
map to one of them is a candidate for deletion**, not addition.

### Non-goals (deliberate)
- No feature comparison tables, testimonials, pricing, or newsletter capture.
- No analytics or tracking of any kind — it would contradict the app's pitch.
- No CMS, no framework, no build pipeline (see §2 for why).
- No user docs here; those stay in the app repo's `README.md` / `CONFIG.md`.

---

## 1. Status

| Area | State |
| --- | --- |
| Page structure + copy | **DONE** — all sections built and rendering |
| Visual design + motion | **DONE** — brand-matched, reduced-motion honored |
| Brand assets | **DONE** — extracted from the app's real `jpen.ico` |
| About copy | **PLACEHOLDER — owner rewrite required** (§5) |
| Download link | **BROKEN until a GitHub Release exists** (§5) |
| Deployment | **NOT YET DEPLOYED** — Pages not enabled, nothing pushed |
| Demo footage | **NOT STARTED** — simulated overlay stands in (§6) |

Nothing is committed yet. The working tree holds the whole site.

---

## 2. Architecture

```
index.html      the entire site — markup, CSS, and JS inline (~750 lines)
assets/
  yappy-256.png hero / about / closing mascot
  yappy-64.png  nav + favicon-size mascot
  favicon.ico   copied verbatim from the app's packaging/jpen.ico
PLAN.md         this file
README.md       orientation, points here
```

**There is no build step and no dependency tree.** Editing means opening
`index.html`; deploying means `git push`. This is a deliberate call, not
laziness — the site is one page with no application state, so a framework would
add a toolchain to maintain while buying nothing. Revisit only if the site grows
past ~4 pages, and prefer **Astro** over React if so (component authoring, still
ships zero JS by default).

### Assets are derived, not authored
The mascot PNGs are extracted from `TranslateJP_EN/packaging/jpen.ico`, which is
itself rendered from `src/jpen/ui/mascot.py` at build time. **Yappy has no
source image file anywhere** — he is vector QPainter geometry.

Consequence: if the mascot changes in the app, re-extract rather than editing the
PNGs by hand. The 256px frame needs manual extraction (`System.Drawing` silently
downscales 256px icon frames to 128px); read the ICO directory, seek to the
256×256 entry, and copy its bottom-up BGRA rows directly.

---

## 3. Design system

Colors are inherited from the app so the site and the product feel like one
thing. Source of truth: `src/jpen/ui/mascot.py` and `ui/styles/dark.qss`.

| Token | Value | Role |
| --- | --- | --- |
| `--fur` | `#8b5a32` | mascot fur; primary warm accent |
| `--fur-lit` | `#c98a4b` | section labels, gradients |
| `--muzzle` | `#f0deba` | links, highlight text |
| `--red` | `#e50914` | the app's accent — CTAs and warnings only |
| `--bg` | `#16110e` | warm near-black (deliberately not neutral) |

- **Type:** Fredoka (headings — rounded and friendly, matches the bear) + Inter
  (body). Loaded from Google Fonts; see §5 for why that should change.
- **Motion:** mascot bob, drifting background blobs, waveform bounce, typing
  caret, hover lifts, scroll reveals. All of it collapses under
  `prefers-reduced-motion: reduce`, and the subtitle demo falls back to a static
  translated line rather than freezing mid-type.
- **Red is rationed.** It marks calls to action and the two genuine warnings.
  Using it for decoration would blunt both.

---

## 4. Page structure

| # | Section | Job |
| --- | --- | --- |
| 1 | Nav (sticky) | persistent download affordance |
| 2 | Hero | one-sentence pitch + primary CTA |
| 3 | **Live subtitle demo** | show the product in ~3 seconds |
| 4 | How it works (3 cards) | desktop audio / local / stays out of the way |
| 5 | **Before you download** (5 notes) | the trust section — see below |
| 6 | Privacy | the differentiator vs. every cloud translator |
| 7 | Requirements | pre-empt "will this run for me" |
| 8 | About | who made it and why |
| 9 | Closing CTA + footer | second download, source links |

### The subtitle demo (§3 above)
A simulated "Desktop audio" window: animated waveform, a Japanese line under
*Heard*, then English typing character-by-character into a replica of the real
overlay bar. Cycles through 5 stream-flavored line pairs.

It exists because **there is no real demo footage yet** and an empty placeholder
box was worse than nothing. It is honestly labeled as a simulation in its
footer. When real footage lands it should sit *beside* this, not necessarily
replace it — the animation loads instantly and needs no click.

### "Before you download" — the load-bearing section
Five honest notes, in this order: SmartScreen warning · Japanese-only ·
machine-translation caveat · download size · GPU is optional.

**This section is the point of the site.** It converts skeptics by refusing to
hide anything, and it mirrors the app's own posture — the reliability disclaimer
is shown on first run for the same reason. Two standing rules:

- **Never soften the machine-translation caveat.** Translation is currently
  blunt Whisper `task="translate"`; the two-stage quality rework ships off and
  isn't live-proven. Overselling accuracy earns a wave of issues you already
  know about.
- **Japanese-only is framed as a design decision, not a gap** — segmentation and
  timing are tuned around Japanese speech, and that tuning is why it keeps up
  live.

---

## 5. Blocking items before launch

Ordered. The first two are hard blockers.

1. **Publish a GitHub Release.** Every CTA points at
   `github.com/Kairukai/TranslateJP_EN/releases/latest`, which currently
   **404s** — the app repo isn't publicly reachable and has no release. Until
   that's fixed the download button, the `Source` link, and the `Report an issue`
   link are all dead. No site change is needed once the release exists.
2. **Rewrite the About copy.** The three paragraphs in `#about` are inferred
   placeholder text, marked with a `TODO` comment. They assume a personal-itch
   origin story, a solo project with no company, and the issue tracker as the
   contact route. Correct or replace.
3. **Publish the installer's SHA-256** on the release page. The site tells
   people to verify against it, so it has to exist.
4. **Self-host the fonts.** The page currently pulls Fredoka and Inter from
   Google. A site whose headline claim is "no network requests" should not phone
   home to Google either. Drop the two `.woff2` files into `assets/` and swap the
   `<link>` for an inline `@font-face`.
5. **Enable GitHub Pages** — Settings → Pages → `main` / root. Live at
   `https://kairukai.github.io/YapTr_Website/`.

---

## 6. Roadmap

### Phase 1 — Launch (blocked only by §5)
Ship the page as-is once the release exists and About is rewritten.

### Phase 2 — Real demo footage
A short screen recording of the overlay subtitling an actual Japanese stream.
**This is the highest-value remaining asset** and the one thing that can't be
authored here — it needs a real capture session. Target a silent, looping,
sub-10-second clip; encode as MP4 with a WebM fallback, autoplay muted.

### Phase 3 — FAQ
Natural first questions: subtitles lagging behind speech · GPU not detected ·
no audio being picked up · which model size to use. Sections on the same page;
only split into separate files once the page is genuinely too long to scroll.

### Phase 4 — Changelog
Only worth adding once there's a second release to compare against. Should be
generated from GitHub releases rather than hand-maintained.

### Deferred / maybe never
Custom domain (nicer than a `github.io` subpath for a trust-sensitive download,
but costs money and DNS upkeep) · a docs section (belongs in the app repo until
proven otherwise) · localization of the site itself.

---

## 7. Working procedure

**Run locally**

```powershell
start .\index.html                       # simplest
python -m http.server 8000 --directory . # matches how Pages serves it
```

**Deploy** — `git push` to `main`. Pages redeploys automatically; there is no
workflow file and nothing to trigger.

**Conventions**
- Keep everything in `index.html`. Don't split CSS/JS into separate files until
  there's a second page that shares them.
- Match the surrounding style: CSS custom properties for anything reused, plain
  ES5-compatible JS in one IIFE, no libraries.
- Every animation needs a `prefers-reduced-motion` answer.
- Copy stays plain-spoken. No marketing superlatives, no "revolutionary",
  no invented capabilities. The honesty *is* the positioning.
- Verify visually before committing — headless Edge works:
  `msedge --headless --disable-gpu --screenshot=out.png --window-size=1280,5400 --hide-scrollbars "file:///.../index.html"`

---

## 8. Risks

| Risk | Mitigation |
| --- | --- |
| Unsigned installer scares people off | §5 item 1 + the SmartScreen note; long-term, code signing in the app repo |
| Site oversells translation quality | The caveat note is standing policy (§4) |
| Mascot drifts out of sync with the app | Assets are re-extracted from `jpen.ico`, never hand-edited (§2) |
| Page grows into an unmaintainable single file | Split at ~4 pages, and move to Astro rather than React (§2) |
| Dead links if the app repo stays private | §5 item 1 is a hard launch blocker for exactly this reason |
