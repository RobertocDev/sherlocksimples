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

    # Retornar os resultados
    if results:
        response = jsonify({"status": "success", "sites": results})
        response.headers['Content-Type'] = 'application/json'  # Forçar o tipo de conteúdo
        return response
    else:
        response = jsonify({"status": "error", "message": f"Nenhum resultado encontrado para o usuário '{username}'."})
        response.headers['Content-Type'] = 'application/json'  # Forçar o tipo de conteúdo
        return response, 404

# Executa a aplicação Flask
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
