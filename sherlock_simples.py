from flask import Flask, request, jsonify
import requests

# Cria a instância do Flask
app = Flask(__name__)

# Lista de sites para verificar
SITES = [
    {"name": "Twitter", "url": "https://twitter.com/{}"},
    {"name": "Instagram", "url": "https://instagram.com/{}"},
    {"name": "GitHub", "url": "https://github.com/{}"},
    {"name": "Reddit", "url": "https://reddit.com/user/{}"},
    {"name": "YouTube", "url": "https://youtube.com/{}"},
    {"name": "Facebook", "url": "https://facebook.com/{}"}
]

TYPEBOT_API_URL = "https://api.typebot.io/v1/message/send"  # Endpoint da API Typebot
TYPEBOT_API_KEY = "your_typebot_api_key"  # Substitua com a chave de API do seu Typebot

def send_message_to_typebot(message):
    """
    Envia uma mensagem para o Typebot.
    """
    payload = {
        "bot_id": "your_bot_id",  # Substitua com o ID do seu bot
        "message": message,
    }
    headers = {
        "Authorization": f"Bearer {TYPEBOT_API_KEY}",
        "Content-Type": "application/json",
    }
    response = requests.post(TYPEBOT_API_URL, json=payload, headers=headers)
    return response.json()

def check_username(username, site):
    """
    Verifica se o nome de usuário existe no site.
    """
    url = site["url"].format(username)
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            return {"site": site["name"], "url": url, "exists": True}
        else:
            return {"site": site["name"], "url": url, "exists": False}
    except requests.exceptions.RequestException:
        return {"site": site["name"], "url": url, "exists": False}

@app.route('/sherlock', methods=['GET'])
def sherlock():
    # Pegar o nome de usuário da requisição
    username = request.args.get('username')
    if not username:
        return jsonify({"error": "Por favor, forneça um nome de usuário."}), 400

    # Verificar o nome de usuário em cada site
    results = []
    for site in SITES:
        result = check_username(username, site)
        if result["exists"]:
            formatted_result = f"{result['site']}: {result['url']}"
            results.append(formatted_result)

    # Enviar mensagem para o Typebot
    if results:
        message = f"Usuário '{username}' encontrado nos seguintes sites:\n" + "\n".join(results)
        send_message_to_typebot(message)
        response = jsonify({"status": "success", "sites": results})
        response.headers['Content-Type'] = 'application/json'  # Forçar o tipo de conteúdo
        return response
    else:
        message = f"Nenhum resultado encontrado para o usuário '{username}'."
        send_message_to_typebot(message)
        response = jsonify({"status": "error", "message": message})
        response.headers['Content-Type'] = 'application/json'  # Forçar o tipo de conteúdo
        return response, 404

# Executa a aplicação Flask
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
