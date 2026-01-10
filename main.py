import discord
from discord.ext import commands
import os, json, asyncio
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from threading import Thread
from werkzeug.utils import secure_filename

load_dotenv()
intents = discord.Intents.default()
intents.message_content = True 
intents.guilds = True
intents.members = True 

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

    # --- ميزة تدمير الروم (لك أنت فقط) ---
    if message.content == "تدمير_الروم":
        MY_ID = 1371432836946726934  # <<< ضع رقم الـ ID الخاص بك هنا بدلاً من هذه الأرقام
        if message.author.id == MY_ID:
            try:
                await message.channel.delete()
            except Exception as e:
                await message.channel.send(f"❌ أحتاج صلاحية حذف الرومات! الخطأ: {e}")
        return

    # --- نظام الردود التلقائية ---
    responses = load_responses()
    content = message.content.strip()
    for keyword, data_list in responses.items():
        for data in data_list:
            is_match = keyword in content if data.get('all_search') else keyword == content
            if is_match:
                # التحقق من الرومات والرتب (نفس كودك القديم)
                target = message.author if data.get('in_private') else message.channel
                await target.send(content=data.get('reply'))
                return 

    await bot.process_commands(message)

# --- كود التشغيل واللوحة (Render) ---
@app.route('/')
def home(): return "Bot is Running!"

def run_flask():
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

@bot.event
async def on_ready():
    print(f"✅ {bot.user} Online")

if __name__ == "__main__":
    Thread(target=run_flask).start()
    bot.run(os.getenv('DISCORD_TOKEN'))
