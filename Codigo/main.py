from concurrent.futures import ProcessPoolExecutor, as_completed
from gga_processor import process_instance
import os
import argparse
from result_display import display_solution
from file_utils import list_directory_files, get_valid_files

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
        "CLASS/cl_01_040_07.ins2D",
        "CLASS/cl_01_040_08.ins2D",
        "CLASS/cl_01_040_09.ins2D",
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
            except Exception as exc:
                print(f"{arquivo} gerou uma exceção: {exc}")

if __name__ == "__main__":
    main()
