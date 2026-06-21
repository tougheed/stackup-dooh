import sqlite3
import time
from config import DB_PATH


def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_conn()
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS seen_items (
            id TEXT PRIMARY KEY,
            source TEXT NOT NULL,
            category TEXT NOT NULL,
            title TEXT NOT NULL,
            url TEXT,
            price TEXT,
            description TEXT,
            first_seen INTEGER NOT NULL,
            alerted INTEGER DEFAULT 0
        );
        CREATE TABLE IF NOT EXISTS opportunities (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            item_id TEXT,
            chain TEXT,
            action TEXT,
            status TEXT DEFAULT 'new',
            notes TEXT,
            created INTEGER NOT NULL,
            FOREIGN KEY (item_id) REFERENCES seen_items(id)
        );
        CREATE TABLE IF NOT EXISTS scan_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            source TEXT NOT NULL,
            timestamp INTEGER NOT NULL,
            items_found INTEGER DEFAULT 0,
            new_items INTEGER DEFAULT 0,
            errors TEXT
        );
    """)
    conn.commit()
    conn.close()


def is_seen(item_id):
    conn = get_conn()
    row = conn.execute("SELECT 1 FROM seen_items WHERE id = ?", (item_id,)).fetchone()
    conn.close()
    return row is not None


def save_item(item_id, source, category, title, url="", price="", description=""):
    conn = get_conn()
    conn.execute(
        "INSERT OR IGNORE INTO seen_items (id, source, category, title, url, price, description, first_seen) "
        "VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
        (item_id, source, category, title, url, price, description, int(time.time())),
    )
    conn.commit()
    conn.close()


def mark_alerted(item_id):
    conn = get_conn()
    conn.execute("UPDATE seen_items SET alerted = 1 WHERE id = ?", (item_id,))
    conn.commit()
    conn.close()


def log_scan(source, items_found, new_items, errors=None):
    conn = get_conn()
    conn.execute(
        "INSERT INTO scan_log (source, timestamp, items_found, new_items, errors) VALUES (?, ?, ?, ?, ?)",
        (source, int(time.time()), items_found, new_items, errors),
    )
    conn.commit()
    conn.close()


def get_stats():
    conn = get_conn()
    total = conn.execute("SELECT COUNT(*) FROM seen_items").fetchone()[0]
    today = conn.execute(
        "SELECT COUNT(*) FROM seen_items WHERE first_seen > ?",
        (int(time.time()) - 86400,),
    ).fetchone()[0]
    alerted = conn.execute("SELECT COUNT(*) FROM seen_items WHERE alerted = 1").fetchone()[0]
    conn.close()
    return {"total_tracked": total, "new_today": today, "alerts_sent": alerted}
