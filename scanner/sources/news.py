import hashlib
import logging
import feedparser

log = logging.getLogger("stackup.news")


def scan(feed_config):
    url = feed_config["url"]
    keywords = [kw.lower() for kw in feed_config["keywords"]]
    category = feed_config["category"]
    name = feed_config["name"]

    items = []
    try:
        feed = feedparser.parse(url)

        for entry in feed.entries[:30]:
            title = entry.get("title", "")
            link = entry.get("link", "")
            summary = entry.get("summary", entry.get("description", ""))
            if hasattr(summary, "__len__") and len(summary) > 500:
                summary = summary[:500]

            text_lower = f"{title} {summary}".lower()
            if any(kw in text_lower for kw in keywords):
                item_id = hashlib.md5(f"{name}:{title}:{link}".encode()).hexdigest()
                items.append({
                    "id": item_id,
                    "source": f"news:{name}",
                    "category": category,
                    "title": title,
                    "url": link,
                    "price": "",
                    "description": summary,
                })

    except Exception as e:
        log.error(f"News scan failed for {name}: {e}")

    return items
