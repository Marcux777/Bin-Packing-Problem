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

    # Primeira linha: número de itens (m)
    m = int(linhas[0])

    # Segunda linha: dimensões do contêiner/bin (W H)
    bin_info = linhas[1].split()
    bin_width, bin_height = int(bin_info[0]), int(bin_info[1])

    # Define a capacidade do bin: se H for -1, utiliza apenas W; caso contrário, W * H
    if bin_height == -1:
        bin_capacity = bin_width
    else:
        bin_capacity = bin_width * bin_height

    # Das linhas restantes, extraímos somente o peso do item (w_i)
    weights = []
    for linha in linhas[2:]:
        dados = linha.split()
        if len(dados) >= 6:
            # dados: item_id, w_i, h_i, d_i, b_i, p_i
            w_i = int(dados[1])
            weights.append(w_i)

    data = {
        "num_items": m,
        "bin_width": bin_width,
        "bin_height": bin_height,
        "bin_capacity": bin_capacity,
        "weights": weights
    }
    return data
