from models.container import Container
import os
import sys
import os.path

# Adicionar o diretório Codigo ao path para importação do config e utils
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from utils.visualization import (create_convergence_plot, visualize_bin_packing,
                              ensure_visualization_directory)
from config import VISUALIZATION_CONFIG

def display_solution(arquivo, solution, execution_time, algorithm_obj=None):
    """
    Exibe os resultados da solução de uma instância do problema e gera visualizações.

    Args:
        arquivo (str): Nome do arquivo da instância
        solution (list): Lista de contêineres na solução
        execution_time (float): Tempo de execução em segundos
        algorithm_obj (object, optional): Objeto do algoritmo que contém histórico de execução
    """
    # Exibir informações textuais sobre a solução
    print(f"\nMelhor solução encontrada para {arquivo}:")
    print("=" * 100)
    for i, container in enumerate(solution, 1):
        print(f"Contêiner {i}: {container}")
    print("=" * 100)
    print("Quantidade de contêineres usados: ", len(solution))
    print("=" * 100)
    print("Tempo total de solução: {:.2f} segundos".format(execution_time))
    print("=" * 100)

    # Verificar se a visualização está habilitada
    if not VISUALIZATION_CONFIG.get('show_plots', True) and not VISUALIZATION_CONFIG.get('save_plots', True):
        return

    # Garantir que o diretório para salvar as visualizações exista
    plots_dir = ensure_visualization_directory()

    # Extrair o nome da instância do caminho do arquivo
    instance_name = os.path.basename(arquivo).split('.')[0]

    # Gerar visualização da ocupação dos bins
    if VISUALIZATION_CONFIG.get('save_plots', True):
        bin_plot_path = os.path.join(plots_dir, f"{instance_name}_bin_packing.{VISUALIZATION_CONFIG.get('plot_format', 'png')}")
    else:
        bin_plot_path = None

    visualize_bin_packing(solution,
                        title=f"Solução Bin Packing - {instance_name}",
                        save_path=bin_plot_path)

    # Se o objeto do algoritmo estiver disponível e tiver histórico, gerar gráfico de convergência
    if algorithm_obj and hasattr(algorithm_obj, 'history') and algorithm_obj.history.get('generation'):
        if VISUALIZATION_CONFIG.get('save_plots', True):
            convergence_plot_path = os.path.join(plots_dir, f"{instance_name}_convergence.{VISUALIZATION_CONFIG.get('plot_format', 'png')}")
        else:
            convergence_plot_path = None

        create_convergence_plot(algorithm_obj.history,
                             instance_name,
                             save_path=convergence_plot_path)
