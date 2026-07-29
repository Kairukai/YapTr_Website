#!/usr/bin/env python3
"""Bake the real installer download count into index.html.

Run by .github/workflows/download-count.yml on a schedule.

WHY BAKE IT IN rather than fetch from the browser:
  * A client-side call to api.github.com would be a third-party request on every
    page load. The site deliberately makes none (fonts are self-hosted for the
    same reason) -- see PLAN.md section 3.
  * It would hand every visitor's IP to GitHub before they chose to go there.
  * Unauthenticated API calls are limited to 60/hour per IP, so anyone on a
    shared or carrier-grade-NAT address would see it fail.

Baking it in at build time keeps the page fully static and truthful.

HONESTY NOTES (these matter -- the whole site is built on not overstating):
  * GitHub counts every asset download, including repeats, bots and mirrors.
    It is an upper bound on real people, never an exact user count.
  * The count is NOT real-time. It lags by hours. A weekly schedule is well
    inside that tolerance; anything pretending to be live would be a lie.
  * Deleting and re-creating a release resets the counter to zero. Don't.
"""

from __future__ import annotations

import json
import os
import re
import sys
import urllib.error
import urllib.request

REPO = os.environ.get("COUNT_REPO", "Kairukai/YapTr_Website")

# Counts below this stay hidden. Currently 0, i.e. always visible -- the owner
# wants the real number shown from the start.
#
# The mechanism is kept rather than deleted because the argument for it still
# holds if this ever goes live with a small number: "7 downloads" tells a
# visitor nobody uses this, which is worse than saying nothing on a page already
# asking them to trust an unsigned installer. Raise it to bring the gate back.
THRESHOLD = int(os.environ.get("COUNT_THRESHOLD", "0"))

HTML = os.environ.get("COUNT_HTML", "index.html")

START, END = "<!--DL_COUNT-->", "<!--/DL_COUNT-->"


def fetch_total(repo: str) -> int:
    """Sum download_count across every .exe asset in every release."""
    req = urllib.request.Request(
        f"https://api.github.com/repos/{repo}/releases?per_page=100",
        headers={
            "Accept": "application/vnd.github+json",
            "User-Agent": "yaptr-download-counter",
        },
    )
    token = os.environ.get("GH_TOKEN")
    if token:
        req.add_header("Authorization", f"Bearer {token}")

    with urllib.request.urlopen(req, timeout=30) as resp:
        releases = json.load(resp)

    total = 0
    for rel in releases:
        for asset in rel.get("assets", []):
            # Skip GitHub's auto-attached source archives; they aren't the app.
            if asset.get("name", "").lower().endswith(".exe"):
                total += int(asset.get("download_count", 0))
    return total


def patch(html: str, total: int) -> str:
    """Write the number between the markers and toggle the `hidden` attribute."""
    if START not in html or END not in html:
        raise SystemExit(f"markers {START}/{END} not found in {HTML}")

    html = re.sub(
        re.escape(START) + r".*?" + re.escape(END),
        f"{START}{total:,}{END}",
        html,
        flags=re.S,
    )

    # Show or hide server-side rather than with JavaScript, so the decision
    # holds for crawlers and for anyone with JS disabled.
    if total >= THRESHOLD:
        html = html.replace('<p class="dl-count" hidden>', '<p class="dl-count">')
    else:
        html = html.replace('<p class="dl-count">', '<p class="dl-count" hidden>')

    return html


def main() -> int:
    try:
        total = fetch_total(REPO)
    except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError) as exc:
        # Never fail the build over a flaky API call -- leave the page as-is.
        print(f"could not reach the GitHub API ({exc}); leaving index.html untouched")
        return 0

    with open(HTML, encoding="utf-8") as fh:
        original = fh.read()

    updated = patch(original, total)

    state = "visible" if total >= THRESHOLD else f"hidden (below {THRESHOLD})"
    if updated == original:
        print(f"total={total:,} - no change needed ({state})")
        return 0

    with open(HTML, "w", encoding="utf-8", newline="") as fh:
        fh.write(updated)
    print(f"total={total:,} - index.html updated, counter {state}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
