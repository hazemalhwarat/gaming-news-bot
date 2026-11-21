"""One pass: fetch every source, post whatever is new to Discord, save state.

Runs on a schedule in GitHub Actions; state lives in state/*.json and is
committed back to the repo after each run.
"""

import difflib
import json
import logging
import os
import re
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

import feedparser
import requests

import sources

WEBHOOK_URL = os.environ.get("DISCORD_WEBHOOK_URL", "")
DRY_RUN = os.environ.get("DRY_RUN") == "1"
MAX_AGE_HOURS = int(os.getenv("MAX_AGE_HOURS", "24"))
# safety valve after an outage so the channel doesn't get hundreds of posts at once
MAX_POSTS_PER_RUN = int(os.getenv("MAX_POSTS_PER_RUN", "40"))
TITLE_DEDUPE_HOURS = 72
TITLE_SIMILARITY = 0.82
SEEN_KEEP_DAYS = 10

STATE_DIR = Path(__file__).parent / "state"
SEEN_FILE = STATE_DIR / "seen.json"
TITLES_FILE = STATE_DIR / "posted_titles.json"

KINDS = {
    "news": ("Gaming News", 0x5865F2),
    "culture": ("Gaming Culture", 0xEB459E),
    "esports": ("Esports", 0x32C9E5),
    "trailer": ("Trailer", 0xED4245),
    "free": ("Free Game", 0x57F287),
    "deal": ("Deal", 0xFEE75C),
}

# guides, puzzle answers and code lists flood some feeds but aren't news
JUNK_TITLE = re.compile(
    r"(?i)^how to |\bguide\b|walkthrough|tier list|\bhints?\b|answers? (for|to)\b|"
    r"\bwordle\b|\bconnections\b|\bcontexto\b|\bstrands\b|\bcrossword\b|"
    r"\bcodes\b.*\(|redeem codes|all .* locations|best .* builds?\b"
)

# RSS category tags: these always mean "not news" ...
BLOCK_TAGS = {
    "guides", "tips & guides", "codes", "sponsored", "deals",
    "gamerant games", "gamerant daily crossword", "gamerant daily crossword mini",
    "name that game", "wordle",
}
# ... and these mean film/TV/food/etc. unless the post is also tagged as a game
OFF_TOPIC_TAGS = {
    "entertainment", "movies", "tv", "food", "anime", "manga", "books", "comic strip",
    "comedy", "animation", "what to watch", "new to streaming", "streaming",
}
GAME_TAGS = {
    "games", "gaming", "pc gaming", "pc", "platform", "playstation 5", "ps5",
    "xbox series x", "nintendo switch", "nintendo switch 2", "mobile",
}

IMG_TAG_RE = re.compile(r'<img[^>]+src="([^"]+)"')
HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; gaming-news-discord-bot/2.0)"}

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger("gaming-news-bot")


def load_json(path: Path) -> dict:
    return json.loads(path.read_text()) if path.exists() else {}


def save_json(path: Path, data: dict) -> None:
    path.parent.mkdir(exist_ok=True)
    path.write_text(json.dumps(data, separators=(",", ":"), ensure_ascii=False))


def normalize_title(title: str) -> str:
    text = re.sub(r"[^a-z0-9\s]", " ", title.lower())
    return re.sub(r"\s+", " ", text).strip()


def is_similar(norm: str, others) -> bool:
    return any(difflib.SequenceMatcher(None, norm, o).ratio() >= TITLE_SIMILARITY for o in others)


def clean_text(html: str, limit: int = 240) -> str:
    text = re.sub(r"<[^>]+>", " ", html or "")
    text = re.sub(r"\s+", " ", text).strip()
    if len(text) > limit:
        text = text[:limit].rsplit(" ", 1)[0] + "..."
    return text


def entry_timestamp(entry) -> Optional[float]:
    for key in ("published_parsed", "updated_parsed"):
        parsed = entry.get(key)
        if parsed:
            return datetime(*parsed[:6], tzinfo=timezone.utc).timestamp()
    return None


def entry_image(entry) -> Optional[str]:
    for key in ("media_thumbnail", "media_content"):
        media = entry.get(key)
        if media and media[0].get("url"):
            return media[0]["url"]
    for enc in entry.get("enclosures", []):
        if enc.get("type", "").startswith("image") and enc.get("href"):
            return enc["href"]
    match = IMG_TAG_RE.search(entry.get("summary", "") or "")
    return match.group(1) if match else None


def is_gaming_news(title: str, entry) -> bool:
    if JUNK_TITLE.search(title):
        return False
    tags = {(t.get("term") or "").strip().lower() for t in entry.get("tags", [])}
    if tags & BLOCK_TAGS:
        return False
    if tags & OFF_TOPIC_TAGS and not tags & GAME_TAGS:
        return False
    return True


def get(url: str):
    resp = requests.get(url, headers=HEADERS, timeout=20)
    resp.raise_for_status()
    return resp


def fetch_rss(feed: dict) -> list[dict]:
    parsed = feedparser.parse(get(feed["url"]).content)
    include = re.compile(feed["include"]) if feed.get("include") else None
    items = []
    for e in parsed.entries:
        title = (e.get("title") or "").strip()
        link = e.get("link")
        ts = entry_timestamp(e)
        if not title or not link or ts is None:
            continue
        if include and not include.search(title):
            continue
        if feed["kind"] in ("news", "culture") and not is_gaming_news(title, e):
            continue
        items.append({
            "id": e.get("id") or link,
            "kind": feed["kind"],
            "source": feed["name"],
            "title": title,
            "link": link,
            "summary": "" if feed["kind"] == "trailer" else clean_text(e.get("summary")),
            "image": entry_image(e),
            "ts": ts,
        })
    return items


def fetch_free_games() -> list[dict]:
    items = []
    for g in get(sources.GAMERPOWER_URL).json():
        ts = datetime.strptime(g["published_date"], "%Y-%m-%d %H:%M:%S").replace(tzinfo=timezone.utc).timestamp()
        title = re.sub(r"\s*Giveaway\s*$", "", g["title"])
        bits = []
        if g.get("worth") and g["worth"] != "N/A":
            bits.append(f"~~{g['worth']}~~ **FREE**")
        bits.append(g.get("platforms", ""))
        if g.get("end_date") and g["end_date"] != "N/A":
            bits.append("ends " + g["end_date"][:10])
        items.append({
            "id": f"free:{g['id']}",
            "kind": "free",
            "source": "GamerPower",
            "title": title,
            "link": g.get("open_giveaway_url") or g.get("gamerpower_url"),
            "summary": " · ".join(b for b in bits if b),
            "image": g.get("image"),
            "ts": ts,
        })
    return items


def fetch_deals() -> list[dict]:
    try:
        stores = {s["storeID"]: s["storeName"] for s in get(sources.CHEAPSHARK_STORES_URL).json()}
    except Exception:
        stores = sources.STORE_NAMES
    items = []
    for page in range(3):
        for d in get(sources.CHEAPSHARK_URL.format(page=page)).json():
            if float(d["savings"]) < sources.DEAL_MIN_SAVINGS or float(d["dealRating"]) < sources.DEAL_MIN_RATING:
                continue
            image = d.get("thumb")
            if d.get("steamAppID"):
                image = f"https://cdn.akamai.steamstatic.com/steam/apps/{d['steamAppID']}/header.jpg"
            items.append({
                # keyed by game, so the same game on sale in several stores posts once
                "id": f"deal:{d['gameID']}",
                "kind": "deal",
                "source": stores.get(d["storeID"], "Store"),
                "title": f"{d['title']} — ${d['salePrice']} ({float(d['savings']):.0f}% off)",
                "link": f"https://www.cheapshark.com/redirect?dealID={d['dealID']}",
                "summary": f"Was ${d['normalPrice']} · Metacritic {d['metacriticScore']}",
                "image": image,
                "ts": float(d["lastChange"]),
            })
    return items


def fetch_all() -> list[dict]:
    jobs = [(f["name"], lambda f=f: fetch_rss(f)) for f in sources.RSS_FEEDS]
    jobs += [("GamerPower", fetch_free_games), ("CheapShark", fetch_deals)]

    def run(job):
        name, fn = job
        try:
            return fn()
        except Exception as exc:
            log.warning("failed to fetch %s: %s", name, exc)
            return []

    with ThreadPoolExecutor(max_workers=16) as pool:
        results = list(pool.map(run, jobs))
    return [item for batch in results for item in batch]


def build_embed(item: dict) -> dict:
    label, color = KINDS[item["kind"]]
    embed = {
        "title": item["title"][:256],
        "url": item["link"],
        "color": color,
        "timestamp": datetime.fromtimestamp(item["ts"], tz=timezone.utc).isoformat(),
        "author": {"name": f"{item['source']} · {label}"[:256]},
    }
    if item["summary"]:
        embed["description"] = item["summary"][:4000]
    if item["image"]:
        embed["image"] = {"url": item["image"]}
    return embed


def send(payload: dict) -> bool:
    """Returns True if Discord accepted it, or rejected it for good (bad payload)."""
    if DRY_RUN:
        return True
    for _ in range(5):
        resp = requests.post(WEBHOOK_URL, json=payload, timeout=20)
        if resp.status_code == 429:
            time.sleep(float(resp.json().get("retry_after", 2)) + 0.5)
            continue
        if resp.status_code >= 500:
            time.sleep(3)
            continue
        if resp.status_code >= 400:
            log.warning("discord rejected a message (%s): %s", resp.status_code, resp.text[:200])
        time.sleep(1)  # stay well under the webhook rate limit
        return True
    return False


def post(items: list[dict]) -> list[dict]:
    """Posts items in order; returns the ones that went out (or were permanently rejected)."""
    done = []
    batch = []

    def flush():
        if batch and send({"embeds": [build_embed(i) for i in batch]}):
            done.extend(batch)
        batch.clear()

    for item in items:
        if item["kind"] == "trailer":
            # a bare YouTube link makes Discord show a playable video
            flush()
            if send({"content": f"**{item['source']} · Trailer**\n{item['link']}"}):
                done.append(item)
        else:
            batch.append(item)
            if len(batch) == 10:  # Discord's per-message embed limit
                flush()
    flush()
    return done


def main() -> None:
    if not WEBHOOK_URL and not DRY_RUN:
        sys.exit("DISCORD_WEBHOOK_URL is not set")

    now = time.time()
    seen = {k: v for k, v in load_json(SEEN_FILE).items() if v >= now - SEEN_KEEP_DAYS * 86400}
    titles = {k: v for k, v in load_json(TITLES_FILE).items() if v >= now - TITLE_DEDUPE_HOURS * 3600}
    first_run = not seen

    items = fetch_all()
    log.info("fetched %d items", len(items))

    fresh, ids = [], set()
    for item in items:
        if item["id"] in seen or item["id"] in ids:
            continue
        ids.add(item["id"])
        fresh.append(item)

    if first_run:
        # don't dump every feed's backlog into the channel on the very first run
        for item in fresh:
            seen[item["id"]] = now
        save_json(SEEN_FILE, seen)
        log.info("first run: remembered %d items, posted none", len(fresh))
        return

    cutoff = now - MAX_AGE_HOURS * 3600
    candidates = sorted((i for i in fresh if i["ts"] >= cutoff), key=lambda i: i["ts"])

    to_post, run_titles = [], []
    for item in candidates:
        norm = normalize_title(item["title"])
        if is_similar(norm, titles) or is_similar(norm, run_titles):
            seen[item["id"]] = now
            continue
        run_titles.append(norm)
        item["_norm"] = norm
        to_post.append(item)

    if len(to_post) > MAX_POSTS_PER_RUN:
        log.info("capping %d new items to the newest %d", len(to_post), MAX_POSTS_PER_RUN)
        for item in to_post[:-MAX_POSTS_PER_RUN]:
            seen[item["id"]] = now
        to_post = to_post[-MAX_POSTS_PER_RUN:]

    posted = post(to_post)
    for item in posted:
        seen[item["id"]] = now
        titles[item["_norm"]] = now
        log.info("posted [%s · %s] %s", item["source"], item["kind"], item["title"])

    # items too old to post never need re-checking
    for item in fresh:
        if item["ts"] < cutoff:
            seen[item["id"]] = now

    save_json(SEEN_FILE, seen)
    save_json(TITLES_FILE, titles)
    log.info("done: %d posted, %d new candidates", len(posted), len(candidates))


if __name__ == "__main__":
    main()
