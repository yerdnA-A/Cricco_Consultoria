from twilio.rest import Client
import os
from dotenv import load_dotenv

# Carrega as variáveis do .env
load_dotenv()

# Configurações do Twilio
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_WHATSAPP_NUMBER = os.getenv("TWILIO_WHATSAPP_NUMBER")  # Ex: whatsapp:+14155238886
VENDEDOR_WHATSAPP = os.getenv("VENDEDOR_WHATSAPP")  # Ex: whatsapp:+55SEUNUMERO

# Cria o cliente
client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

# Teste de envio
try:
    mensagem = client.messages.create(
        from_=TWILIO_WHATSAPP_NUMBER,
        body="✅ Teste de envio via Twilio WhatsApp Sandbox!",
        to=VENDEDOR_WHATSAPP
    )
    print("Mensagem enviada com sucesso!")
    print("SID da mensagem:", mensagem.sid)
except Exception as e:
    print("❌ Erro ao enviar mensagem:", e)
