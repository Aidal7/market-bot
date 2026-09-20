import discord
from discord import app_commands
from discord.ext import commands


class ToolsCmd(commands.Cog):

  def __init__(self, bot):
    self.bot = bot

  @app_commands.command(
      name='tutorial',
      description='Menampilkan panduan lengkap cara menggunakan HelenaBot',
  )
  async def tutorial(self, interaction: discord.Interaction):
    embed = discord.Embed(
        title='📖 Panduan Penggunaan HelenaBot',
        description=(
            'Selamat datang! Berikut adalah panduan lengkap cara mencari data'
            ' item market menggunakan HelenaBot[span_7](start_span)[span_7](end_span).'
        ),
        color=discord.Color.blue(),
    )

    embed.add_field(
        name='1️⃣ Fitur Menu Pilihan (Autocomplete)',
        value=(
            '• Ketik `/market` pada kolom chat Discord.\n• Saat Anda mengetik'
            ' **1 huruf atau kata** pada kolom `item_name`, Discord akan'
            ' memunculkan **menu pilihan otomatis**.\n• Klik salah satu'
            ' pilihan yang muncul agar penulisan nama item dijamin akurat dan'
            ' terhindar dari salah ketik[span_8](start_span)[span_8](end_span)[span_9](start_span)[span_9](end_span).'
        ),
        inline=False,
    )

    embed.add_field(
        name='2️⃣ Informasi yang Ditampilkan',
        value=(
            'Bot akan merangkum dan menampilkan:\n• **Total Stok** keseluruhan'
            ' barang di market.\n• **Jumlah Seller** atau penawar yang'
            ' menjual item tersebut.\n• **Harga Termurah** (*Lowest Price*)'
            ' secara *real-time* berdasarkan pembaruan data terakhir[span_10](start_span)[span_10](end_span).'
        ),
        inline=False,
    )

    embed.add_field(
        name='3️⃣ Pembaruan Data Otomatis',
        value=(
            'Data diambil dari sinkronisasi sistem GitHub Actions secara'
            ' berkala, sehingga informasi harga dan stok selalu terbarukan[span_11](start_span)[span_11](end_span).'
        ),
        inline=False,
    )

    embed.set_footer(text='HelenaBot Market Checker System • Powered by JSON')
    await interaction.response.send_message(embed=embed)


async def setup(bot):
  await bot.add_cog(ToolsCmd(bot))
