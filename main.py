import os
import threading
from flask import Flask, render_template
import discord
from discord.ext import commands

# إعداد واجهة الموقع
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

def run():
    # هذا السطر هو السر: يقرأ البورت الذي يريده ريندر تلقائياً
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = threading.Thread(target=run)
    t.start()

# إعداد البوت
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f'✅ {bot.user} Online and Dashboard Ready!')
    try:
        await bot.tree.sync()
    except Exception as e:
        print(f"Sync Error: {e}")

if __name__ == "__main__":
    keep_alive()
    token = os.environ.get("DISCORD_TOKEN")
    if token:
        bot.run(token)
    else:
        print("Error: No DISCORD_TOKEN found!")
