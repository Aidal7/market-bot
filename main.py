import discord
from discord.ext import commands
import os
import asyncio

# Import file config tempat token bot disimpan
import config

# Konfigurasi Intents (Wajib untuk discord.py versi terbaru)
intents = discord.Intents.default()
intents.message_content = True  # Wajib diaktifkan agar bot bisa membaca pesan user

@bot.event
async def on_ready():
    print("=========================================")
    print(f"✅ Sistem Online: Bot terhubung sebagai {bot.user}")
    print("=========================================")

    # --- TAMBAHKAN BLOK INI UNTUK SINKRONISASI SLASH COMMAND ---
    try:
        guild = discord.Object(id=config.GUILD_ID)
        bot.tree.copy_global_to(guild=guild)
        synced = await bot.tree.sync(guild=guild)
        print(f"✅ Berhasil sinkronisasi {len(synced)} slash command(s).")
        for cmd in synced:
            print(f"   • /{cmd.name}")
    except Exception as e:
        print(f"❌ Gagal melakukan sinkronisasi: {e}")
    # ----------------------------------------------------------------

    # Mengatur status bot saat online (opsional)
    await bot.change_presence(activity=discord.Game(name="Memantau Market Lord Nine"))

async def load_cogs():
    """Fungsi untuk memuat seluruh file command (Cog) dari folder 'cogs'."""
    # Pastikan folder cogs/ ada di direktori yang sama dengan main.py
    if not os.path.exists('./cogs'):
        print("⚠️ Folder 'cogs' tidak ditemukan!"
        return

    for filename in os.listdir('./cogs'):
        if filename.endswith('.py') and not filename.startswith('__'):
            try:
                # Memuat extension/cog satu per satu
                await bot.load_extension(f'cogs.{filename[:-3]}')
                print(f"⚙️ Berhasil memuat sistem: {filename}")
            except Exception as e:
                print(f"❌ Gagal memuat {filename}: {e}")

async def main():
    """Fungsi utama untuk menjalankan startup bot secara asinkron."""
    # 1. Muat semua command dari folder cogs
    await load_cogs()
    
    # 2. Jalankan bot menggunakan variabel BOT_TOKEN dari file config.py
    if hasattr(config, 'BOT_TOKEN') and config.BOT_TOKEN:
        try:
            await bot.start(config.BOT_TOKEN)
        except discord.LoginFailure:
            print("❌ Token tidak valid. Periksa kembali BOT_TOKEN di config.py!")
    else:
        print("❌ Variabel BOT_TOKEN tidak ditemukan di file config.py!")

# Eksekusi script utama
if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n🛑 Bot dimatikan secara manual.")
