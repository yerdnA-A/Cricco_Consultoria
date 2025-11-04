from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # permite requisições do front-end

@app.route("/api/cotacao", methods=["POST"])
def receber_cotacao():
    dados = request.get_json()
    print("Dados recebidos:", dados)
    
    # Aqui você pode salvar num arquivo, banco de dados, etc.
    # Exemplo simples: salva em um arquivo local
    with open("dados.json", "a", encoding="utf-8") as f:
        f.write(str(dados) + "\n")

    return jsonify({"status": "ok", "mensagem": "Dados recebidos com sucesso!"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
