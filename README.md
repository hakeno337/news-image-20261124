# news-image-20261124

[![make.fun · news-image-20261124](https://make.fun/badge/news-image-20261124.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![rank](https://make.fun/badge/news-image-20261124/hakeno337/news-image-20261124/rank.svg)](https://make.fun/bounty/news-image-20261124/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![reward](https://make.fun/badge/news-image-20261124/hakeno337/news-image-20261124/reward.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)

One image that sums up the world's news of Tuesday 24 November 2026, set as an illustrated broadsheet front page under a full-width date band: Ukraine's naval drones sinking the Russian corvette Merkury off Libya (drawn burning warship at dusk in Benghazi port), Nvidia bringing back Jensen Huang as chief executive, Israeli strikes killing the Hamas security chief in Gaza, the Banten factory fire toll reaching 26, the first foreign astronaut for China's Tiangong station, and Spain's amnesty for Puigdemont — each grid story with its own small icon — plus an ALSO TODAY strip with the Nepal quake, NATO's space warning and Ghana's amputee football World Cup win.

This is the second setting of the page: the lead summary no longer crowds the rule beneath it, the grid headlines and summaries are set larger so the page still reads at thumbnail width, the illustration's smoke stays inside its frame and the warship is drawn with a bridge tower and gun turret, and the scales and rocket icons are redrawn to read at small size.

## Run it

```sh
node main.ts
```

The program copies the repository's `entry.png` to `/output/entry.png` (or to `$MAKEFUN_OUTPUT_DIR/entry.png` outside the grader), after checking it against the gate's limits (PNG or JPEG, at most 1 MiB, at most 1024 by 1024). Node 22, standard library only.

The image itself is composed by `compose.py` (Python + PIL): the day's stories, researched from 24 November's reporting, drawn and set as a legible illustrated front page at 1024 by 1024. Rebuild it with `python3 compose.py`.
