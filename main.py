import discord
from discord.ext import commands
import os, json, random
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
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def load_responses():
    if os.path.exists(RESPONSES_FILE):
        with open(RESPONSES_FILE, "r", encoding="utf-8") as f:
            try: return json.load(f)
            except: return {}
    return {}

# --- محرك الردود التلقائية في ديسكورد ---
@bot.event
async def on_message(message):
    if message.author.bot:
        return

    responses = load_responses()
    content = message.content.strip()

    for keyword, data_list in responses.items():
        for data in data_list:
            # التحقق من نوع البحث (كامل الرسالة أو تطابق تام)
            is_match = False
            if data.get('all_search'):
                if keyword in content: is_match = True
            else:
                if keyword == content: is_match = True

            if is_match:
                # التحقق من الرومات المسموحة
                if data.get('allowed_rooms') and str(message.channel.id) not in data['allowed_rooms']:
                    continue
                
                # التحقق من الرتب المسموحة
                user_roles = [str(role.id) for role in message.author.roles]
                if data.get('allowed_roles') and not any(r in user_roles for r in data['allowed_roles']):
                    continue

                # التجهيز للإرسال
                file = None
                if data.get('media') and os.path.exists(data['media']):
                    file = discord.File(data['media'])

                target = message.author if data.get('in_private') else message.channel
                
                try:
                    if data.get('as_reply') and not data.get('in_private'):
                        await message.reply(content=data.get('reply'), file=file)
                    else:
                        await target.send(content=data.get('reply'), file=file)
                except Exception as e:
                    print(f"Error sending message: {e}")
                return # التوقف بعد أول رد مطابق

    await bot.process_commands(message)

# --- مسارات لوحة التحكم (Flask) ---
@app.route('/')
def home():
    with open("dashboard2.html", "r", encoding="utf-8") as f:
        return f.read()

@app.route('/get_server_info')
def get_server_info():
    guild = bot.guilds[0] if bot.guilds else None
    if guild:
        channels = [{"id": str(c.id), "name": c.name} for c in guild.text_channels]
        roles = [{"id": str(r.id), "name": r.name} for r in guild.roles if not r.is_default()]
        return jsonify({"channels": channels, "roles": roles})
    return jsonify({"channels": [], "roles": []})

@app.route('/get_all_responses')
def get_all_responses():
    return jsonify(load_responses())

@app.route('/upload_media', methods=['POST'])
def upload_media():
    file = request.files['file']
    filename = secure_filename(file.filename)
    path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(path)
    return jsonify({"url": path})

@app.route('/save_reply', methods=['POST'])
def save_reply():
    data = request.json
    responses = load_responses()
    responses[data['word']] = data['replies_list']
    with open(RESPONSES_FILE, "w", encoding="utf-8") as f:
        json.dump(responses, f, indent=4, ensure_ascii=False)
    return jsonify({"status": "success"})

@app.route('/delete_reply', methods=['POST'])
def delete_reply():
    data = request.json
    word = data.get('word')
    responses = load_responses()
    if word in responses:
        del responses[word]
        with open(RESPONSES_FILE, "w", encoding="utf-8") as f:
            json.dump(responses, f, indent=4, ensure_ascii=False)
        return jsonify({"status": "success"})
    return jsonify({"status": "error"}), 404

@bot.event
async def on_ready():
    print(f"✅ البوت شغال باسم: {bot.user}")
    print(f"🔗 لوحة التحكم: http://127.0.0.1:5000")

# --- نهاية الكود الخاص بك (استبدل الجزء الأخير بهذا) ---

def run_flask():
    # هنا الطكامة: غيرنا الآي بي لـ 0.0.0.0 والمنفذ ليقرأ من الاستضافة
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=False)

if __name__ == "__main__":
    # تشغيل Flask في خيط منفصل
    t = Thread(target=run_flask)
    t.start()
    
    # تشغيل البوت
    token = os.getenv('DISCORD_TOKEN')
    if token:
        bot.run(token)
    else:
        print("❌ خطأ: لم يتم العثور على DISCORD_TOKEN في الإعدادات!")