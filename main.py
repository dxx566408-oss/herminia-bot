import os
from flask import Flask, render_template
import threading
from discord.ext import commands
import discord

app = Flask(__name__)

@app.route('/')
def home():
    # سيبحث الفلاسك تلقائياً عن ملف index.html داخل مجلد templates
    return render_template('index.html')

def run():
    # بورت 8080 هو الأنسب لخدمات Render
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = threading.Thread(target=run)
    t.start()

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f'✅ {bot.user} Online and Web UI Ready!')
    await bot.tree.sync()

keep_alive()
token = os.environ.get("DISCORD_TOKEN")
bot.run(token)


