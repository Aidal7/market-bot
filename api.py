import aiohttp
import asyncio
from config import API_BASE_URL, HEADERS, EXACT_PAYLOAD
from utils import group_item_stats
import storage


async def query_market_api_direct(keyword: str = ""):
    url = f"{API_BASE_URL}?page=0"

    payload = EXACT_PAYLOAD.copy()

    if keyword.strip():
        payload["keyword"] = keyword.strip()

    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(
                url,
                headers=HEADERS,
                json=payload,
                timeout=aiohttp.ClientTimeout(total=8)
            ) as response:

                if response.status == 200:
                    data = await response.json()
                    items = []

                    for entry in data.get("content", []):
                        item_data = entry.get("item") or {}
                        crypto_info = entry.get("cryptoPriceInfo") or {}

                        name = item_data.get("name")

                        price_usdt = crypto_info.get(
                            "price",
                            0
                        ) or 0

                        price_idr = (
                            price_usdt
                            * storage.usdt_rate
                        )

                        stock = entry.get(
                            "displayAmount",
                            1
                        ) or 1

                        bg_color = entry.get(
                            "backgroundColor",
                            "UNKNOWN"
                        ) or "UNKNOWN"

                        enhancement = (
                            entry.get("enhancementLevel")
                            or item_data.get("enhancementLevel")
                            or 0
                        )

                        ability_options = (
                            entry.get(
                                "abilityOptionList",
                                []
                            ) or []
                        )

                        if name:
                            items.append({
                                "name": name,
                                "price_idr": float(
                                    price_idr
                                ),
                                "price_usdt": float(
                                    price_usdt
                                ),
                                "stock": int(
                                    stock
                                ),
                                "color": str(
                                    bg_color
                                ).upper(),
                                "enhancement": int(
                                    enhancement
                                ),
                                "abilityOptionList":
                                    ability_options
                            })

                    return items

        except Exception as e:
            print(
                f"Direct API Query Error "
                f"'{keyword}': {e}"
            )

    return []


async def fetch_single_page(
    session,
    page,
    sem
):
    url = f"{API_BASE_URL}?page={page}"

    async with sem:
        try:
            async with session.post(
                url,
                headers=HEADERS,
                json=EXACT_PAYLOAD,
                timeout=aiohttp.ClientTimeout(total=8)
            ) as response:

                if response.status == 200:
                    data = await response.json()
                    items = []

                    for entry in data.get(
                        "content",
                        []
                    ):
                        item_data = (
                            entry.get("item")
                            or {}
                        )

                        crypto_info = (
                            entry.get(
                                "cryptoPriceInfo"
                            )
                            or {}
                        )

                        name = item_data.get(
                            "name"
                        )

                        price_usdt = (
                            crypto_info.get(
                                "price",
                                0
                            )
                            or 0
                        )

                        price_idr = (
                            price_usdt
                            * storage.usdt_rate
                        )

                        stock = (
                            entry.get(
                                "displayAmount",
                                1
                            )
                            or 1
                        )

                        bg_color = (
                            entry.get(
                                "backgroundColor",
                                "UNKNOWN"
                            )
                            or "UNKNOWN"
                        )

                        enhancement = (
                            entry.get(
                                "enhancementLevel"
                            )
                            or item_data.get(
                                "enhancementLevel"
                            )
                            or 0
                        )

                        ability_options = (
                            entry.get(
                                "abilityOptionList",
                                []
                            )
                            or []
                        )

                        if name:
                            items.append({
                                "name": name,
                                "price_idr": float(
                                    price_idr
                                ),
                                "price_usdt": float(
                                    price_usdt
                                ),
                                "stock": int(
                                    stock
                                ),
                                "color": str(
                                    bg_color
                                ).upper(),
                                "enhancement": int(
                                    enhancement
                                ),
                                "abilityOptionList":
                                    ability_options
                            })

                    return items

        except Exception as e:
            print(
                f"Fetch error page "
                f"{page}: {e}"
            )

        return []


async def fetch_live_items(pages=40):
    sem = asyncio.Semaphore(5)

    async with aiohttp.ClientSession() as session:
        tasks = [
            fetch_single_page(
                session,
                page,
                sem
            )
            for page in range(pages)
        ]

        results = await asyncio.gather(
            *tasks
        )

        return [
            item
            for page_result in results
            for item in page_result
        ]