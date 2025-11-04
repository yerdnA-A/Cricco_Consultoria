from flask import Flask, request, jsonify
from twilio.rest import Client
import os

app = Flask(__name__)

# ✅ Coloque suas credenciais do Twilio
TWILIO_ACCOUNT_SID = "SEU_ACCOUNT_SID"
TWILIO_AUTH_TOKEN = "SEU_AUTH_TOKEN"
TWILIO_WHATSAPP_NUMBER = "whatsapp:+14155238886"  # Número padrão do sandbox
VENDEDOR_WHATSAPP = "whatsapp:+55XXXXXXXXXXX"  # Número do vendedor (com DDI)

client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

@app.route("/api/cotacao", methods=["POST"])
def receber_cotacao():
    dados = request.get_json()

    # Monta a mensagem com as informações do formulário
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

    try:
        # Envia a mensagem via WhatsApp para o vendedor
        client.messages.create(
            from_=TWILIO_WHATSAPP_NUMBER,
            body=mensagem,
            to=VENDEDOR_WHATSAPP
        )

        return jsonify({"status": "sucesso", "mensagem": "Cotação enviada com sucesso!"})
    except Exception as e:
        print("Erro ao enviar WhatsApp:", e)
        return jsonify({"status": "erro", "mensagem": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
