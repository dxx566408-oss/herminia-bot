import os
import threading
from flask import Flask, render_template
import discord
from discord.ext import commands

app = Flask(__name__)

@app.route('/')
def home():
    # هنا نجلب قائمة السيرفرات التي دخلها البوت
    # سنرسل الأسماء والأيقونات
    guilds = []
    for guild in bot.guilds:
        guild_info = {
            "name": guild.name,
            "id": guild.id,
            "icon": str(guild.icon.url) if guild.icon else "https://cdn.discordapp.com/embed/avatars/0.png"
        }
        guilds.append(guild_info)
    
    # نرسل القائمة لملف الـ HTML
    return render_template('index.html', guilds=guilds)

def run():
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = threading.Thread(target=run)
    t.start()

intents = discord.Intents.default()
intents.guilds = True  # مهم جداً لرؤية السيرفرات
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f'✅ {bot.user} Dashboard Live!')

if __name__ == "__main__":
    keep_alive()
    token = os.environ.get("DISCORD_TOKEN")
    bot.run(token)
