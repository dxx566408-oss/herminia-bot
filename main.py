import os
import threading
from flask import Flask, render_template
import discord
from discord.ext import commands

app = Flask(__name__)

@app.route('/')
def home():
    # جمع بيانات السيرفرات التي يتواجد فيها البوت
    guilds_data = []
    if bot.is_ready():
        for guild in bot.guilds:
            guilds_data.append({
                "name": guild.name,
                "icon": str(guild.icon.url) if guild.icon else "https://cdn.discordapp.com/embed/avatars/0.png"
            })
    return render_template('index.html', guilds=guilds_data)

def run():
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = threading.Thread(target=run)
    t.start()

intents = discord.Intents.default()
intents.guilds = True 
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f'✅ {bot.user} Dashboard is Ready!')

if __name__ == "__main__":
    keep_alive()
    token = os.environ.get("DISCORD_TOKEN")
    bot.run(token)
