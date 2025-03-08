from flask import Flask, jsonify
import requests

app = Flask(__name__)

# Dicionário com os sites que você deseja verificar
SITES = {
    "Twitter": "https://twitter.com/{}",
    "Instagram": "https://www.instagram.com/{}",
    "GitHub": "https://github.com/{}",
    "Reddit": "https://www.reddit.com/user/{}",
    "YouTube": "https://www.youtube.com/{}",
    "Facebook": "https://www.facebook.com/{}"
}

@app.route('/check/<username>', methods=['GET'])
def check_username(username):
    results = {}

    for site, url in SITES.items():
        profile_url = url.format(username)
        response = requests.get(profile_url)

        # Se o status for 200, significa que a conta existe
        if response.status_code == 200:
            results[site] = {"status": "✅ Encontrado", "url": profile_url}
        else:
            results[site] = {"status": "❌ Não encontrado", "url": None}

    return jsonify(results)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
