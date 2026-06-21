import hashlib
import logging
import requests
from bs4 import BeautifulSoup

log = logging.getLogger("stackup.auctions")

HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
}


def scan(source_config):
    url = source_config["url"]
    category = source_config["category"]
    name = source_config["name"]

    items = []
    try:
        resp = requests.get(url, headers=HEADERS, timeout=30)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "lxml")

        auction_links = soup.select("a[href*='auction'], a[href*='Auction']")
        if not auction_links:
            auction_links = soup.select("a[href*='/event'], a[href*='/sale']")
        if not auction_links:
            auction_links = soup.select(".auction-card a, .event-card a, [class*='auction'] a")

        seen_titles = set()
        for link in auction_links[:30]:
            title = link.get_text(strip=True)
            if not title or len(title) < 5 or title in seen_titles:
                continue
            seen_titles.add(title)

            href = link.get("href", "")
            full_url = href if href.startswith("http") else f"{url.rstrip('/')}/{href.lstrip('/')}"

            item_id = hashlib.md5(f"{name}:{title}".encode()).hexdigest()
            items.append({
                "id": item_id,
                "source": f"auction:{name}",
                "category": category,
                "title": title,
                "url": full_url,
                "price": "",
                "description": f"Upcoming auction: {title}",
            })

    except Exception as e:
        log.error(f"Auction scan failed for {name}: {e}")

    return items
