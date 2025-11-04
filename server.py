from flask import Flask, request, jsonify
from flask_cors import CORS
import psycopg2
import os

app = Flask(__name__)
CORS(app)

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise RuntimeError("❌ DATABASE_URL não configurada! Configure-a nas variáveis do Render.")

def get_connection():
    return psycopg2.connect(DATABASE_URL)

# Criar tabela caso ainda não exista
try:
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS cotacoes (
                    id SERIAL PRIMARY KEY,
                    nome TEXT,
                    email TEXT,
                    telefone TEXT,
                    mensagem TEXT,
                    criado_em TIMESTAMP DEFAULT NOW()
                )
            """)
            conn.commit()
except Exception as e:
    print("⚠️ Erro ao criar tabela:", e)


@app.route("/api/cotacao", methods=["POST"])
def receber_cotacao():
    dados = request.get_json()
    print("Dados recebidos:", dados)

    nome = dados.get("nome")
    email = dados.get("email")
    telefone = dados.get("telefone")
    mensagem = dados.get("mensagem")

    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO cotacoes (nome, email, telefone, mensagem)
            VALUES (%s, %s, %s, %s)
        """, (nome, email, telefone, mensagem))
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({"status": "ok", "mensagem": "Cotação salva no banco com sucesso!"})
    except Exception as e:
        print("Erro ao salvar no banco:", e)
        return jsonify({"status": "erro", "mensagem": str(e)}), 500

@app.route("/api/dados", methods=["GET"])
def listar_dados():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, nome, email, telefone, mensagem, criado_em FROM cotacoes ORDER BY criado_em DESC")
    registros = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify([
        {"id": r[0], "nome": r[1], "email": r[2], "telefone": r[3], "mensagem": r[4], "criado_em": r[5].isoformat()}
        for r in registros
    ])

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
