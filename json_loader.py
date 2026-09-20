# json_loader.py
import glob
import json
import os
from typing import Optional

# ============================================================
# JSON CATALOG LOADER
# ============================================================
# Membaca semua file data/preset_*_full.json, build index by name,
# dan simpan di memory supaya tidak perlu baca file berulang kali.
# ============================================================

_catalog: list[dict] = []
_index_by_name: dict[str, list[dict]] = {}
_index_by_sku: dict[str, list[dict]] = {}
_unique_names: list[str] = []
_loaded: bool = False


def load_catalog(force: bool = False) -> int:
    """
    Load semua file data/preset_*_full.json ke memory.
    Return jumlah item unik.
    """
    global _catalog, _index_by_name, _index_by_sku, _unique_names, _loaded

    if _loaded and not force:
        return len(_unique_names)

    _catalog = []
    _index_by_name = {}
    _index_by_sku = {}
    _unique_names = []

    json_files = glob.glob("data/preset_*_full.json")
    if not json_files:
        print("⚠️ [json_loader] Tidak ada file data/preset_*_full.json")
        _loaded = True
        return 0

    for jf in json_files:
        try:
            with open(jf, "r", encoding="utf-8") as f:
                data = json.load(f)

            if not isinstance(data, list):
                continue

            for entry in data:
                item_data = entry.get("item") or {}
                name = (item_data.get("name") or "").strip()
                sku = (item_data.get("sku") or "").strip()

                if not name:
                    continue

                _catalog.append(entry)

                key = name.lower()
                _index_by_name.setdefault(key, []).append(entry)

                if sku:
                    _index_by_sku.setdefault(sku, []).append(entry)

        except Exception as e:
            print(f"⚠️ [json_loader] Gagal baca {jf}: {e}")

    _unique_names = sorted(
        {(e.get("item") or {}).get("name", "") for e in _catalog if (e.get("item") or {}).get("name")}
    )
    _loaded = True

    print(f"✅ [json_loader] Load {len(_catalog)} listing, {len(_unique_names)} item unik dari {len(json_files)} file.")
    return len(_unique_names)


def search_names(query: str, limit: int = 25) -> list[str]:
    """Cari nama item yang mengandung query (case-insensitive)."""
    if not _loaded:
        load_catalog()

    query_lower = (query or "").strip().lower()

    if not query_lower:
        return _unique_names[:limit]

    matches = [n for n in _unique_names if query_lower in n.lower()]
    return matches[:limit]


def get_listings_by_name(name: str) -> list[dict]:
    """Ambil semua listing untuk nama item tertentu."""
    if not _loaded:
        load_catalog()

    return _index_by_name.get((name or "").strip().lower(), [])


def get_stats_by_name(name: str) -> Optional[dict]:
    """
    Hitung statistik harga & stok untuk nama item.
    Return dict atau None kalau tidak ada.
    """
    listings = get_listings_by_name(name)
    if not listings:
        return None

    prices = []
    stocks = 0
    color = "UNKNOWN"
    enhancement = 0
    currency = "USDT"

    for entry in listings:
        crypto = entry.get("cryptoPriceInfo") or {}
        price = float(crypto.get("price", 0) or 0)
        if price > 0:
            prices.append(price)

        stocks += int(entry.get("displayAmount", 1) or 1)

        if color == "UNKNOWN":
            color = (entry.get("backgroundColor") or "UNKNOWN").upper()

        enh = entry.get("enhancementLevel") or (entry.get("item") or {}).get("enhancementLevel") or 0
        enhancement = max(enhancement, int(enh or 0))

        currency = crypto.get("currencyType", currency)

    if not prices:
        return None

    return {
        "name": name,
        "total_stock": stocks,
        "seller_count": len(listings),
        "min_price": min(prices),
        "max_price": max(prices),
        "avg_price": sum(prices) / len(prices),
        "currency": currency,
        "color": color,
        "enhancement": enhancement,
    }


def get_total_unique_items() -> int:
    if not _loaded:
        load_catalog()
    return len(_unique_names)


def is_loaded() -> bool:
    return _loaded
