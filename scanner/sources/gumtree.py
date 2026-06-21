import hashlib
import logging
import requests
from bs4 import BeautifulSoup

log = logging.getLogger("stackup.gumtree")

HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept-Language": "en-ZA,en;q=0.9",
}


def scan(search_config):
    url = search_config["url"]
    keywords = [kw.lower() for kw in search_config["keywords"]]
    category = search_config["category"]
    name = search_config["name"]

    items = []
    try:
        resp = requests.get(url, headers=HEADERS, timeout=30)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "lxml")

        listings = soup.select("a.related-ad-card") or soup.select("div.result") or soup.select("article")
        if not listings:
            listings = soup.select("[class*='listing']") or soup.select("[class*='result']")

        for listing in listings[:50]:
            title_el = listing.select_one("h2, h3, [class*='title'], [class*='name']")
            price_el = listing.select_one("[class*='price'], [class*='amount']")
            link_el = listing if listing.name == "a" else listing.select_one("a")
            desc_el = listing.select_one("[class*='description'], p")

            if not title_el:
                continue

            title = title_el.get_text(strip=True)
            price = price_el.get_text(strip=True) if price_el else ""
            link = ""
            if link_el and link_el.get("href"):
                href = link_el["href"]
                link = href if href.startswith("http") else f"https://www.gumtree.co.za{href}"
            description = desc_el.get_text(strip=True) if desc_el else ""

            text_lower = f"{title} {description}".lower()
            if any(kw in text_lower for kw in keywords):
                item_id = hashlib.md5(f"{name}:{title}:{price}".encode()).hexdigest()
                items.append({
                    "id": item_id,
                    "source": f"gumtree:{name}",
                    "category": category,
                    "title": title,
                    "url": link,
                    "price": price,
                    "description": description[:500],
                })

    except Exception as e:
        log.error(f"Gumtree scan failed for {name}: {e}")

    return items
