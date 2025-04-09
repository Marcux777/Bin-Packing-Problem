def create_data(arquivo):
    """
    Processa um arquivo de instância e extrai os dados necessários.

    Args:
        arquivo (str): Nome do arquivo de instância a ser processado

    Returns:
        dict: Dicionário contendo os dados processados
    """
    caminho = f"/workspaces/Bin-Paking-Problem/Instances/{arquivo}"
    with open(caminho, "r") as file:
        # Filtrar apenas as linhas não vazias que iniciam com dígitos ou sinal negativo
        linhas = [linha.strip() for linha in file.readlines() if linha.strip() and (linha.strip()[0].isdigit() or linha.strip()[0] == '-')]

    # Primeira linha: número de itens (N)
    n = int(linhas[0])

    # Segunda linha: capacidade do contêiner
    bin_capacity = int(linhas[1])

    # Das linhas restantes, extraímos os pesos dos itens
    weights = []
    for i in range(2, 2+n):
        if i < len(linhas):
            weights.append(int(linhas[i]))

    data = {
        "num_items": n,
        "bin_capacity": bin_capacity,
        "weights": weights
    }
    return data
