from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Lista de sites para verificar
SITES = [
    {"name": "Twitter", "url": "https://twitter.com/{}"},
    {"name": "Instagram", "url": "https://instagram.com/{}"},
    {"name": "GitHub", "url": "https://github.com/{}"},
    {"name": "Reddit", "url": "https://reddit.com/user/{}"},
    {"name": "YouTube", "url": "https://youtube.com/{}"},
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
            results.append({"site": site["name"], "url": result["url"]})

    # Retornar os resultados
    if results:
        return jsonify(results)
    else:
        return jsonify({"error": f"Nenhum resultado encontrado para o usuário '{username}'."}), 404

if __name__ == '__main__':
    # Rodar a API na porta 5000
    app.run(host='0.0.0.0', port=5000)
