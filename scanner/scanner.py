#!/usr/bin/env python3
"""
StackUp Opportunity Scanner
Runs continuously on VPS, scans marketplaces/tenders/auctions/news
and alerts via Telegram when actionable deals appear.
"""

import json
import os
import time
import logging
import schedule
from datetime import datetime

from config import (
    GUMTREE_SEARCHES, TENDER_SOURCES, AUCTION_SOURCES,
    NEWS_FEEDS, SCAN_INTERVAL_MINUTES,
)

CUSTOM_SEARCHES_FILE = os.path.join(os.path.dirname(__file__), "custom_searches.json")
from db import init_db, is_seen, save_item, mark_alerted, log_scan, get_stats
from alerter import alert_item, send_telegram
from sources import gumtree, news, auctions, tenders

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(name)s] %(levelname)s: %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("scanner.log"),
    ],
)
log = logging.getLogger("stackup")


def run_scan_group(scan_fn, configs, group_name):
    total_new = 0
    for config in configs:
        try:
            items = scan_fn(config)
            new_items = []
            for item in items:
                if not is_seen(item["id"]):
                    save_item(
                        item["id"], item["source"], item["category"],
                        item["title"], item.get("url", ""),
                        item.get("price", ""), item.get("description", ""),
                    )
                    new_items.append(item)

            for item in new_items:
                if alert_item(item):
                    mark_alerted(item["id"])

            log_scan(config["name"], len(items), len(new_items))
            total_new += len(new_items)

            if new_items:
                log.info(f"{config['name']}: {len(new_items)} new items found")

            time.sleep(2)

        except Exception as e:
            log.error(f"Error scanning {config['name']}: {e}")
            log_scan(config["name"], 0, 0, str(e))

    return total_new


def load_custom_searches():
    if os.path.exists(CUSTOM_SEARCHES_FILE):
        try:
            with open(CUSTOM_SEARCHES_FILE) as f:
                return json.load(f)
        except Exception:
            return []
    return []


def run_full_scan():
    log.info("=" * 50)
    log.info(f"Starting full scan at {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    total = 0

    all_gumtree = GUMTREE_SEARCHES + load_custom_searches()
    total += run_scan_group(gumtree.scan, all_gumtree, "Gumtree")
    total += run_scan_group(news.scan, NEWS_FEEDS, "News")
    total += run_scan_group(auctions.scan, AUCTION_SOURCES, "Auctions")
    total += run_scan_group(tenders.scan, TENDER_SOURCES, "Tenders")

    stats = get_stats()
    log.info(
        f"Scan complete. New items this run: {total} | "
        f"Total tracked: {stats['total_tracked']} | "
        f"New today: {stats['new_today']} | "
        f"Alerts sent: {stats['alerts_sent']}"
    )


def send_daily_summary():
    stats = get_stats()
    msg = (
        f"📊 *StackUp Daily Summary*\n\n"
        f"Items tracked: {stats['total_tracked']}\n"
        f"New today: {stats['new_today']}\n"
        f"Alerts sent: {stats['alerts_sent']}\n\n"
        f"Scanner running. Next scan in {SCAN_INTERVAL_MINUTES} min."
    )
    send_telegram(msg)


def main():
    log.info("StackUp Opportunity Scanner starting...")
    init_db()

    run_full_scan()

    schedule.every(SCAN_INTERVAL_MINUTES).minutes.do(run_full_scan)
    schedule.every().day.at("07:00").do(send_daily_summary)
    schedule.every().day.at("18:00").do(send_daily_summary)

    log.info(f"Scheduled: scan every {SCAN_INTERVAL_MINUTES} min, daily summary at 07:00 and 18:00")

    send_telegram(
        f"✅ *StackUp Scanner Online*\n"
        f"Scanning every {SCAN_INTERVAL_MINUTES} min\n"
        f"Sources: Gumtree, News, Auctions, Tenders"
    )

    while True:
        schedule.run_pending()
        time.sleep(10)


if __name__ == "__main__":
    main()
