# config.py
import os

BOT_VERSION = "v6.0.0-Hybrid"

# Baca dari environment variable, dengan fallback ke default
BOT_TOKEN = os.getenv("BOT_TOKEN", "")
GUILD_ID = int(os.getenv("GUILD_ID", "589167145452175411"))

CMD_CHANNEL_ID = int(os.getenv("CMD_CHANNEL_ID", "1544490756809564170"))
ALERT_CHANNEL_ID = int(os.getenv("ALERT_CHANNEL_ID", "1545258649323176006"))

API_BASE_URL = "https://api.nextmarket.games/l9asia/v1/sale/c2c"

HEADERS = {
    "Accept": "application/json, text/plain, */*",
    "Content-Type": "application/json",
    "Origin": "https://l9asia.nextmarket.games",
    "Referer": "https://l9asia.nextmarket.games/",
    "User-Agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36"
}

EXACT_PAYLOAD = {
    "presetIdList": [],
    "realmCode": "NEW_REALM_2"
}

SALES_FILE = "sales.json"
