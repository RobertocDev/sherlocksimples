from sherlock import sherlock

def verificar_usuario(username):
    """
    Verifica se o username existe nas plataformas usando o Sherlock.
    """
    resultado = {}
    try:
        # Usando o Sherlock como uma biblioteca
        sherlock_results = sherlock.sherlock(username)
        resultado = {site: data for site, data in sherlock_results.items()}
    except Exception as e:
        resultado = {"erro": str(e)}
    return resultado
