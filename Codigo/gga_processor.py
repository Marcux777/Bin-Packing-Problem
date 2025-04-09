import time as t
from GGA import GGA
from data_processor import create_data

def process_instance(arquivo):
    """
    Processa uma instância, executa o algoritmo GGA e retorna os resultados.

    Args:
        arquivo (str): Nome do arquivo de instância a ser processado

    Returns:
        tuple: (nome_arquivo, melhor_solução, tempo_execução)
    """
    start_time = t.time()
    data = create_data(arquivo)
    gga = GGA(data)
    best_solution = gga.run()
    end_time = t.time()
    # Retornar também o nome do arquivo
    return arquivo, best_solution, end_time - start_time
