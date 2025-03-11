from flask import Flask, jsonify
import requests

app = Flask(__name__)

# Dicionário com os sites que você deseja verificar
SITES = {
    "YouTube": "https://www.youtube.com/{}",
    "Facebook": "https://www.facebook.com/{}",
    "Twitter": "https://twitter.com/{}",
    "Instagram": "https://www.instagram.com/{}",
    "TikTok": "https://www.tiktok.com/@{}",
    "Reddit": "https://www.reddit.com/user/{}",
    "LinkedIn": "https://www.linkedin.com/in/{}",
    "Spotify": "https://open.spotify.com/user/{}",
    "Telegram": "https://t.me/{}",
    "Twitch": "https://www.twitch.tv/{}",
    "Pinterest": "https://www.pinterest.com/{}",
    "GitHub": "https://github.com/{}",
    "Snapchat": "https://www.snapchat.com/add/{}",
    "Quora": "https://www.quora.com/profile/{}",
    "Steam": "https://steamcommunity.com/id/{}",
    "SoundCloud": "https://soundcloud.com/{}",
    "Gravatar": "https://www.gravatar.com/{}",
    "Kwai": "https://www.kwai.com/{}",
    "Flickr": "https://www.flickr.com/photos/{}",
    "Medium": "https://medium.com/@{}",
    "Substack": "https://{}.substack.com",
    "Trello": "https://trello.com/{}",
    "Tumblr": "https://tumblr.com/{}",
    "Blogger": "https://{}.blogspot.com",
    "Dailymotion": "https://www.dailymotion.com/{}",
    "Catarse": "https://www.catarse.me/{}",
    "Tenor": "https://tenor.com/users/{}",
    "Vimeo": "https://vimeo.com/{}"
}

# Função que pega todas as URLs encontradas e junta em um único texto
def get_all_urls(results):
    urls = []
    for site, data in results.items():
        if data['status'] == "✅ Encontrado" and data['url']:
            urls.append(data['url'])
    
    # Retorna todas as URLs juntas em uma string separada por nova linha
    return "\n".join(urls) if urls else "Nenhum perfil encontrado."

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

    # Agora vamos pegar todas as URLs encontradas e juntá-las
    all_urls = get_all_urls(results)

    # Retornar a resposta com as URLs combinadas em um único texto
    return jsonify({"result": all_urls})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
