#!/usr/bin/env python3
"""Fill the GITHUB_STATS window of assets/bento-bottom.svg with live GitHub data.

Rewrites only what sits between the marker comments in that file:

    <!-- stats:start --> ... <!-- stats:end -->   the four stat columns
    <!-- grid:start -->  ... <!-- grid:end -->    the contribution heatmap

then runs build-themes.py so assets/dark/ stays in sync. Run daily by
.github/workflows/update-stats.yml; you can also run it by hand.

Token lookup: $GITHUB_TOKEN, then $GH_TOKEN, then `gh auth token`.
The Actions token only sees public contributions; to count private commits,
add a personal access token as the repo secret STATS_TOKEN (the workflow
prefers it when present).

Usage:
    python3 scripts/build-stats.py
"""

import json
import os
import re
import subprocess
import sys
import urllib.request
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SVG = ROOT / "assets" / "bento-bottom.svg"
LOGIN = os.environ.get("STATS_USER", "MrPanda009")
WEEKS = 30  # columns that fit the window: 30 x 10px pitch = 298px
LEVELS = ["NONE", "FIRST_QUARTILE", "SECOND_QUARTILE", "THIRD_QUARTILE", "FOURTH_QUARTILE"]

# Stat column centres and baselines, in GITHUB_STATS window coordinates.
COLUMN_X = [53.25, 127.75, 202.25, 276.75]
VALUE_Y, LABEL_Y = 70, 84


def token():
    for var in ("GITHUB_TOKEN", "GH_TOKEN"):
        if os.environ.get(var):
            return os.environ[var]
    try:
        return subprocess.run(["gh", "auth", "token"], capture_output=True, text=True, check=True).stdout.strip()
    except (OSError, subprocess.CalledProcessError):
        sys.exit("No GitHub token: set GITHUB_TOKEN or log in with `gh auth login`.")


def graphql(query, tok):
    req = urllib.request.Request(
        "https://api.github.com/graphql",
        data=json.dumps({"query": query}).encode(),
        headers={"Authorization": f"bearer {tok}", "Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        body = json.load(resp)
    if body.get("errors"):
        sys.exit(f"GitHub API error: {body['errors']}")
    return body["data"]


def fetch(tok):
    data = graphql(f"""
    query {{
      user(login: "{LOGIN}") {{
        createdAt
        repositories(ownerAffiliations: OWNER, privacy: PUBLIC) {{ totalCount }}
        followers {{ totalCount }}
        following {{ totalCount }}
        contributionsCollection {{
          contributionCalendar {{
            weeks {{ contributionDays {{ contributionLevel date }} }}
          }}
        }}
      }}
    }}""", tok)["user"]

    # contributionsCollection spans at most a year, so sum all-time commits one year at a time.
    start = datetime.fromisoformat(data["createdAt"].replace("Z", "+00:00"))
    now = datetime.now(timezone.utc)
    windows = []
    while start < now:
        end = min(start + timedelta(days=365), now)
        windows.append((start, end))
        start = end
    fields = "\n".join(
        f'y{i}: contributionsCollection(from: "{a.isoformat()}", to: "{b.isoformat()}") {{ totalCommitContributions }}'
        for i, (a, b) in enumerate(windows)
    )
    years = graphql(f'query {{ user(login: "{LOGIN}") {{ {fields} }} }}', tok)["user"]
    commits = sum(v["totalCommitContributions"] for v in years.values())

    weeks = data["contributionsCollection"]["contributionCalendar"]["weeks"][-WEEKS:]
    return {
        "repos": data["repositories"]["totalCount"],
        "commits": commits,
        "followers": data["followers"]["totalCount"],
        "following": data["following"]["totalCount"],
        "weeks": [[LEVELS.index(d["contributionLevel"]) for d in w["contributionDays"]] for w in weeks],
        # The calendar can start mid-week, so the first column may hold fewer than 7 days.
        "first_week_offset": [datetime.fromisoformat(w["contributionDays"][0]["date"]).isoweekday() % 7 for w in weeks],
    }


def short(n):
    """28 -> '28', 1002 -> '1k+', 2350 -> '2.3k+', 3000 -> '3k'."""
    if n < 1000:
        return str(n)
    k = int(n / 100) / 10
    text = f"{k:g}k"
    return text + "+" if n > k * 1000 else text


def render_stats(s, indent):
    cols = [(short(s["repos"]), "Public Repos"), (short(s["commits"]), "Total Commits"),
            (short(s["followers"]), "Followers"), (short(s["following"]), "Following")]
    lines = []
    for x, (value, label) in zip(COLUMN_X, cols):
        lines.append(f'<text x="{x}" y="{VALUE_Y}" class="stat-value">{value}</text>')
        lines.append(f'<text x="{x}" y="{LABEL_Y}" class="stat-label">{label}</text>')
    return "\n".join(indent + line for line in lines)


def render_grid(s, indent):
    lines = []
    last = None
    for col, (week, offset) in enumerate(zip(s["weeks"], s["first_week_offset"])):
        for i, level in enumerate(week):
            row = offset + i
            lines.append(f'<use href="#cell-{level}" x="{col * 10}" y="{row * 10}" />')
            last = (col * 10, row * 10)
    if last:  # the final day in the calendar is today
        x, y = last
        lines.append(f'<rect x="{x - 1}" y="{y - 1}" width="10" height="10" fill="none" class="st-ink today" stroke-width="1.5" />')
    # Four cells per line keeps the file readable.
    rows = [" ".join(lines[i:i + 4]) for i in range(0, len(lines), 4)]
    return "\n".join(indent + r for r in rows)


def fill(src, name, body):
    pattern = re.compile(r"([ \t]*)<!-- %s:start -->\n.*?<!-- %s:end -->" % (name, name), re.S)
    m = pattern.search(src)
    if not m:
        sys.exit(f"{SVG.name}: missing <!-- {name}:start --> / <!-- {name}:end --> markers")
    indent = m.group(1)
    block = f"{indent}<!-- {name}:start -->\n{body}\n{indent}<!-- {name}:end -->"
    return src[: m.start()] + block + src[m.end():]


def main():
    stats = fetch(token())
    src = SVG.read_text(encoding="utf-8")
    m = re.search(r"([ \t]*)<!-- stats:start -->", src)
    g = re.search(r"([ \t]*)<!-- grid:start -->", src)
    out = fill(src, "stats", render_stats(stats, m.group(1) if m else ""))
    out = fill(out, "grid", render_grid(stats, g.group(1) if g else ""))
    if out != src:
        SVG.write_text(out, encoding="utf-8")
        print(f"updated {SVG.relative_to(ROOT)}: {stats['repos']} repos, {stats['commits']} commits, "
              f"{stats['followers']} followers, {stats['following']} following")
    else:
        print("stats unchanged")
    subprocess.run([sys.executable, str(ROOT / "scripts" / "build-themes.py")], check=True)


if __name__ == "__main__":
    main()
