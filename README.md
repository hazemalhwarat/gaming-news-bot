# Competitive Gaming News Discord Bot

Posts every new story about competitive games to a Discord channel, checked every 15 minutes by GitHub Actions.

Covered games: CS2, Valorant, LoL, Dota 2, R6, Overwatch, Apex, Call of Duty, Marvel Rivals, Fortnite, Rocket League,
EA FC, PUBG / PUBG Mobile, Mobile Legends, Free Fire, Honor of Kings, Wild Rift, Brawl Stars, Street Fighter, Tekken,
Mortal Kombat and more, plus the big tournaments, orgs and players (see `COMPETITIVE_GAMES` in [sources.py](sources.py)).

- **Esports**: Dust2.us, VLR.gg, Hotspawn, Strafe, GINX, Esports.gg, Esports Insider and more
- **Competitive**: creator, trend and viral stories about those games from ~40 gaming sites (IGN, PC Gamer, Dexerto, ...),
  plus official Steam patch notes
- **Trailers**: official game channels (VALORANT, League of Legends, PUBG MOBILE, ...), posted as playable videos
- **Free games / deals**: only when they are for a competitive game

Anything that doesn't name a competitive game is skipped. Only stories from the last 24 hours are posted,
and the same story from two outlets is posted once. Guides, puzzle answers and code lists are filtered out.

## Setup

1. Repo → Settings → Secrets and variables → Actions → New repository secret:
   `DISCORD_WEBHOOK_URL` = the channel's webhook URL.
2. Actions tab → enable workflows. It then runs on its own every 15 minutes
   (GitHub can delay or skip scheduled runs, sometimes for hours; whatever was missed
   goes out on the next run).
   "Run workflow" on the **gaming-news** workflow runs it immediately.

## Changing sources

Edit [sources.py](sources.py). To cover another game, add its name to `COMPETITIVE_GAMES`.
YouTube channels use `yt("Name", "channel id")`.
`state/` holds what has already been posted; the workflow commits it after each run.
