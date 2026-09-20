# cogs/market_cmd.py
import discord
from discord import app_commands
from discord.ext import commands

import json_loader
from utils import get_rarity_badge


class MarketCmd(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    # ============================================================
    # AUTOCOMPLETE
    # ============================================================
    async def item_autocomplete(
        self, interaction: discord.Interaction, current: str
    ) -> list[app_commands.Choice[str]]:
        try:
            names = json_loader.search_names(current, limit=25)
            return [
                app_commands.Choice(name=n[:100], value=n)
                for n in names
            ]
        except Exception as e:
            print(f"❌ Autocomplete error: {e}")
            return []

    # ============================================================
    # COMMAND: /market
    # ============================================================
    @app_commands.command(
        name="market",
        description="Cek harga dan stok item di market NextMarket",
    )
    @app_commands.autocomplete(item_name=item_autocomplete)
    async def market(self, interaction: discord.Interaction, item_name: str):
        await interaction.response.defer()

        stats = json_loader.get_stats_by_name(item_name)

        if not stats:
            await interaction.followup.send(
                f'❌ Item **"{item_name}"** tidak ditemukan di katalog.\n'
                f'Coba pilih dari menu autocomplete saat mengetik.'
            )
            return

        badge = get_rarity_badge(stats["name"], stats["color"])

        embed = discord.Embed(
            title=f"📊 Market Info",
            description=f"**{stats['name']}**\n{badge}",
            color=discord.Color.green(),
        )

        embed.add_field(
            name="📦 Total Stok",
            value=f"`{stats['total_stock']}` pcs",
            inline=True,
        )
        embed.add_field(
            name="🏷️ Jumlah Seller",
            value=f"`{stats['seller_count']}` listing",
            inline=True,
        )
        embed.add_field(
            name="\u200b",
            value="\u200b",
            inline=True,
        )

        currency = stats["currency"]
        embed.add_field(
            name="💰 Harga Terendah",
            value=f"`{stats['min_price']:.2f}` {currency}",
            inline=True,
        )
        embed.add_field(
            name="💵 Harga Tertinggi",
            value=f"`{stats['max_price']:.2f}` {currency}",
            inline=True,
        )
        embed.add_field(
            name="📈 Rata-rata",
            value=f"`{stats['avg_price']:.2f}` {currency}",
            inline=True,
        )

        if stats["enhancement"] > 0:
            embed.add_field(
                name="✨ Enhancement",
                value=f"+{stats['enhancement']}",
                inline=True,
            )

        embed.set_footer(text="HelenaBot • Market Checker")

        await interaction.followup.send(embed=embed)


async def setup(bot):
    await bot.add_cog(MarketCmd(bot))
