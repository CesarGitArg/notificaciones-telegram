import os
from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

BOT_TOKEN = os.environ.get('BOT_TOKEN')
CHAT_ID = os.environ.get('CHAT_ID')


@app.route('/webhook', methods=['POST'])
def webhook():
  data = request.json or request.form

  # Capturamos cada dato enviado por MacroDroid de forma individual
  monto = data.get('monto', 'Sin monto')
  concepto = data.get('concepto', 'Sin concepto')
  fecha = data.get('fecha', '')
  hora = data.get('hora', '')

  # Armamos el mensaje final con formato HTML para Telegram
  mensaje = (
      '<b>Depositos</b>\n'
      '<b>INGRESO PERSONAL PAY</b>\n\n'
      f'<b>Monto:</b> {monto}\n'
      f'<b>De:</b> {concepto}\n'
      f'<b>Fecha:</b> {fecha} {hora}'
  )

  url = f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage'
  payload = {'chat_id': CHAT_ID, 'text': mensaje, 'parse_mode': 'HTML'}

  response = requests.post(url, json=payload)

  if response.status_code == 200:
    return jsonify({'status': 'success'}), 200
  else:
    return jsonify({'status': 'error', 'details': response.text}), 500


if __name__ == '__main__':
  app.run(host='0.0.0.0', port=5000)

