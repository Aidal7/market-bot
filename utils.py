from database import EQ_KEYWORDS, MASTER_ITEM_DATABASE


def classify_item(item_name: str) -> str:
    """Klasifikasi item secara eksklusif agar hasil command tidak tercampur.

    Returns: weapon, armor, accessory, skill, atau other.
    """
    name = (item_name or "").strip().lower()

    # Skill/ability dipisahkan lebih dulu.
    skill_keywords = (
        "skill", "skillbook", "skill book", "ability", "ability book"
    )
    if any(k in name for k in skill_keywords):
        return "skill"

    weapon_keywords = (
        "crossbow", "bow", "dagger", "sword", "staff", "spear",
        "scythe", "axe", "mace", "hammer", "wand", "orb", "blade",
        "weapon", "gun", "rifle", "pistol"
    )

    armor_keywords = (
        "armor", "armour", "helmet", "helm", "hat", "hood", "robe",
        "coat", "gloves", "glove", "boots", "boot",
        "shoes", "shoe", "pants", "trousers", "gaiters", "shield"
    )

    accessory_keywords = (
        "necklace", "wristband", "ring", "earring", "belt", "pendant",
        "cape", "cloak", "accessory", "accessories"
    )

    # Urutan ini penting: armor tidak pernah dianggap weapon walaupun
    # namanya mengandung token yang kebetulan cocok dengan weapon.
    if any(k in name for k in armor_keywords):
        return "armor"

    if any(k in name for k in weapon_keywords):
        return "weapon"

    if any(k in name for k in accessory_keywords):
        return "accessory"

    return "other"


def is_weapon_item(item_name: str) -> bool:
    return classify_item(item_name) == "weapon"


def is_armor_item(item_name: str) -> bool:
    return classify_item(item_name) == "armor"


def is_accessory_item(item_name: str) -> bool:
    return classify_item(item_name) == "accessory"


def is_equipment_item(item_name: str) -> bool:
    """True hanya untuk equipment yang dikenal (weapon/armor/accessory)."""
    category = classify_item(item_name)
    if category in {"weapon", "armor", "accessory"}:
        return True

    name_lower = (item_name or "").lower()
    return any(
        word.lower() in name_lower
        for word in EQ_KEYWORDS
    )


def get_item_location(item_name):
    """
    Mengambil lokasi drop dari database manual.
    Jika belum ada, tampilkan pesan bahwa lokasi
    dapat ditambahkan secara manual.
    """
    item_lower = item_name.lower()

    for key, locs in MASTER_ITEM_DATABASE.items():
        key_lower = key.lower()

        if (
            key_lower in item_lower
            or item_lower in key_lower
        ):
            return "\n".join(
                f"• {loc}"
                for loc in locs
            )

    return (
        "📍 *Lokasi drop belum terdaftar di database bot "
        "(Bisa ditambahkan secara manual).*"
    )


def get_rarity_badge(name, color):
    """Mengubah tier/color item menjadi badge."""
    name_upper = name.upper()
    color_upper = color.upper() if color else "UNKNOWN"

    t_badge_map = {
        "T1": "⚪ [T1 Common]",
        "T2": "🟩 [T2 Uncommon]",
        "T3": "🟦 [T3 Rare]",
        "T4": "🟪 [T4 Epic]",
        "T5": "🟨 [T5 Legendary]",
        "T6": "🟥 [T6 Mythic]"
    }

    for t_key, badge in t_badge_map.items():
        if t_key in name_upper:
            return badge

    badge_map = {
        "GRAY": "⚪ [Common]",
        "GREY": "⚪ [Common]",
        "GREEN": "🟩 [Uncommon]",
        "BLUE": "🟦 [Rare]",
        "MAGENTA": "🟪 [Epic]",
        "PURPLE": "🟪 [Epic]",
        "ORANGE": "🟨 [Legendary]",
        "YELLOW": "🟨 [Legendary]",
        "RED": "🟥 [Mythic]"
    }

    return badge_map.get(
        color_upper,
        "⚪ [Common]"
    )


def group_item_stats(items, usdt_rate):
    """Menggabungkan listing item yang memiliki nama sama."""
    grouped = {}

    for item in items:
        name = item["name"]
        price_idr = item["price_idr"]
        price_usdt = item["price_usdt"]
        stock = item["stock"]

        if name not in grouped:
            grouped[name] = {
                "prices_idr": [],
                "prices_usdt": [],
                "total_stock": 0,
                "color": item["color"]
            }

        grouped[name]["prices_idr"].append(
            price_idr
        )

        grouped[name]["prices_usdt"].append(
            price_usdt
        )

        grouped[name]["total_stock"] += stock

    summary = []

    for name, data in grouped.items():
        idr_list = data["prices_idr"]
        usdt_list = data["prices_usdt"]

        summary.append({
            "name": name,

            "lowest_idr": min(idr_list),
            "lowest_usdt": min(usdt_list),

            "highest_idr": max(idr_list),
            "highest_usdt": max(usdt_list),

            "average_idr": (
                sum(idr_list) / len(idr_list)
            ),

            "average_usdt": (
                sum(usdt_list) / len(usdt_list)
            ),

            "stock": data["total_stock"],

            "color": data["color"]
        })

    summary.sort(
        key=lambda x: x["lowest_idr"],
        reverse=True
    )

    return summary