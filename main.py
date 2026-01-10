import os
import requests
from flask import Flask, redirect, url_for, session, render_template, request

app = Flask(__name__)
app.secret_key = "herminia_secure_key" 

# استخدمنا الرقم الجديد الذي أرسلته أنت
CLIENT_ID = "1458119547335999521"
CLIENT_SECRET = os.environ.get("CLIENT_SECRET")
REDIRECT_URI = "https://herminia-bot.onrender.com/callback"

@app.route('/')
def home():
    if 'token' in session:
        headers = {"Authorization": f"Bearer {session['token']}"}
        response = requests.get("https://discord.com/api/users/@me/guilds", headers=headers)
        user_guilds = response.json()
        
        if isinstance(user_guilds, list):
            # تصفية السيرفرات (مدير 0x20)
            manageable_guilds = [g for g in user_guilds if (int(g.get('permissions', 0)) & 0x20) == 0x20]
            return render_template('index.html', guilds=manageable_guilds, logged_in=True)
        else:
            session.pop('token', None)
            return render_template('index.html', logged_in=False, error="خطأ في الجلسة")
    
    return render_template('index.html', logged_in=False)

@app.route('/login')
def login():
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
        'redirect_uri': REDIRECT_URI
    }
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    response = requests.post("https://discord.com/api/oauth2/token", data=data, headers=headers)
    
    token_data = response.json()
    if 'access_token' in token_data:
        session['token'] = token_data.get('access_token')
        return redirect(url_for('home'))
    else:
        return f"خطأ من ديسكورد: {token_data.get('error_description', 'Check Secret in Render')}"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
