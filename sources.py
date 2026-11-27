# Every source the bot reads. "kind" sets the Discord label/color.
# Optional "include" is a regex the title must match (used to keep only
# trailers from channels that also post clips, shorts and streams).
# The bot covers competitive games only: general sources (news, culture, general
# trailers, deals) are marked competitive_only in RSS_FEEDS, so only their stories
# that name a competitive game get through.

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
    {"name": "Dexerto", "url": "https://www.dexerto.com/gaming/feed/"},
    {"name": "GameRant", "url": "https://gamerant.com/feed/"},
]

# Titles naming one of these turn a news/culture story into "Competitive", so creator
# drama, trends and viral stories about these games get flagged wherever they appear.
COMPETITIVE_GAMES = (
    r"(?i)\b(counter-strike|cs2|cs:go|csgo|valorant|vct|league of legends|lck|lec|lpl|"
    r"dota|the international|rainbow six|r6|overwatch|apex legends|call of duty|cod|warzone|"
    r"black ops|modern warfare|marvel rivals|fortnite|rocket league|rlcs|ea sports fc|ea fc|"
    r"fc ?2\d|ultimate team|pubg|battlegrounds|mobile legends|mlbb|free fire|honor of kings|"
    r"street fighter|tekken|deadlock|the finals|esports?|e-sports|esports world cup|ewc|"
    r"wild rift|brawl stars|clash royale|mortal kombat|smash bros|guilty gear|fatal fury|2xko|"
    r"delta force|arena breakout|halo|splitgate|smite|"
    r"blast (premier|slam|open|bounty)|iem|pgl|esl|riot games|faker|t1|fnatic|team liquid|"
    r"team falcons|team vitality|natus vincere|g2 esports)\b"
)

# official game news (patch notes, events) straight from Steam
STEAM_GAMES = [
    ("Counter-Strike 2", 730), ("Dota 2", 570), ("Rainbow Six Siege", 359550),
    ("Apex Legends", 1172470), ("PUBG", 578080), ("Marvel Rivals", 2767030),
    ("Overwatch 2", 2357570), ("Deadlock", 1422450), ("The Finals", 2073850),
    ("Rocket League", 252950), ("Street Fighter 6", 1364780), ("Tekken 8", 1778820),
]

COMPETITIVE = [
    {"name": n, "url": f"https://store.steampowered.com/feeds/news/app/{app_id}/"}
    for n, app_id in STEAM_GAMES
] + [
    # mobile coverage is mostly guides; keep only stories about competitive titles
    {"name": "Pocket Gamer", "url": "https://www.pocketgamer.com/rss/", "competitive_only": True},
    {"name": "Talkesport", "url": "https://www.talkesport.com/feed/", "competitive_only": True},
]

COMPETITIVE_TRAILER_WORDS = (
    TRAILER_ONLY + r"|agent|champion|hero|operator|cinematic|battle pass|act \d|episode|"
    r"new map|dev update|patch notes"
)

ESPORTS = [
    {"name": "Dust2.us", "url": "https://www.dust2.us/rss"},
    {"name": "VLR.gg", "url": "https://www.vlr.gg/rss"},
    {"name": "Hotspawn", "url": "https://www.hotspawn.com/feed"},
    {"name": "Esports News UK", "url": "https://esports-news.co.uk/feed/"},
    {"name": "Esports Insider", "url": "https://esportsinsider.com/feed"},
    {"name": "Esports Advocate", "url": "https://esportsadvocate.net/feed/"},
    {"name": "Esports.gg", "url": "https://esports.gg/feed/"},
    # these two mix in general gaming news, so keep only their competitive stories
    {"name": "Fragster", "url": "https://www.fragster.com/feed/", "competitive_only": True},
    {"name": "ESTNN", "url": "https://estnn.com/feed/", "competitive_only": True},
    {"name": "GINX", "url": "https://www.ginx.tv/en/rss"},
    {"name": "Strafe", "url": "https://www.strafe.com/news/rss/"},
]

GENERAL_TRAILERS = [
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

COMPETITIVE_TRAILERS = [
    # official competitive game channels: trailers, patches and new heroes/agents only
    yt("VALORANT", "UC8CX0LD98EDXl4UYX1MDCXg", COMPETITIVE_TRAILER_WORDS),
    yt("League of Legends", "UC2t5bjwHdUX4vM2g8TRDq5g", COMPETITIVE_TRAILER_WORDS),
    yt("Dota 2", "UCTQKT5QqO3h7y32G8VzuySQ", COMPETITIVE_TRAILER_WORDS),
    yt("Apex Legends", "UC0ZV6M2THA81QT9hrVWJG3A", COMPETITIVE_TRAILER_WORDS),
    yt("Call of Duty", "UC9YydG57epLqxA9cTzZXSeQ", COMPETITIVE_TRAILER_WORDS),
    yt("Overwatch", "UClOf1XXinvZsy4wKPAkro2A", COMPETITIVE_TRAILER_WORDS),
    yt("Marvel Rivals", "UCWzmOSSiSPbVnVu3ZAyDx2w", COMPETITIVE_TRAILER_WORDS),
    yt("PUBG MOBILE", "UCKuBf7CRNf4OYoDyTtAL5fg", COMPETITIVE_TRAILER_WORDS),
    yt("Free Fire", "UC7qTEluetD2pDB7lUBBlKuw", COMPETITIVE_TRAILER_WORDS),
    yt("Honor of Kings", "UCAWqx9F2mfnF5VHtUaQjUCg", COMPETITIVE_TRAILER_WORDS),
    yt("Rocket League", "UCBjQwd62OJgixzW49TKGERg", COMPETITIVE_TRAILER_WORDS),
    yt("EA SPORTS FC", "UCoyaxd5LQSuP4ChkxK0pnZQ", COMPETITIVE_TRAILER_WORDS),
    yt("Street Fighter", "UCVg9nCmmfIyP4QcGOnZZ9Qg", COMPETITIVE_TRAILER_WORDS),
]

DEALS_RSS = [
    {"name": "GG.deals", "url": "https://gg.deals/news/feed/"},
    {"name": "Indie Game Bundles", "url": "https://www.indiegamebundles.com/feed/"},
]

RSS_FEEDS = (
    [dict(f, kind="news", competitive_only=True) for f in NEWS]
    + [dict(f, kind="culture", competitive_only=True) for f in CULTURE]
    + [dict(f, kind="competitive") for f in COMPETITIVE]
    + [dict(f, kind="esports") for f in ESPORTS]
    + [dict(f, kind="trailer", competitive_only=True) for f in GENERAL_TRAILERS]
    + [dict(f, kind="trailer") for f in COMPETITIVE_TRAILERS]
    + [dict(f, kind="deal", competitive_only=True) for f in DEALS_RSS]
)

# free games: GamerPower covers Epic, Steam, GOG, Prime Gaming, mobile, etc.
GAMERPOWER_URL = "https://www.gamerpower.com/api/giveaways?type=game&sort-by=date"
