import requests

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

def main():
    username = input("Digite o nome de usuário: ")
    results = []

    for site in SITES:
        result = check_username(username, site)
        if result["exists"]:
            results.append(result)

    if results:
        print(f"Resultados para {username}:")
        for result in results:
            print(f"- {result['site']}: {result['url']}")
    else:
        print(f"Nenhum resultado encontrado para o usuário '{username}'.")

if __name__ == '__main__':
    main()