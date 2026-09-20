import discord
from discord.ext import commands
import os
import asyncio

# Import file config
import config


# ============================================================
# KONFIGURASI INTENTS
# ============================================================
intents = discord.Intents.default()
intents.message_content = True


# ============================================================
# INISIALISASI BOT
# ============================================================
bot = commands.Bot(
    command_prefix="!",
    intents=intents,
    help_command=None
)


# ============================================================
# EVENT: ON READY
# ============================================================
@bot.event
async def on_ready():
    print("=========================================")
    print(f"✅ Sistem Online: Bot terhubung sebagai {bot.user}")
    print("=========================================")

    # Load JSON catalog dari folder data/
    try:
        import json_loader
        total = json_loader.load_catalog()
        print(f"📚 Katalog: {total} item unik siap dipakai.")
    except Exception as e:
        print(f"⚠️ Gagal load catalog: {e}")

    # Sinkronisasi slash command ke guild
    try:
        guild = discord.Object(id=config.GUILD_ID)
        bot.tree.copy_global_to(guild=guild)
        synced = await bot.tree.sync(guild=guild)
        print(f"✅ Berhasil sinkronisasi {len(synced)} slash command(s).")
        for cmd in synced:
            print(f"   • /{cmd.name}")
    except Exception as e:
        print(f"❌ Gagal sinkronisasi: {e}")

    await bot.change_presence(
        activity=discord.Game(name="Market Lord Nine")
    )


# ============================================================
# LOAD SEMUA COG
# ============================================================
async def load_cogs():
    """Fungsi untuk memuat seluruh file command (Cog) dari folder 'cogs'."""
    if not os.path.exists('./cogs'):
        print("⚠️ Folder 'cogs' tidak ditemukan!")
        return

    for filename in os.listdir('./cogs'):
        if filename.endswith('.py') and not filename.startswith('__'):
            try:
                await bot.load_extension(f'cogs.{filename[:-3]}')
                print(f"⚙️ Berhasil memuat sistem: {filename}")
            except Exception as e:
                print(f"❌ Gagal memuat {filename}: {e}")


# ============================================================
# FUNGSI UTAMA
# ============================================================
async def main():
    """Fungsi utama untuk menjalankan startup bot secara asinkron."""
    await load_cogs()

    if hasattr(config, 'BOT_TOKEN') and config.BOT_TOKEN:
        try:
            await bot.start(config.BOT_TOKEN)
        except discord.LoginFailure:
            print("❌ Token tidak valid. Periksa BOT_TOKEN di Wispbyte env var!")
    else:
        print("❌ Variabel BOT_TOKEN tidak ditemukan di config.py!")


# ============================================================
# EKSEKUSI
# ============================================================
if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n🛑 Bot dimatikan secara manual.")
