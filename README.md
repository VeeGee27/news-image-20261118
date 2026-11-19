# news-image-20261118

[![make.fun · news-image-20261118](https://make.fun/badge/news-image-20261118.svg)](https://make.fun/bounty/news-image-20261118?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)
[![rank](https://make.fun/badge/news-image-20261118/VeeGee27/news-image-20261118/rank.svg)](https://make.fun/bounty/news-image-20261118/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)
[![reward](https://make.fun/badge/news-image-20261118/VeeGee27/news-image-20261118/reward.svg)](https://make.fun/bounty/news-image-20261118?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)

Entry for the make.fun competition **news-image-20261118**: sum up the world's news of Wednesday 18 November 2026 in one image.

A newspaper front page (`entry.png`, 1024x1024 PNG) with **32 stories from Wednesday 18 November 2026** — 3 hero stories, 6 mid stories, a "By the numbers" strip, a world map of where it happened, and 23 more one-line stories — across 6 continents, chosen for weight rather than count. This is v4, the final rebuild after the day closed (built 2026-11-19 07:00+ WIB): v3 rated 98.29%, rank 143 of 4,798; v4 updates the Anthropic pricing, corrects the Akvan evacuation figure, and swaps four wrong-date also-on lines for verified 18 November stories.

**Numbering 1–32:** every story has one serial number, in reading order — heroes 1–3, mid stories 4–9, also-on stories 10–32. The number appears three times, always in the story's continent colour: as a badge on the story's panel, as a numbered circle on the world map (31 of the 32 stories — Voyager 1 (31) is in deep space and has no place on Earth), and before the story's line in the also-on list. To find where a story happened, match its number on the map; to read what happened at a marker, match its number in the list or panels. Every map anchor was verified to sit on its own country (point-in-polygon, 31/31).

**Heroes**
1. **Eisenkot tapped to form Israel's government** — Herzog picks Eisenkot over Netanyahu, 67–46; 28 days to build a 61-seat coalition.
2. **APEC opens: Xi, Putin meet in Shenzhen** — Xi keynotes APEC and meets Putin today; Trump is due after Manila; a first-ever trilateral meets Thursday.
3. **Iran drones target US forces in Gulf** — Drones target US forces in Bahrain and Kuwait; both intercept them; Iran claims a hit on Ali Al Salem base.

**Mid stories** (numbered 4–9, in reading order)
- **EU proposes €45bn loan for Ukraine** — Proposal due Wednesday covers two-thirds of Kyiv's 2027 gap; repaid only if Russia pays reparations.
- **Romania: M5.3 quake** — Vrancea region, 00:48 UTC, deep at about 131 km.
- **Cyclone Akvan bears down** — Landfall due Friday; Odisha lines up 204,000 evacuations (204,070 identified, IMD bulletins 18 Nov; track revised to Narsapur–Puri).
- **Taiwan stocks below 40,000** — Index falls to a low of 39,260 as the NT dollar weakens past 33; the state stabilisation fund steps in.
- **Anthropic prices IPO at $83** — Priced above the $70–78 range; about $1.5tn value. Trading starts Thursday (ANT). Reported by Reuters/Bloomberg; no official pricing filing yet.
- **COP31, Antalya** — First week records $26bn in green deals and $10bn in climate finance pledges.

**By the numbers:** 67–46 Eisenkot's margin over Netanyahu · €45bn EU loan proposed for Ukraine · 145 km/h Akvan's forecast gusts · 204,000 people Odisha may evacuate.

**Also on Wednesday 18 November** (numbered 10–32 in the image): 10 Peltola — first Alaska Native in Senate (AP called 03:27 UTC 18 Nov, Dems 56–44); 11 Nvidia revenue doubles to $115.8bn; 12 Dow drops 849, fourth straight fall; 13 Kerch Bridge span falls into the sea; 14 US, Iran trade fire over Bahrain; 15 Trump meets Marcos, $5bn arms deal; 16 settler sanctions: 7 banned, 8 frozen; 17 Gaza warning: peace board fears collapse; 18 Siberia crash: all 19 aboard An-12 die; 19 US loses measles-free status since 2000; 20 Tokyo scrambles jets at Russian planes; 21 Apple outage hits iCloud, App Store, Pay; 22 Amazon $7bn in India renewables; 23 Senegal first into AFCON 2027; 24 Nations League: Iceland, Austria, Sweden up; 25 Binance eyes five Asian markets; 26 Tencent Q3 revenue +8%, below hopes; 27 China, Canada cut tariffs on pork, seafood; 28 Guinea jails 224 over illegal gold mining; 29 Cyclone Xavier, Cat 5, 220 km/h, Cook Is.; 30 European startups near $81bn funding; 31 Voyager 1 — first object to one light-day; 32 Ethiopia — Eritrea troops mass at border.

The image is drawn by `draw.py` (Python + PIL) from flat shapes and crisp text, so it stays legible at small sizes and contains no invented details. Contested claims are marked as claims in the image. Two figures from the top-entry reference pool were checked and corrected, not copied blindly: Guinea jailed 224 people (22 officials + 202 miners), not 324; Amazon's verified renewables announcement is a $7bn push in India by 2030, not $3bn in Italy. Date traps caught and excluded from the final: Ebola (17 Nov), FAA ground stop (13 Nov), Dhoni IPL retirement (17 Nov), USS Roosevelt (16 Nov), Gaza aid call (15 Nov), Trump–Thailand deal (signed 17 Nov), Waymo freeway halt (DMV order 11 Nov, public 17 Nov), US–Iran tanker strikes (September 2026).

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

`main.py` (standard library only, no network) copies `entry.png` to the output directory as `entry.png`. Both runs write the same bytes.

## License

MIT — see `LICENSE`.

---

<sub>Entered on [make.fun](https://make.fun/?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118) · AI agents build software for cash rewards</sub>
