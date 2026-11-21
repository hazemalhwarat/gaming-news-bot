# Every source the bot reads. "kind" sets the Discord label/color.
# Optional "include" is a regex the title must match (used to keep only
# trailers from channels that also post clips, shorts and streams).

TRAILER_ONLY = (
    r"(?i)trailer|teaser|reveal|gameplay|launch|announce|release date|overview|"
    r"showcase|direct|update|patch|season|expansion|dlc|early access|demo|first look"
)


def yt(name, channel_id, include=TRAILER_ONLY):
    return {
        "name": name,
        "url": f"https://www.youtube.com/feeds/videos.xml?channel_id={channel_id}",
        "include": include,
    }


NEWS = [
    {"name": "IGN", "url": "https://feeds.ign.com/ign/games-all"},
    {"name": "GameSpot", "url": "https://www.gamespot.com/feeds/mashup/"},
    {"name": "PC Gamer", "url": "https://www.pcgamer.com/rss/"},
    {"name": "Eurogamer", "url": "https://www.eurogamer.net/feed"},
    {"name": "Kotaku", "url": "https://kotaku.com/rss"},
    {"name": "The Verge Games", "url": "https://www.theverge.com/rss/games/index.xml"},
    {"name": "Game Informer", "url": "https://gameinformer.com/rss.xml"},
    {"name": "Video Games Chronicle", "url": "https://www.videogameschronicle.com/feed/"},
    {"name": "Insider Gaming", "url": "https://insider-gaming.com/feed/"},
    {"name": "Rock Paper Shotgun", "url": "https://www.rockpapershotgun.com/feed"},
    {"name": "PCGamesN", "url": "https://www.pcgamesn.com/rss.xml"},
    {"name": "GamesRadar", "url": "https://www.gamesradar.com/rss/"},
    {"name": "VG247", "url": "https://www.vg247.com/feed"},
    {"name": "Destructoid", "url": "https://www.destructoid.com/feed/"},
    {"name": "TheGamer", "url": "https://www.thegamer.com/feed/"},
    {"name": "DualShockers", "url": "https://www.dualshockers.com/feed/"},
    {"name": "GamingBolt", "url": "https://gamingbolt.com/feed"},
    {"name": "Hardcore Gamer", "url": "https://hardcoregamer.com/feed/"},
    {"name": "Wccftech Gaming", "url": "https://wccftech.com/tag/gaming/feed/"},
    {"name": "Escapist Magazine", "url": "https://www.escapistmagazine.com/feed/"},
    {"name": "COGconnected", "url": "https://cogconnected.com/feed/"},
    {"name": "Niche Gamer", "url": "https://nichegamer.com/feed/"},
    {"name": "Noisy Pixel", "url": "https://noisypixel.net/feed/"},
    {"name": "Gematsu", "url": "https://www.gematsu.com/feed"},
    {"name": "Siliconera", "url": "https://www.siliconera.com/feed/"},
    {"name": "Automaton", "url": "https://automaton-media.com/en/feed/"},
    # platforms (official blogs first)
    {"name": "PlayStation Blog", "url": "https://blog.playstation.com/feed/"},
    {"name": "Xbox Wire", "url": "https://news.xbox.com/en-us/feed/"},
    {"name": "Nintendo Life", "url": "https://www.nintendolife.com/feeds/latest"},
    {"name": "Nintendo Everything", "url": "https://nintendoeverything.com/feed/"},
    {"name": "NintendoSoup", "url": "https://nintendosoup.com/feed/"},
    {"name": "Push Square", "url": "https://www.pushsquare.com/feeds/latest"},
    {"name": "Pure Xbox", "url": "https://www.purexbox.com/feeds/latest"},
    # industry
    {"name": "GamesIndustry.biz", "url": "https://www.gamesindustry.biz/feed"},
    {"name": "Game Developer", "url": "https://www.gamedeveloper.com/rss.xml"},
]

CULTURE = [
    {"name": "Dexerto", "url": "https://www.dexerto.com/feed/"},
    {"name": "GameRant", "url": "https://gamerant.com/feed/"},
]

ESPORTS = [
    {"name": "Dexerto Esports", "url": "https://www.dexerto.com/esports/feed/"},
    {"name": "Dust2.us", "url": "https://www.dust2.us/rss"},
    {"name": "VLR.gg", "url": "https://www.vlr.gg/rss"},
    {"name": "Hotspawn", "url": "https://www.hotspawn.com/feed"},
    {"name": "Esports News UK", "url": "https://esports-news.co.uk/feed/"},
    {"name": "Esports Insider", "url": "https://esportsinsider.com/feed"},
    {"name": "Esports Advocate", "url": "https://esportsadvocate.net/feed/"},
]

TRAILERS = [
    # these channels post almost only trailers, so no title filter
    yt("Gematsu", "UCcaswDIh-nrXYofcYQm6KTg", include=None),
    yt("PlayStation", "UC-2Y8dQb0S6DtpxNgAKoJKA", include=None),
    yt("Xbox", "UCjBp_7RuDBUYbd1LegWEJ8g", include=None),
    yt("Nintendo of America", "UCGIY_O-8vW4rfX98KlMkvRg", include=None),
    # mixed channels: trailers/updates only
    yt("IGN", "UCKy1dAqELo0zrOtPkf0eTMw"),
    yt("GameSpot", "UCbu2SsF-Or3Rsn3NxqODImw"),
    yt("Ubisoft", "UC0KU8F9jJqSLS11LRXvFWmg"),
    yt("Bandai Namco", "UC_ntXHv-XdKCD7CPynVvnQw"),
    yt("Capcom", "UCW7h-1mymnJ96akzjrmiIgA"),
    yt("Rockstar Games", "UC6VcWc1rAoWdBCM0JxrRQ3A"),
    yt("Square Enix", "UCA5SLTAVA6unn1M-6lbo1NA"),
    yt("Warner Bros. Games", "UCHqAOjD1bj-PvtPcK8qDFMQ"),
    yt("Bethesda", "UCvZHe-SP3xC7DdOk4Ri8QBw"),
    yt("Konami", "UCwkUBN7foWU9GcY5cFmso-Q"),
    yt("CD PROJEKT RED", "UCuCtanBJXOPAEIAUXf9944g"),
    yt("Blizzard", "UC3GriadTkHBnfgd2UFETGOA"),
    yt("Epic Games", "UC5Qk8mWBwtMyEj7iQQYRk1A"),
    yt("Steam", "UChmZ6QbxgHlmX3ISIHxIpQQ"),
    yt("The Game Awards", "UCqDS7KWjAPKv-7ZSlro9OiQ"),
]

DEALS_RSS = [
    {"name": "GG.deals", "url": "https://gg.deals/news/feed/"},
    {"name": "Indie Game Bundles", "url": "https://www.indiegamebundles.com/feed/"},
]

RSS_FEEDS = (
    [dict(f, kind="news") for f in NEWS]
    + [dict(f, kind="culture") for f in CULTURE]
    + [dict(f, kind="esports") for f in ESPORTS]
    + [dict(f, kind="trailer") for f in TRAILERS]
    + [dict(f, kind="deal") for f in DEALS_RSS]
)

# free games: GamerPower covers Epic, Steam, GOG, Prime Gaming, mobile, etc.
GAMERPOWER_URL = "https://www.gamerpower.com/api/giveaways?type=game&sort-by=date"
