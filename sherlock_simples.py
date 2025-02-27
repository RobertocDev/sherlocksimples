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
