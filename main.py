import os
import requests
from flask import Flask, redirect, url_for, session, render_template, request

app = Flask(__name__)
app.secret_key = "any_secret_key" # مفتاح لتأمين الجلسة

# معلومات البوت (استبدل CLIENT_SECRET بالخاص بك من ديسكورد)
CLIENT_ID = "1326462947265843241"
CLIENT_SECRET = os.environ.get("CLIENT_SECRET")
REDIRECT_URI = "https://herminia-bot.onrender.com/callback"

@app.route('/')
def home():
    if 'token' in session:
        # إذا سجل الدخول، نجلب سيرفراته
        headers = {"Authorization": f"Bearer {session['token']}"}
        user_guilds = requests.get("https://discord.com/api/users/@me/guilds", headers=headers).json()
        
        # تصفية السيرفرات التي يملك فيها صلاحية إدارة السيرفر (Permissions 0x20)
        manageable_guilds = [g for g in user_guilds if (int(g['permissions']) & 0x20) == 0x20]
        return render_template('index.html', guilds=manageable_guilds, logged_in=True)
    
    return render_template('index.html', logged_in=False)

@app.route('/login')
def login():
    # رابط تسجيل الدخول لطلب الوصول للسيرفرات
    scope = "identify guilds"
    discord_login_url = f"https://discord.com/api/oauth2/authorize?client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}&response_type=code&scope={scope}"
    return redirect(discord_login_url)

@app.route('/callback')
def callback():
    code = request.args.get("code")
    data = {
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': REDIRECT_URI,
        'scope': 'identify guilds'
    }
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    response = requests.post("https://discord.com/api/oauth2/token", data=data, headers=headers)
    session['token'] = response.json().get('access_token')
    return redirect(url_for('home'))

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
