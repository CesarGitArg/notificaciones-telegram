import os
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

BOT_TOKEN = os.environ.get('BOT_TOKEN')
CHAT_ID = os.environ.get('CHAT_ID')

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json or request.form
    monto = data.get('monto', 'Sin monto')
    concepto = data.get('concepto', 'Sin concepto')
    
    mensaje = f"💳 *Nuevo Pago Recibido*\n💰 Monto: {monto}\n📝 Concepto: {concepto}"
    
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        'chat_id': CHAT_ID,
        'text': mensaje,
        'parse_mode': 'Markdown'
    }
    
    response = requests.post(url, json=payload)
    
    if response.status_code == 200:
        return jsonify({"status": "success"}), 200
    else:
        return jsonify({"status": "error", "details": response.text}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
