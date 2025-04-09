import sys
import os

# Adicionar o diretório atual ao sys.path para que o Python encontre os módulos
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from concurrent.futures import ProcessPoolExecutor, as_completed
from models.container import Container
from algorithms.gga import GGA
from algorithms.tabu_search import Tabu_Search
from utils.data_processor import create_data
from utils.file_utils import list_directory_files, get_valid_files
import argparse
from result_display import display_solution

def process_instance(arquivo):
    """
    Processa uma instância do problema do bin packing usando o GGA.

    Args:
        arquivo (str): O nome do arquivo de instância a ser processado.

    Returns:
        tuple: Uma tupla contendo o nome do arquivo, a melhor solução encontrada e o tempo de execução.
    """
    import time
    start_time = time.time()

    data = create_data(arquivo)
    gga = GGA(data)
    best_solution = gga.run()

    execute_time = time.time() - start_time
    return arquivo, best_solution, execute_time

def main():
    # Configurar argumentos de linha de comando
    parser = argparse.ArgumentParser(description='Resolver o problema de bin packing')
    parser.add_argument('--files', nargs='+', help='Lista de arquivos de instância para processar')
    parser.add_argument('--list', action='store_true', help='Listar arquivos disponíveis')
    args = parser.parse_args()

    # Pasta base de instâncias
    instances_dir = "/workspaces/Bin-Paking-Problem/Instances"

    # Listar apenas os arquivos disponíveis se solicitado
    if args.list:
        print("\nArquivos disponíveis na pasta de instâncias:")
        list_directory_files(instances_dir)
        return

    # Lista de instâncias para processar
    arquivos = args.files if args.files else [
        "Scholl/Scholl_3/HARD0.txt",
        "Scholl/Scholl_3/HARD1.txt",
        "Scholl/Scholl_3/HARD2.txt",
        "Scholl/Scholl_3/HARD3.txt",
        "Scholl/Scholl_3/HARD4.txt",
        "Scholl/Scholl_3/HARD5.txt",
    ]

    # Verificar se os arquivos existem
    valid_files = get_valid_files(arquivos, instances_dir)

    if not valid_files:
        print("Nenhum arquivo válido encontrado. Verifique o diretório de instâncias.")
        print("\nArquivos disponíveis na pasta de instâncias:")
        list_directory_files(instances_dir)
        return

    print(f"\nProcessando {len(valid_files)} arquivos válidos...\n")

    with ProcessPoolExecutor() as executor:
        future_to_file = {executor.submit(process_instance, arquivo): arquivo for arquivo in valid_files}

        for future in as_completed(future_to_file):
            arquivo = future_to_file[future]
            try:
                arquivo, best_solution, execute_time = future.result()
                display_solution(arquivo, best_solution, execute_time)
            except ZeroDivisionError as zde:
                print(f"{arquivo} gerou uma exceção de divisão por zero: {zde}")
            except Exception as exc:
                print(f"{arquivo} gerou uma exceção: {exc}")

if __name__ == "__main__":
    main()
