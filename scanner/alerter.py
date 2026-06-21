import requests
import logging
from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID

log = logging.getLogger("stackup.alerter")


def send_telegram(message):
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        log.warning("Telegram not configured — printing to console instead")
        print(f"\n{'='*60}\nALERT: {message}\n{'='*60}\n")
        return False

    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    try:
        resp = requests.post(url, json={
            "chat_id": TELEGRAM_CHAT_ID,
            "text": message,
            "parse_mode": "Markdown",
            "disable_web_page_preview": True,
        }, timeout=10)
        if resp.status_code == 200:
            return True
        log.error(f"Telegram API error: {resp.status_code} {resp.text}")
        return False
    except Exception as e:
        log.error(f"Telegram send failed: {e}")
        return False


def format_deal_alert(item):
    chain_map = {
        "solar_flip": "SOLAR DUMP",
        "tool_flip": "TOOL FLIP",
        "equipment_flip": "EQUIPMENT",
        "generator_flip": "GENERATOR",
        "water_crisis": "WATER CRISIS",
        "vehicle_flip": "VEHICLE",
        "government_tender": "TENDER",
        "auction": "AUCTION",
        "news_opportunity": "NEWS",
    }
    tag = chain_map.get(item["category"], item["category"].upper())
    price_str = f" | *{item['price']}*" if item.get("price") else ""

    return (
        f"🔥 *[{tag}]* {item['title']}\n"
        f"{price_str}\n"
        f"_{item.get('description', '')[:200]}_\n"
        f"{item.get('url', '')}"
    )


def format_news_alert(item):
    return (
        f"📰 *[MARKET SIGNAL]* {item['title']}\n"
        f"_{item.get('description', '')[:300]}_\n"
        f"{item.get('url', '')}"
    )


def alert_item(item):
    if item["category"] == "news_opportunity":
        msg = format_news_alert(item)
    else:
        msg = format_deal_alert(item)
    return send_telegram(msg)
