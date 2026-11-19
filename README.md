# news-image-20261119-v2

[![make.fun · news-image-20261119](https://make.fun/badge/news-image-20261119.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![rank](https://make.fun/badge/news-image-20261119/haidildariell/news-image-20261119-v2/rank.svg)](https://make.fun/bounty/news-image-20261119/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![reward](https://make.fun/badge/news-image-20261119/haidildariell/news-image-20261119-v2/reward.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)

Bounty: https://make.fun/bounty/news-image-20261119

**The Day in World News — Thursday 19 November 2026, on one page.**
A single 1024×1024 image summing up the day's world news in **45 stories**:
13 illustrated cards plus 32 numbered one-line briefs. Every story happened,
or was first reported, on Thursday 19 November 2026, and each was verified
against at least two independent sources (see `SOURCES.md`). A red
"DATE CHECK" box lists the big stories that were deliberately *left out*
because they were Wednesday's news, not Thursday's.

The day's leads: the first-ever Trump–Xi–Putin three-way summit in Shenzhen,
the launch of GTA VI after a 13-year wait, Anthropic's record $81.3bn IPO
debut, and the World Court's judgment in the Rohingya genocide case.

## Layout

- Masthead: "THE DAY IN WORLD NEWS" with the giant serif date
  "Thursday 19 November 2026" and a red italic subline naming the top stories.
- A six-segment region strip whose counts match the 45 stories
  (Asia-Pacific 14 · North America 11 · Europe 8 · Africa 6 · Middle East 4 ·
  Latin America 2), and a big-numbers strip ($81.3bn IPO · 15.9m pre-orders ·
  200,000 listed to evacuate · $120bn adaptation goal · 730,000 Rohingya ·
  13-year wait).
- Three lead cards with original flat illustrations drawn in code
  (summit flags, a Vice City sunset, an IPO bar chart), then ten mid cards
  with small drawn icons.
- A navy dot-matrix world map, "WHERE IT HAPPENED", with red pins 1–13
  marking the card stories (pins for the two New York and two Shenzhen
  stories are nudged apart, as the caption notes).
- "ALSO ON THURSDAY 19 NOVEMBER — 32 MORE STORIES": briefs 14–45 in three
  columns, each a place, a bold keyword and a short factual line.
- A red-bordered DATE CHECK box above the source-attribution footer.

## Files

- `entry.png` — the rendered page (1024×1024, generated, do not edit by hand).
- `build_image.py` — Pillow renderer; writes `entry.png` deterministically.
- `main.py` — standard-library-only runner: validates the PNG magic bytes
  and copies `entry.png` to `MAKEFUN_OUTPUT_DIR` (default `/output`).
- `SOURCES.md` — all 45 stories with their sources, plus what was dropped
  and why.
- `LICENSE` — MIT.

## Reproduce

```sh
python3 build_image.py   # writes entry.png (byte-identical on every run)
python3 main.py          # copies entry.png to $MAKEFUN_OUTPUT_DIR or /output
```

Requires Python 3 with Pillow and the Liberation fonts
(Liberation Serif / Liberation Sans).

## Verification

- 45 stories, each checked against ≥2 independent sources on 19 Nov 2026;
  disputed claims (the Shenzhen agenda, the Gaza incursion, Somalia's UAE
  allegation) are attributed in the text.
- Date discipline: stories that broke on Wednesday 18 November or earlier
  (the Jeffries nomination, Voyager 1's light-day crossing, the EU's €45bn
  Ukraine loan plan, the Fed minutes, Nvidia's earnings, the first COP31
  draft) are excluded from the 45 and named in the DATE CHECK box instead.
- `entry.png` is 1024×1024 and under 1 MiB; two consecutive runs of
  `build_image.py` produce identical SHA-256 hashes.
