# config.py
"""
Arquivo de configuração para os algoritmos de Bin Packing.

Este módulo centraliza os parâmetros configuráveis dos algoritmos
de resolução do problema de Bin Packing, permitindo ajustes fáceis
sem necessidade de modificar o código-fonte.
"""

# Configurações gerais
DEFAULT_INSTANCES = [
    "Scholl/Scholl_3/HARD0.txt",
    "Scholl/Scholl_3/HARD1.txt",
    "Scholl/Scholl_3/HARD2.txt",
    "Scholl/Scholl_3/HARD3.txt",
    "Scholl/Scholl_3/HARD4.txt",
    "Scholl/Scholl_3/HARD5.txt",
]

INSTANCES_DIR = "/workspaces/Bin-Paking-Problem/Instances"

# Configurações para o algoritmo GGA (Grouping Genetic Algorithm)
GGA_CONFIG = {
    'population_size': 100,      # Tamanho da população
    'crossover_rate': 0.8,       # Taxa de crossover
    'mutation_rate': 0.1,        # Taxa de mutação
    'num_generations': 100,      # Número de gerações
    'elite_size': 5,             # Número de indivíduos elite mantidos entre gerações
    'selection_tournament_size': 3,  # Tamanho do torneio para seleção
}

# Configurações para o algoritmo Tabu Search
TABU_CONFIG = {
    'tabu_list_size': 10,       # Tamanho da lista tabu
    'max_iterations': 1000,     # Número máximo de iterações
    'max_iterations_no_improve': 100,  # Número máximo de iterações sem melhoria
    'neighborhood_size': 20,    # Tamanho da vizinhança a explorar em cada iteração
}

# Configurações de visualização
VISUALIZATION_CONFIG = {
    'show_plots': True,          # Mostrar gráficos de resultados
    'save_plots': True,          # Salvar gráficos em arquivos
    'plots_directory': '/workspaces/Bin-Paking-Problem/resultados',  # Diretório para salvar gráficos
    'plot_format': 'png',        # Formato dos gráficos (png, pdf, svg, etc.)
}
