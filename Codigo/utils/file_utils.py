import os

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

def get_valid_files(arquivos, base_dir):
    """Verifica quais arquivos existem no diretório base e retorna uma lista dos válidos."""
    valid_files = []
    for arquivo in arquivos:
        full_path = os.path.join(base_dir, arquivo)
        if os.path.exists(full_path):
            valid_files.append(arquivo)
        else:
            print(f"Aviso: O arquivo {full_path} não existe.")
    return valid_files
