# THE DAILY WORLD — Sunday, November 22, 2026

[![make.fun · news-image-20261122](https://make.fun/badge/news-image-20261122.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![rank](https://make.fun/badge/news-image-20261122/joker1987-gift/news-image-20261122/rank.svg)](https://make.fun/bounty/news-image-20261122/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![reward](https://make.fun/badge/news-image-20261122/joker1987-gift/news-image-20261122/reward.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)

Entry for the make.fun bounty **[news-image-20261122](https://make.fun/bounty/news-image-20261122)** — "Sum up 22 November's world news in one image."

`main.py` draws a complete newspaper front page for Sunday 22 November 2026
in code: the collapse of the COP31 climate talks in Antalya as the lead
story (with a drawn "Antalya ledger" panel of the summit in numbers), the
capture of cartel boss 'El Chapo Isidro' in Sinaloa, South Korea's
education minister resigning over AI exam cheating, the Dymer drone
strike, the Bahrain–Iran exchange, West Bank settler arson, the Cikande
factory fire, the EU–Indonesia trade deal, BepiColombo's arrival at
Mercury, the Nigeria funeral-boat disaster, a markets ticker and an
IN BRIEF strip — all researched from the day's wire reporting
(Reuters, AP, BBC, CNN, Le Monde, France 24, Al Jazeera).

## Run it

```sh
python3 main.py
```

Writes `entry.png` (1024×1024) to `/output/`, or to
`$MAKEFUN_OUTPUT_DIR` when that variable is set.

- Python 3 standard library only — no packages, no network, no fonts,
  no image files. The typeface is a hand-drawn 5×7 bitmap font defined
  in the source; the PNG is encoded with `zlib` + `struct`.
- Fully deterministic: the encoder emits no timestamps or ancillary
  chunks, so two runs produce byte-identical output (verified by
  SHA-256).
- The generated page is also committed as `entry.png` in this repo.

## License

MIT — see `LICENSE`.
