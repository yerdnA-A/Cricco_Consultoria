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

    # Monta a mensagem simples (sem Markdown problemático)
    mensagem = (
        "📋 Nova Cotação Recebida!\n"
        "--------------------------\n"
        f"Nome: {dados.get('nome')}\n"
        f"WhatsApp: {dados.get('whatsapp')}\n"
        f"Email: {dados.get('email')}\n"
        f"Administradora: {dados.get('administradora')}\n"
        f"Valor da Carta: R$ {dados.get('valor_carta')}\n"
        f"Valor Pago: R$ {dados.get('valor_pago')}\n"
        f"Status: {dados.get('status_carta').replace('_', ' ').title()}\n"
    )

    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID_VENDEDOR,
        "text": mensagem
    }

    try:
        response = requests.post(url, json=payload)
        response_data = response.json()
        print("Resposta Telegram:", response_data)

        if response.status_code == 200 and response_data.get("ok"):
            return jsonify({"status": "sucesso", "mensagem": "Cotação enviada pelo Telegram!"})
        else:
            return jsonify({"status": "erro", "mensagem": response_data}), 500
    except Exception as e:
        print("Erro ao enviar para o Telegram:", e)
        return jsonify({"status": "erro", "mensagem": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
