"""
Módulo principal para execução do problema de Bin Packing.

Este módulo implementa a solução para o problema de Bin Packing usando
diferentes algoritmos como GGA (Grouping Genetic Algorithm) e Tabu Search.
O programa pode processar múltiplas instâncias do problema paralelamente e
exibir os resultados obtidos.

O módulo oferece as seguintes funcionalidades:
- Processamento de instâncias específicas ou instâncias padrão
- Execução paralela para melhor performance
- Listagem de instâncias disponíveis
- Exibição formatada de resultados
"""

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
from config import DEFAULT_INSTANCES, INSTANCES_DIR

def process_instance(arquivo):
    """
    Processa uma instância do problema do bin packing usando o algoritmo GGA.

    Esta função carrega os dados do arquivo de instância, cria um objeto GGA
    e executa o algoritmo para encontrar a melhor solução. O tempo de execução
    é medido para avaliação de performance.

    Args:
        arquivo (str): O caminho do arquivo de instância a ser processado.

    Returns:
        tuple: Uma tupla contendo (nome do arquivo, melhor solução encontrada, tempo de execução, objeto do algoritmo).
            - nome do arquivo (str): Nome da instância processada
            - melhor solução (list): Lista de containers com a melhor solução encontrada
            - tempo de execução (float): Tempo em segundos gasto para encontrar a solução
            - objeto do algoritmo (GGA): A instância do algoritmo usado para resolver o problema

    Raises:
        Exception: Se ocorrer erro durante o processamento da instância
    """
    import time
    start_time = time.time()

    data = create_data(arquivo)
    gga = GGA(data)
    best_solution = gga.run()

    execute_time = time.time() - start_time
    return arquivo, best_solution, execute_time, gga

def main():
    """
    Função principal do programa.

    Processa os argumentos da linha de comando, configura as instâncias
    a serem executadas e gerencia a execução paralela do processamento.
    Suporta listagem de arquivos disponíveis e seleção específica de
    instâncias para processamento.

    Returns:
        None
    """
    # Configurar argumentos de linha de comando
    parser = argparse.ArgumentParser(description='Resolver o problema de bin packing')
    parser.add_argument('--files', nargs='+', help='Lista de arquivos de instância para processar')
    parser.add_argument('--list', action='store_true', help='Listar arquivos disponíveis')
    parser.add_argument('--parallel', action='store_true', help='Executar em paralelo (default: False)')
    args = parser.parse_args()

    # Listar apenas os arquivos disponíveis se solicitado
    if args.list:
        print("\nArquivos disponíveis na pasta de instâncias:")
        list_directory_files(INSTANCES_DIR)
        return

    # Lista de instâncias para processar
    arquivos = args.files if args.files else DEFAULT_INSTANCES

    # Verificar se os arquivos existem
    valid_files = get_valid_files(arquivos, INSTANCES_DIR)

    if not valid_files:
        print("Nenhum arquivo válido encontrado. Verifique o diretório de instâncias.")
        print("\nArquivos disponíveis na pasta de instâncias:")
        list_directory_files(INSTANCES_DIR)
        return

    print(f"\nProcessando {len(valid_files)} arquivos válidos...\n")

    # Decidir se executa em paralelo ou sequencialmente
    if args.parallel:
        # Execução paralela
        with ProcessPoolExecutor() as executor:
            future_to_file = {executor.submit(process_instance, arquivo): arquivo for arquivo in valid_files}

            for future in as_completed(future_to_file):
                arquivo = future_to_file[future]
                try:
                    arquivo, best_solution, execute_time, gga = future.result()
                    display_solution(arquivo, best_solution, execute_time, gga)
                except ZeroDivisionError as zde:
                    print(f"{arquivo} gerou uma exceção de divisão por zero: {zde}")
                except Exception as exc:
                    print(f"{arquivo} gerou uma exceção: {exc}")
    else:
        # Execução sequencial
        for arquivo in valid_files:
            try:
                arquivo, best_solution, execute_time, gga = process_instance(arquivo)
                display_solution(arquivo, best_solution, execute_time, gga)
            except Exception as exc:
                print(f"{arquivo} gerou uma exceção: {exc}")

if __name__ == "__main__":
    main()
