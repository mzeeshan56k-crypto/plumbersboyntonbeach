# content-queue

Holds blog posts that are written but not yet published.

Vercel only builds `main`, so nothing on this branch is deployed or
reachable. `scripts/publish_batch.py` on `main` moves one week's batch
from `queue/<slug>/` into `blog/<slug>/`, rebuilds the index and sitemap,
and commits.

`schedule.json` maps every slug to its publish week and date.
