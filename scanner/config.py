import os

TELEGRAM_BOT_TOKEN = os.environ.get("STACKUP_TELEGRAM_TOKEN", "")
TELEGRAM_CHAT_ID = os.environ.get("STACKUP_TELEGRAM_CHAT_ID", "")

DB_PATH = os.path.join(os.path.dirname(__file__), "stackup.db")

SCAN_INTERVAL_MINUTES = 30

GUMTREE_SEARCHES = [
    {
        "name": "solar_inverter_urgent",
        "url": "https://www.gumtree.co.za/s-generators-solar-power/v1c9751p1",
        "keywords": ["urgent", "must go", "make an offer", "emigrating", "moving"],
        "category": "solar_flip",
    },
    {
        "name": "power_tools_urgent",
        "url": "https://www.gumtree.co.za/s-power-tools/v1c9307p1",
        "keywords": ["urgent", "must go", "make an offer", "bargain", "clearance"],
        "category": "tool_flip",
    },
    {
        "name": "construction_equipment",
        "url": "https://www.gumtree.co.za/s-construction+equipment/v1q0p1",
        "keywords": ["urgent", "must go", "cheap", "clearance", "make an offer"],
        "category": "equipment_flip",
    },
    {
        "name": "generators",
        "url": "https://www.gumtree.co.za/s-generators-solar-power/v1c9751p1",
        "keywords": ["generator", "urgent", "must go"],
        "category": "generator_flip",
    },
    {
        "name": "water_tanks",
        "url": "https://www.gumtree.co.za/s-water+tank/v1q0p1",
        "keywords": ["jojo", "water tank", "urgent", "delivery"],
        "category": "water_crisis",
    },
    {
        "name": "bakkies_cheap",
        "url": "https://www.gumtree.co.za/s-cars-bakkies/v1c9077p1?pr=o,150000",
        "keywords": ["bakkie", "hilux", "ranger", "np200", "urgent"],
        "category": "vehicle_flip",
    },
]

TENDER_SOURCES = [
    {
        "name": "etenders",
        "url": "https://www.etenders.gov.za/Home/opportunities?id=1",
        "category": "government_tender",
    },
]

AUCTION_SOURCES = [
    {
        "name": "sa_auction_group",
        "url": "https://www.saauctiongroup.co.za/",
        "category": "auction",
    },
    {
        "name": "auction_operation",
        "url": "https://www.auctionoperation.co.za/auction_calendar.aspx",
        "category": "auction",
    },
]

NEWS_FEEDS = [
    {
        "name": "dailymaverick",
        "url": "https://www.dailymaverick.co.za/feed/",
        "keywords": ["water crisis", "joburg water", "diesel shortage", "loadshedding",
                      "eskom", "tender", "infrastructure", "construction",
                      "B-BBEE", "POPIA", "liquidation", "auction"],
        "category": "news_opportunity",
    },
    {
        "name": "businesstech",
        "url": "https://businesstech.co.za/news/feed/",
        "keywords": ["tender", "construction", "solar", "eskom", "water crisis",
                      "hiring", "skills shortage", "fuel", "diesel",
                      "B-BBEE", "POPIA", "liquidation"],
        "category": "news_opportunity",
    },
    {
        "name": "moneyweb",
        "url": "https://www.moneyweb.co.za/feed/",
        "keywords": ["tender", "construction", "solar", "eskom", "water",
                      "shortage", "opportunity", "small business", "SMME"],
        "category": "news_opportunity",
    },
]
