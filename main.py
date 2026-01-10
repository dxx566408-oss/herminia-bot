import os
import threading
from flask import Flask, render_template
import discord
from discord.ext import commands

# 1. إعداد السيرفر
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

def run():
    # تأكدنا أن البورت 5000 ليتوافق مع ريندر
    app.run(host='0.0.0.0', port=5000)

def keep_alive():
    t = threading.Thread(target=run)
    t.start()

# 2. إعداد البوت
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f'✅ {bot.user} Online!')
    try:
        await bot.tree.sync()
    except Exception as e:
        print(e)

# 3. التشغيل
if __name__ == "__main__":
    keep_alive()
    token = os.environ.get("DISCORD_TOKEN")
    bot.run(token)
