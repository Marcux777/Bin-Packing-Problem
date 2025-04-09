from GGA import GGA
import time as t
from concurrent.futures import ProcessPoolExecutor, as_completed


def create_data(Arquivo):
    caminho = f"/workspaces/Heuristicas/Bin Packing Problem/Instances/{Arquivo}"
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

def process_instance(Arquivo):
    start_time = t.time()
    data = create_data(Arquivo)
    gga = GGA(data)
    best_solution = gga.run()
    end_time = t.time()
    # Retornar também o nome do arquivo
    return Arquivo, best_solution, end_time - start_time


def main():
    arquivos = [
        "CLASS/cl_01_040_07.ins2D", "CLASS/cl_01_040_08.ins2D", "CLASS/cl_01_040_09.ins2D",
    ]

    with ProcessPoolExecutor() as executor:
        future_to_file = {executor.submit(process_instance, arquivo): arquivo for arquivo in arquivos}

        for future in as_completed(future_to_file):
            arquivo = future_to_file[future]
            try:
                arquivo, best_solution, execute_time = future.result()
                print(f"\nMelhor solução encontrada para {arquivo}:")
                print("=" * 100)
                for i, container in enumerate(best_solution, 1):
                    print(f"Contêiner {i}: {container}")
                print("=" * 100)
                print("Quantidade de contêineres usados: ", len(best_solution))
                print("=" * 100)
                print("Tempo total de solução: {:.2f} segundos".format(execute_time))
                print("=" * 100)
            except Exception as exc:
                print(f"{arquivo} gerou uma exceção: {exc}")

if __name__ == "__main__":
    main()
