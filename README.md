# Gaming News Discord Bot

Posts every new gaming story to a Discord channel, checked every 15 minutes by GitHub Actions:

- **Gaming News**: IGN, GameSpot, PC Gamer, Eurogamer, Kotaku, Game Informer, VGC, Insider Gaming, PlayStation Blog, Xbox Wire, Nintendo Life and ~25 more
- **Trailers**: official YouTube channels (PlayStation, Xbox, Nintendo, Gematsu, Ubisoft, Capcom, Rockstar, ...), posted as playable videos
- **Free Games**: Epic, Steam, GOG, Prime Gaming and mobile giveaways (GamerPower)
- **Deals**: 75%+ off on games with Metacritic 80+ (CheapShark), plus bundles
- **Esports**: HLTV, VLR.gg, Dexerto Esports, Esports Insider and more

Only stories from the last 24 hours are posted, and the same story from two outlets is posted once.
Guides, puzzle answers, codes and film/TV coverage are filtered out.

## Setup

1. Repo → Settings → Secrets and variables → Actions → New repository secret:
   `DISCORD_WEBHOOK_URL` = the channel's webhook URL.
2. Actions tab → enable workflows. It then runs on its own every 15 minutes
   (GitHub may delay scheduled runs by a few minutes at busy times).
   "Run workflow" on the **gaming-news** workflow runs it immediately.

## Changing sources

Edit [sources.py](sources.py). YouTube channels use `yt("Name", "channel id")`.
`state/` holds what has already been posted; the workflow commits it after each run.
