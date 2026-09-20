import os
import json

from config import SALES_FILE


# ============================================================
# GLOBAL STATE
# ============================================================

tax_rate = 15.0
usdt_rate = 17718.8

previous_stock_snapshot = {}

daily_sales_tracker = {}
weekly_sales_tracker = {}

rolling_12h_history = {}

recent_search_history = []


# ============================================================
# LOAD DATA
# ============================================================

def load_sales_data():
    global daily_sales_tracker
    global weekly_sales_tracker
    global tax_rate
    global usdt_rate
    global rolling_12h_history
    global recent_search_history

    if not os.path.exists(SALES_FILE):
        return

    try:
        with open(
            SALES_FILE,
            "r",
            encoding="utf-8"
        ) as f:
            data = json.load(f)

        daily_sales_tracker = data.get(
            "daily",
            {}
        )

        weekly_sales_tracker = data.get(
            "weekly",
            {}
        )

        tax_rate = data.get(
            "tax_rate",
            15.0
        )

        usdt_rate = data.get(
            "usdt_rate",
            17718.8
        )

        rolling_12h_history = data.get(
            "history_12h",
            {}
        )

        recent_search_history = data.get(
            "search_history",
            []
        )

        print(
            "Data sales & config berhasil dimuat."
        )

    except Exception as e:
        print(
            f"Error loading sales.json: {e}"
        )


# ============================================================
# SAVE DATA
# ============================================================

def save_sales_data():
    try:
        data = {
            "daily": daily_sales_tracker,
            "weekly": weekly_sales_tracker,
            "tax_rate": tax_rate,
            "usdt_rate": usdt_rate,
            "history_12h": rolling_12h_history,
            "search_history": recent_search_history
        }

        with open(
            SALES_FILE,
            "w",
            encoding="utf-8"
        ) as f:
            json.dump(
                data,
                f,
                indent=4,
                ensure_ascii=False
            )

    except Exception as e:
        print(
            f"Error saving sales.json: {e}"
        )


# ============================================================
# SEARCH HISTORY
# ============================================================

def add_to_history(item_name):
    global recent_search_history

    item_name = item_name.strip()

    if not item_name:
        return

    if item_name in recent_search_history:
        recent_search_history.remove(
            item_name
        )

    recent_search_history.insert(
        0,
        item_name
    )

    if len(recent_search_history) > 15:
        recent_search_history.pop()

    save_sales_data()