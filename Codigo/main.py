from concurrent.futures import ProcessPoolExecutor, as_completed
from gga_processor import process_instance
import os

def main():
    # Pasta base de instâncias
    instances_dir = "/workspaces/Bin-Paking-Problem/Instances"

    # Lista de instâncias para processar
    arquivos = [
        "CLASS/cl_01_040_07.ins2D", "CLASS/cl_01_040_08.ins2D", "CLASS/cl_01_040_09.ins2D",
    ]

    # Verificar se os arquivos existem
    valid_files = []
    for arquivo in arquivos:
        full_path = os.path.join(instances_dir, arquivo)
        if os.path.exists(full_path):
            valid_files.append(arquivo)
        else:
            print(f"Aviso: O arquivo {full_path} não existe.")

    if not valid_files:
        print("Nenhum arquivo válido encontrado. Verifique o diretório de instâncias.")
        return

    # Listar os arquivos disponíveis no diretório (para ajudar o usuário)
    print("\nArquivos disponíveis na pasta de instâncias:")
    list_directory_files(instances_dir)

    print(f"\nProcessando {len(valid_files)} arquivos válidos...\n")

    with ProcessPoolExecutor() as executor:
        future_to_file = {executor.submit(process_instance, arquivo): arquivo for arquivo in valid_files}

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

def list_directory_files(directory):
    """Lista os arquivos em um diretório e seus subdiretórios."""
    try:
        for root, dirs, files in os.walk(directory):
            if files:
                rel_path = os.path.relpath(root, directory)
                if rel_path == ".":
                    print(f"  - Pasta raiz: {', '.join(files)}")
                else:
                    print(f"  - {rel_path}: {', '.join(files)}")
    except Exception as e:
        print(f"Erro ao listar diretório: {e}")

if __name__ == "__main__":
    main()
