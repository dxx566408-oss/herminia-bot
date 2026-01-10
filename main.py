import discord
from discord.ext import commands
import os
import asyncio
from flask import Flask
from threading import Thread

intents = discord.Intents.default()
intents.message_content = True
intents.members = True 

bot = commands.Bot(command_prefix="!", intents=intents)
app = Flask(__name__)

@app.route('/')
def home(): return "Herminia Central Brain is Online"

def run_flask():
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))

async def load_extensions():
    # تأكد أن الأسماء مطابقة لأسماء ملفاتك في GitHub
    extensions = ['destruction', 'general'] 
    for ext in extensions:
        try:
            await bot.load_extension(ext)
            print(f"✅ [اللوحة] تم تحميل المجال: {ext}")
        except Exception as e:
            print(f"❌ [اللوحة] فشل تحميل {ext}: {e}")

@bot.event
async def on_ready():
    print(f"⏳ [اللوحة] جاري مزامنة أوامر السلاش...")
    try:
        synced = await bot.tree.sync()
        print(f"✅ [اللوحة] تمت المزامنة! عدد الأوامر الشغالة: {len(synced)}")
    except Exception as e:
        print(f"❌ [اللوحة] فشل المزامنة: {e}")
    print(f"🚀 [اللوحة] البوت جاهز باسم: {bot.user}")

async def main():
    Thread(target=run_flask).start()
    async with bot:
        await load_extensions()
        await bot.start(os.getenv('DISCORD_TOKEN'))

if __name__ == "__main__":
    asyncio.run(main())

