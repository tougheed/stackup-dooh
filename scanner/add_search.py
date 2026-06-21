#!/usr/bin/env python3
"""Quick CLI to add a new Gumtree search without editing config.py"""

import json
import os
import sys

CUSTOM_SEARCHES_FILE = os.path.join(os.path.dirname(__file__), "custom_searches.json")


def load_custom():
    if os.path.exists(CUSTOM_SEARCHES_FILE):
        with open(CUSTOM_SEARCHES_FILE) as f:
            return json.load(f)
    return []


def save_custom(searches):
    with open(CUSTOM_SEARCHES_FILE, "w") as f:
        json.dump(searches, f, indent=2)


def add():
    print("=== Add Custom Gumtree Search ===")
    name = input("Search name (e.g., 'diesel_bowser'): ").strip()
    search_term = input("Gumtree search term (e.g., 'diesel bowser'): ").strip()
    keywords = input("Alert keywords, comma-separated (e.g., 'urgent,cheap,must go'): ").strip()
    category = input("Category tag (e.g., 'diesel_flip'): ").strip() or "custom"

    url = f"https://www.gumtree.co.za/s-{search_term.replace(' ', '+')}/v1q0p1"

    entry = {
        "name": name,
        "url": url,
        "keywords": [k.strip() for k in keywords.split(",")],
        "category": category,
    }

    searches = load_custom()
    searches.append(entry)
    save_custom(searches)
    print(f"Added. Restart scanner to pick up: sudo systemctl restart stackup-scanner")


def list_searches():
    searches = load_custom()
    if not searches:
        print("No custom searches yet.")
        return
    for s in searches:
        print(f"  {s['name']}: {s['url']} | keywords: {s['keywords']}")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "list":
        list_searches()
    else:
        add()
