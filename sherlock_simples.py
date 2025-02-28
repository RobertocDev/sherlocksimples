import os
import json
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

TYPEBOT_API_URL = "https://typebot.io/api/message"  # Substitua pela URL correta
TYPEBOT_API_KEY = os.getenv("TYPEBOT_API_KEY")  # Defina essa variável de ambiente


def verificar_usuario(username):
    """
    Verifica se o username existe nas plataformas usando o Sherlock.
    """
    resultado = {}
    try:
        resposta = os.popen(f"python3 sherlock/sherlock.py {username} --json").read()
        resultado = json.loads(resposta)
    except Exception as e:
        resultado = {"erro": str(e)}
    return resultado


def enviar_resposta_typebot(mensagem):
    """
    Envia a resposta para o Typebot.
    """
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {TYPEBOT_API_KEY}"
    }
    payload = {"message": mensagem}
    try:
        response = requests.post(TYPEBOT_API_URL, headers=headers, json=payload)
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"erro": str(e)}


@app.route("/sherlock", methods=["GET"])
def sherlock():
    username = request.args.get("username")
    if not username:
        return jsonify({"erro": "Username não fornecido"}), 400
    
    resultado = verificar_usuario(username)
    resposta_typebot = enviar_resposta_typebot(resultado)
    
    return jsonify({"resultado": resultado, "typebot": resposta_typebot})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
