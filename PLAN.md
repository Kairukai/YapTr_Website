# YapTr Website — Plan

**Snapshot: 2026-07-28.** Living plan for the YapTr marketing/download site.
The app itself lives in a separate repo (`TranslateJP_EN`); this repo is only
the public website.

**Live at <https://kairukai.github.io/YapTr_Website/>** — GitHub Pages, free
tier, deploying from `main` / root. No custom domain (see §6).

---

## 0. What this site is for (scope)

YapTr is a **free, unsigned, 511 MB Windows installer that captures desktop
audio**. That single sentence decides the whole design. This site is not a
product funnel, a docs portal, or a blog — it is a **download page plus a trust
page**, and its job is to remove the reasons a first-time visitor bails:

1. They don't know what the app looks like in use.
2. SmartScreen will call it unsafe.
3. A half-gigabyte download for a subtitle tool looks suspicious.
4. An app that listens to your audio needs its privacy story stated up front.

Every section on the page maps to one of those four. **Anything that doesn't
map to one of them is a candidate for deletion**, not addition.

### Distribution model (decided 2026-07-28)

**The app's source stays private. Only the installer is public.**

- `Kairukai/TranslateJP_EN` — **private**. Source, planning docs, git history.
- `Kairukai/YapTr_Website` — **public** (this repo). The installer is published
  as a **GitHub Release here**, on the website repo, rather than on the app repo
  or a third repo.

Why here: **release assets on a private repo require authentication to
download** — an anonymous visitor gets a 404 — so the download has to be served
from *some* public repo. A dedicated `YapTr-Releases` repo was considered and
rejected as an unnecessary third repo; this one is already public (GitHub Pages
on the free tier requires it), so publishing releases here costs nothing and
creates nothing new to maintain.

Release assets are stored outside the git repo and don't count toward its size,
so a 511 MB installer here does not bloat the site's clone or its Pages deploy.

The owner's constraint is not wanting the code copied. Worth recording honestly:
the installer is a PyInstaller freeze, and Python bytecode can be extracted from
those bundles and decompiled with common tools. Keeping the repo private stops
casual copying, which is the actual concern, but it is a speed bump rather than
real protection. Nothing on the site should claim otherwise.

**Consequence for the copy:** the site previously claimed "Open source" in five
places. With the source closed those claims are false, so they were removed —
see §4e. The privacy claims (no telemetry, nothing written to disk, no network
calls) remain, but visitors now have to take them on trust rather than being able
to verify them. That is a real reduction in the trust story for an unsigned
binary, and it is the price of keeping the source closed.

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
| Deployment | **LIVE** — public repo, Pages on, HTTPS by default |
| Fonts | **DONE** — self-hosted, zero third-party requests (§3) |
| Social preview | **DONE** — 1200×630 card, absolute URLs (§4a) |
| Keyboard accessibility | **DONE** — focus rings + skip link (§4b) |
| Release values | **DONE** — single-sourced from one JS constant (§4c) |
| Download flow | **BUILT** — one-click direct-to-file (§4d) |
| v1.0.0 release | **PUBLISHED** — installer attached, checksum in notes (§4f) |
| Pushing the above | **PENDING — the live site is still the pre-fix version** (§5) |
| About copy | **PLACEHOLDER — owner rewrite required** (§5) |
| Demo footage | **NOT STARTED** — simulated overlay stands in (§6) |

---

## 2. Architecture

```
index.html          the entire site — markup, CSS, and JS inline (~780 lines)
assets/
  yappy-256.png     hero / about / closing mascot
  yappy-64.png      nav + favicon-size mascot
  favicon.ico       copied verbatim from the app's packaging/jpen.ico
  og-image.png      1200x630 social preview card (generated — see §4a)
  fonts/
    fredoka-latin.woff2   headings, variable 300-700 (30 KB)
    inter-latin.woff2     body, variable 100-900 (48 KB)
tools/
  og-card.html      source for og-image.png; never linked from the site
PLAN.md             this file
README.md           orientation, points here
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
  (body), both **self-hosted** in `assets/fonts/`.

  They were originally loaded from Google Fonts, which was a quiet contradiction:
  a page whose headline claim is *"nothing ever leaves your computer"* was making
  a third-party request on every visit. The page now issues **zero third-party
  requests**. Both are variable fonts, so one file per family covers every weight
  (78 KB total), Latin subsets only — the Japanese in the demo deliberately falls
  back to the visitor's system CJK font, which is how it already rendered.

  To update a font, re-fetch the `latin` block from the Google Fonts CSS API with
  a browser `User-Agent` (it serves `.woff2` only to modern UAs), drop the file
  in `assets/fonts/`, and leave the `@font-face` rules alone.
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

### 4a. Social preview

`assets/og-image.png` is a 1200×630 card — Yappy, the headline, and three pills
(Fully local / No telemetry / Free). It is **generated, not hand-drawn**: the
source is `tools/og-card.html`, rendered with headless Edge. The exact command
is in a comment at the top of that file.

Two rules:

- **The `og:` and `twitter:` URLs must stay absolute.** They were relative
  originally, which meant crawlers couldn't resolve them and every shared link
  rendered as a blank grey box. If the site ever moves to a custom domain, every
  one of those URLs has to be updated — they hardcode the `github.io` origin.
- **Keep the card exactly 1200×630.** That's what Discord, Slack, X and iMessage
  crop to; anything else gets letterboxed.

This matters more than it would for most sites. A niche tool spreads by someone
pasting a link into a chat, so the preview card *is* a big share of the
first impression.

### 4b. Keyboard accessibility

- `:focus-visible` rings (3px, muzzle cream, 3px offset) on every link and
  button. `:focus-visible` rather than `:focus` so mouse clicks don't leave a
  ring behind, while keyboard users always see where they are.
- A **skip link** as the first focusable element, hidden off-screen until
  focused, jumping to `#main` on the hero.

There were no focus styles at all before this — keyboard users got the browser
default, which is close to invisible on the red gradient buttons.

### 4c. Release values (version and size)

The version and download size appear in three places (hero meta, the download-size
note, closing CTA). They used to be hardcoded in all three, which guarantees drift
the first time a release ships.

Now every occurrence is a `<span data-app="version">` / `<span data-app="size">`,
overwritten on load from a single `RELEASE` constant at the top of the script.
**Update that constant on each release and all three update together** — see the
checklist in §7.

The literal values remain in the HTML as a no-JS fallback, so the page is still
correct with JavaScript disabled. That is technically a second copy; the constant
is authoritative for essentially every real visitor, and the fallback is a
belt-and-braces measure rather than something to maintain in lockstep.

### 4d. Download links — one click, straight to the file

All three buttons (nav, hero, closing) point at GitHub's direct-asset path on
**this repo's** releases (see §0 — the app repo is private, so the download can't
be served from there):

```
https://github.com/Kairukai/YapTr_Website/releases/latest/download/YapTr-<version>-setup.exe
```

That URL 302-redirects to the binary, so a click starts the download
immediately rather than dropping the visitor on a release page to work out which
file they need. `/latest/` resolves server-side, so it always tracks the newest
release.

**Hard dependency:** the release asset must be named exactly
`YapTr-<version>-setup.exe`. That's what Inno Setup produces today
(`OutputBaseFilename=YapTr-{#MyAppVersion}-setup` in `installer.iss`), so
attaching the build output unmodified is all that's required. **Renaming the
asset on the release breaks every download button on the site**, silently, with
a 404.

Because the filename embeds the version, the URL is **built in JS from
`RELEASE.version`** rather than written out — bumping that one constant updates
the button labels and all three download URLs together. The full URL is also in
each `href` as a no-JS fallback.

Alongside the buttons is a quieter **"Release notes & SHA-256 checksum"** link to
the release page itself. That's deliberate: §4's trust section tells people to
verify the installer's hash, so there has to be a route to it. Direct download
for the 95% who just want the app, one small link for the people who check.

**Hard dependency #2:** this repo must stay **public**. Flipping it private
404s every download button. In practice that's already locked in — free GitHub
Pages requires a public repo, so the site would go dark at the same moment.

> **Not testable yet.** No release has been published, so these URLs are
> unverified. The first thing to check after publishing is that the hero button
> actually starts a download.

### 4e. What the site does NOT claim

The source is closed (§0), so these were removed rather than left as
comfortable-but-false marketing:

| Was | Now | Where |
| --- | --- | --- |
| "Open source" pill | "No ads, no upsells" | privacy pills |
| "Free and open source" | "Free, no account needed" | closing CTA |
| "built and maintained in the open" | "there's no company behind it" | About |
| `Source` → app repo | `All releases` → this repo's releases | footer |
| `Report an issue` → app repo | same, on this repo's issues | footer |

**Standing rule: don't reintroduce them.** "Open source" has a specific meaning,
and a page whose entire strategy is candour cannot afford a claim a curious
visitor can disprove in one click. If the source is ever opened, add a LICENSE
first — a public repo with no license is *source-available*, not open source,
and still wouldn't justify the phrase.

### 4f. Shipped releases

| Version | Date | Asset | Size (as GitHub reports it) | SHA-256 |
| --- | --- | --- | --- | --- |
| v1.0.0 | 2026-07-28 | `YapTr-1.0.0-setup.exe` | 511 MB | `89121f952667b6c01b0fefb040685b104d433a46f3d5d8f1aefdea9f6809ab55` |

**Quote sizes the way GitHub and Windows do.** The installer is 535,577,376
bytes — 535 MB in decimal, but **511 MB** in the MiB units that Windows Explorer,
browser download bars, and GitHub's release page all display. The site said
"535 MB" at first; on a page asking people to trust an unsigned binary, a visitor
seeing one number on the site and a different one in their download bar is
exactly the kind of small inconsistency that plants doubt. Always use the number
GitHub shows on the release.

**GitHub auto-attaches "Source code (zip)" and "(tar.gz)" to every release.**
There's no way to disable it. On this repo those archives contain the *website's*
source, which is already public — **not the app's**. Harmless, but expect the
question.



---

## 5. Blocking items before launch

Ordered. The first is a hard blocker — until it happens, none of the work below
is actually visible to anyone.

1. **Commit and push the working tree.** The fonts, social card and generator are
   already committed and pushed (`7180722`, `e62ea7e`). Still local: the size
   correction to 511 MB, the release record in §4f, and this section — i.e.
   `index.html`, `PLAN.md`, `README.md` modified. Until they land, the live page
   quotes the wrong download size.
2. **Verify the download end to end** once pushed — click the hero button and
   confirm `YapTr-1.0.0-setup.exe` starts downloading. The release exists (§4f),
   but the URL has never been exercised.
3. **Rewrite the About copy.** The three paragraphs in `#about` are inferred
   placeholder text, marked with a `TODO` comment. They assume a personal-itch
   origin story, a solo project with no company, and the issue tracker as the
   contact route. Correct or replace.

**Done and no longer blocking:** fonts self-hosted (§3) · Pages enabled and live ·
social preview fixed (§4a) · focus styles added (§4b) · release values
single-sourced (§4c) · one-click download built (§4d) · open-source claims
removed (§4e) · **v1.0.0 published with its SHA-256 (§4f)**.

---

## 6. Roadmap

### Phase 1 — Launch (blocked only by §5)
Push the pending work, confirm the download fires, rewrite About. The release
itself is already published.

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

**When the app ships a new release**

1. Update the `RELEASE` constant in `index.html` (`version` and `size`). Keep the
   non-breaking space in the size string so "511 MB" never wraps.
2. Update the same two literals in the three `[data-app]` spans — they're the
   no-JS fallback (§4c).
3. Update the hardcoded `href` on the three `[data-dl]` buttons to the new
   filename — same no-JS fallback reasoning as step 2.
4. **Attach the installer to the release without renaming it.** The site's
   download URL is built as `YapTr-<version>-setup.exe`; any other asset name
   404s every download button (§4d).
5. After publishing, click the hero button once and confirm a download starts.

**Regenerating derived assets**

- **Social card:** edit `tools/og-card.html`, then re-run the headless-Edge
  command in its header comment. Output must stay 1200×630.
- **Mascot:** re-extract from the app's `packaging/jpen.ico` (§2). Never edit
  the PNGs by hand.

**Conventions**
- Keep everything in `index.html`. Don't split CSS/JS into separate files until
  there's a second page that shares them.
- Match the surrounding style: CSS custom properties for anything reused, plain
  ES5-compatible JS in one IIFE, no libraries.
- Every animation needs a `prefers-reduced-motion` answer.
- Every interactive element needs a visible `:focus-visible` state (§4b).
- **No third-party requests.** No CDNs, no hosted fonts, no analytics, no
  embeds. If something needs an external file, vendor it into `assets/`.
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
| Version drifts from the shipped installer | Single `RELEASE` constant + release checklist (§4c, §7) |
| Release asset renamed → every download 404s | Called out in §4d and step 4 of the release checklist |
| This repo flipped private → every download 404s | §4d hard dependency #2. Low risk: free Pages already requires it to be public |
| Closed source weakens the trust story | Accepted tradeoff (§0). Mitigated by publishing a SHA-256 and by the candour of §4's "Before you download" |
| "Open source" creeps back into the copy | §4e records exactly what was removed and why |
| Social URLs break on a domain move | Flagged in §4a — they hardcode the `github.io` origin |
| `PLAN.md` is public | Repo is public, so this file is world-readable. Nothing sensitive, but it does expose the roadmap and the placeholder/blocker list. Move it out if that stops being acceptable. |
