# database.py

EQ_KEYWORDS = [
    "armor",
    "helmet",
    "boots",
    "gloves",
    "gaiters",
    "shield",
    "sword",
    "staff",
    "bow",
    "dagger",
    "crossbow",
    "scythe",
    "axe",
    "mace",
    "spear",
    "wand",
    "necklace",
    "wristband",
    "ring",
    "earring",
    "belt",
    "pendant",
    "cape",
    "cloak"
]

EQ_TRIGGERS = [
    "eq",
    "weap",
    "weapon",
    "equipment",
    "armor"
]


# ============================================================
# LOKASI DROP MANUAL
# ============================================================
# Bisa ditambah/update manual kapan saja.
#
# Format:
#
# "Nama Item": [
#     "📍 Lokasi 1",
#     "📍 Lokasi 2"
# ]
#
# Kalau item belum ada di sini, bot akan menampilkan:
# "Lokasi drop belum terdaftar..."
# ============================================================

MASTER_ITEM_DATABASE = {

    "Bow: Quality Arrow": [
        "🏹 **Lv.45 Tomb Archer** @ Twilight Hill (Tomb of Time)",
        "🧙 **Lv.52 Mutant Goblin Wizard** @ Secret Laboratory (Test Subject Lab)"
    ],

    "Bow: Aim Target": [
        "🎯 **Monster Boss / Elite Drop** @ Twilight Hill Level 45+"
    ],

    "Bow: Sharp Arrow": [
        "🏹 **Lv.38 Skeleton Archer** @ Coastal Zone"
    ],

    "Crossbow: Distance Control": [
        "🏹 **Elite Crossbowman** @ Coastal Zone / Dungeon T2"
    ],

    "Crossbow: Sharp Arrow": [
        "🏹 **Lv.40 Bandit Crossbow** @ Twilight Hill"
    ],

    "T1 #13 Culture Cell Chest x10": [
        "🧪 **Homunculus Lab & Daily Quest Drop**"
    ],

    "T3 #10 Culture Cell Chest x100": [
        "🧪 **High-Tier Homunculus Lab Level 50+**"
    ]
}