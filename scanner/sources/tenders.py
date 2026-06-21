import hashlib
import logging
import requests
from bs4 import BeautifulSoup

log = logging.getLogger("stackup.tenders")

HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
}

INTERESTING_KEYWORDS = [
    "water", "sanitation", "construction", "building", "road",
    "maintenance", "cleaning", "security", "transport", "delivery",
    "supply", "equipment", "solar", "energy", "electrical",
    "plumbing", "fencing", "painting", "landscaping", "waste",
    "rubble", "clearing", "demolition",
]


def scan(source_config):
    url = source_config["url"]
    category = source_config["category"]
    name = source_config["name"]

    items = []
    try:
        resp = requests.get(url, headers=HEADERS, timeout=30)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "lxml")

        rows = soup.select("table tr, .tender-item, [class*='tender'], [class*='opportunity']")

        for row in rows[:50]:
            text = row.get_text(strip=True)
            if len(text) < 10:
                continue

            text_lower = text.lower()
            if not any(kw in text_lower for kw in INTERESTING_KEYWORDS):
                continue

            link_el = row.select_one("a")
            href = ""
            title = text[:200]
            if link_el:
                title = link_el.get_text(strip=True) or title
                raw_href = link_el.get("href", "")
                href = raw_href if raw_href.startswith("http") else f"https://www.etenders.gov.za{raw_href}"

            item_id = hashlib.md5(f"{name}:{title}".encode()).hexdigest()
            items.append({
                "id": item_id,
                "source": f"tender:{name}",
                "category": category,
                "title": title[:200],
                "url": href,
                "price": "",
                "description": text[:500],
            })

    except Exception as e:
        log.error(f"Tender scan failed for {name}: {e}")

    return items
