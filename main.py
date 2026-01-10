import discord
from discord.ext import commands
import os
import asyncio
from flask import Flask
from threading import Thread

# --- إعدادات البوت الأساسية ---
intents = discord.Intents.default()
intents.message_content = True
intents.members = True 

bot = commands.Bot(command_prefix="!", intents=intents)
app = Flask(__name__)

# --- إعدادات الاستضافة (Render) ---
@app.route('/')
def home(): return "Herminia Central Brain is Online"

def run_flask():
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

# --- دالة تشغيل المجالات (Cogs) ---
async def load_extensions():
    # هنا نضيف اسم أي ملف جديد ننشئه (بدون .py)
    extensions = ['destruction', 'general'] 
    for ext in extensions:
        try:
            await bot.load_extension(ext)
            print(f"✅ تم تحميل: {ext}")
        except Exception as e:
            print(f"❌ خطأ في تحميل {ext}: {e}")

@bot.event
async def on_ready():
    print(f"🚀 العقل المركزي جاهز.. البوت متصل باسم: {bot.user}")

# --- تشغيل البوت ---
async def main():
    Thread(target=run_flask).start()
    async with bot:
        await load_extensions()
        await bot.start(os.getenv('DISCORD_TOKEN'))

if __name__ == "__main__":
    asyncio.run(main())
