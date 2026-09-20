import glob
import json
import discord
from discord import app_commands
from discord.ext import commands


class MarketCmd(commands.Cog):

  def __init__(self, bot):
    self.bot = bot

  async def item_autocomplete(
      self, interaction: discord.Interaction, current: str
  ) -> list[app_commands.Choice[str]]:
    try:
      # Mengarah ke folder data/
      json_files = glob.glob('data/preset_*_full.json')
      item_names = set()

      for jf in json_files:
        with open(jf, 'r', encoding='utf-8') as f:
          data = json.load(f)
          for item in data:
            name = item.get('item', {}).get('name')
            if name:
              item_names.add(name)

      filtered = [
          name for name in item_names if current.lower() in name.lower()
      ]
      return [
          app_commands.Choice(name=name[:100], value=name)
          for name in list(filtered)[:25]
      ]
    except Exception as e:
      print(f'Gagal memuat autocomplete: {e}')
      return []

  @app_commands.command(
      name='market',
      description=(
          'Cek harga dan stok item market (gunakan pilihan menu yang muncul)'
      ),
  )
  @app_commands.autocomplete(item_name=item_autocomplete)
  async def market(self, interaction: discord.Interaction, item_name: str):
    await interaction.response.defer()

    # Mengarah ke folder data/
    json_files = glob.glob('data/preset_*_full.json')
    found_items = []
    total_stock = 0
    min_price = float('inf')
    currency = 'USDT'

    for jf in json_files:
      with open(jf, 'r', encoding='utf-8') as f:
        data = json.load(f)
        for item in data:
          name = item.get('item', {}).get('name', '')
          if name.lower() == item_name.lower():
            stock = item.get('displayAmount', 1)
            price = item.get('cryptoPriceInfo', {}).get('price', 0)
            currency = item.get('cryptoPriceInfo', {}).get(
                'currencyType', 'USDT'
            )

            total_stock += stock
            if price > 0 and price < min_price:
              min_price = price

            found_items.append(item)

    if not found_items:
      await interaction.followup.send(
          f'❌ Item dengan nama **"{item_name}"** tidak ditemukan di database'
          ' market[span_1](start_span)[span_1](end_span).'
      )
      return

    best_price = min_price if min_price != float('inf') else 'N/A'

    embed = discord.Embed(
        title=f'📊 Info Market: {item_name}', color=discord.Color.green()
    )
    embed.add_field(name='📦 Total Stok Tersedia', value=f'{total_stock} pcs')
    embed.add_field(name='🏷️ Jumlah Penawar', value=f'{len(found_items)} seller')
    embed.add_field(
        name='💰 Harga Termurah', value=f'{best_price} {currency}', inline=False
    )

    await interaction.followup.send(embed=embed)


async def setup(bot):
  await bot.add_cog(MarketCmd(bot))
