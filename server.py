from flask import Flask, request, jsonify, render_template
import os
import requests
from dotenv import load_dotenv

app = Flask(__name__)

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID_VENDEDOR = os.getenv("CHAT_ID_VENDEDOR")

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/api/cotacao", methods=["POST"])
def receber_cotacao():
    dados = request.get_json()
    print("Dados recebidos:", dados)
    mensagem = f"""
        📋 *Nova Cotação Recebida!*
        --------------------------
        👤 *Nome:* {dados.get('nome')}
        📱 *WhatsApp:* {dados.get('whatsapp')}
        ✉️ *Email:* {dados.get('email')}
        🏦 *Administradora:* {dados.get('administradora')}
        💰 *Valor da Carta:* R$ {dados.get('valor_carta')}
        💵 *Valor Pago:* R$ {dados.get('valor_pago')}
        📄 *Status:* {dados.get('status_carta').replace('_', ' ').title()}
        """
    
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID_VENDEDOR,
        "text": mensagem,
        "parse_mode":"Markdown"
    }

    try:
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            return jsonify({"status": "sucesso", "mensagem": "Cotação enviada pelo Telegram!"})
        else:
            return jsonify({"status": "erro", "mensagem": response.text}), 500
    except Exception as e:
        print("Erro ao enviar para o Telegram:", e)
        return jsonify({"status": "erro", "mensagem": str(e)}), 500



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

