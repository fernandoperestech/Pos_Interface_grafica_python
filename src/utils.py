def validar_preco(preco):
    try:
        return float(preco) > 0
    except ValueError:
        return False

def validar_campos_obrigatorios(campos):
    return all(campos.values())
