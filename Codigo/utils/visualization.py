"""
Módulo para visualização de resultados do problema de Bin Packing.

Este módulo implementa funções para gerar visualizações gráficas dos resultados
dos algoritmos de otimização, permitindo uma melhor compreensão e análise
do desempenho e das soluções encontradas.
"""

import matplotlib.pyplot as plt
import numpy as np
import os
from config import VISUALIZATION_CONFIG
import seaborn as sns


def create_convergence_plot(history, instance_name, save_path=None):
    """
    Cria um gráfico de convergência mostrando a evolução do fitness ao longo das gerações.

    Args:
        history (dict): Dicionário contendo listas de 'best_fitness', 'avg_fitness' e 'generation'
        instance_name (str): Nome da instância para o título do gráfico
        save_path (str, optional): Caminho para salvar o gráfico. Se None, não salva.
    """
    plt.figure(figsize=(10, 6))

    # Configuração de estilo
    sns.set_style("whitegrid")

    # Plotar fitness médio e melhor fitness
    plt.plot(history['generation'], history['best_fitness'],
             'b-', linewidth=2, label='Melhor Fitness')
    plt.plot(history['generation'], history['avg_fitness'],
             'r--', linewidth=1.5, label='Fitness Médio')

    # Configuração do gráfico
    plt.title(f'Evolução do Fitness - Instância: {instance_name}')
    plt.xlabel('Geração')
    plt.ylabel('Fitness (menor é melhor)')
    plt.legend()
    plt.grid(True)

    # Salvar o gráfico se o caminho for fornecido
    if save_path:
        plt.savefig(save_path, bbox_inches='tight', dpi=300)
        print(f"Gráfico salvo em: {save_path}")

    if VISUALIZATION_CONFIG.get('show_plots', True):
        plt.show()

    plt.close()


def visualize_bin_packing(solution, title="Solução de Bin Packing", save_path=None):
    """
    Cria uma visualização gráfica da solução de bin packing.

    Args:
        solution (list): Lista de containers (bins) com seus elementos
        title (str): Título do gráfico
        save_path (str, optional): Caminho para salvar o gráfico. Se None, não salva.
    """
    num_bins = len(solution)
    if num_bins == 0:
        print("Nenhum bin para visualizar")
        return

    # Configurações de tamanho e estilo
    plt.figure(figsize=(12, 8))
    sns.set_style("whitegrid")

    # Calcular altura máxima para cada bin (normalizado pela capacidade)
    bin_capacities = [container.capacity for container in solution]
    max_capacity = max(bin_capacities)

    # Configurar largura das barras e espaçamentos
    bar_width = 0.8
    bin_positions = np.arange(num_bins)

    # Para cada bin, plotar os itens como barras empilhadas
    bottom = np.zeros(num_bins)

    # Criar uma paleta de cores
    colors = plt.cm.viridis(np.linspace(0, 1, 10))

    # Agrupar elementos por tamanho para visualização
    size_groups = {}
    for i, container in enumerate(solution):
        for item in container.elements:
            if item not in size_groups:
                size_groups[item] = []
            size_groups[item].append((i, item))

    # Ordenar os grupos por tamanho para a legenda
    sorted_sizes = sorted(size_groups.keys(), reverse=True)

    # Plotar os itens agrupados por tamanho
    for i, size in enumerate(sorted_sizes):
        bin_indices = []
        heights = []

        for bin_idx, height in size_groups[size]:
            bin_indices.append(bin_idx)
            heights.append(height)

        color_idx = i % len(colors)
        for bin_idx, height in zip(bin_indices, heights):
            plt.bar(bin_positions[bin_idx], height, bar_width,
                   bottom=bottom[bin_idx], color=colors[color_idx],
                   edgecolor='white', linewidth=0.5)
            bottom[bin_idx] += height

    # Adicionar linha de capacidade máxima dos bins
    plt.axhline(y=max_capacity, color='r', linestyle='--',
               label='Capacidade Máxima')

    # Configurações finais do gráfico
    plt.title(title)
    plt.xlabel('Número do Bin')
    plt.ylabel('Ocupação')
    plt.xticks(bin_positions, [f'Bin {i+1}' for i in range(num_bins)])
    plt.ylim(0, max_capacity * 1.1)  # Deixar um espaço acima da capacidade máxima

    plt.legend(['Capacidade Máxima'] + [f'Item {size}' for size in sorted_sizes[:10]] +
              (['Outros tamanhos'] if len(sorted_sizes) > 10 else []))

    plt.tight_layout()

    # Salvar o gráfico se o caminho for fornecido
    if save_path:
        plt.savefig(save_path, bbox_inches='tight', dpi=300)
        print(f"Visualização da solução salva em: {save_path}")

    if VISUALIZATION_CONFIG.get('show_plots', True):
        plt.show()

    plt.close()


def visualize_bin_comparison(original_solution, improved_solution,
                            title="Comparação de Soluções", save_path=None):
    """
    Compara visualmente duas soluções de bin packing (original vs melhorada).

    Args:
        original_solution (list): Lista de containers da solução original
        improved_solution (list): Lista de containers da solução melhorada
        title (str): Título do gráfico
        save_path (str, optional): Caminho para salvar o gráfico. Se None, não salva.
    """
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(18, 8))

    # Configuração de estilo
    sns.set_style("whitegrid")

    # Função auxiliar para plotar uma solução em um eixo específico
    def plot_solution(solution, ax, title):
        num_bins = len(solution)
        bin_capacities = [container.capacity for container in solution]
        max_capacity = max(bin_capacities)

        # Configurar largura das barras e espaçamentos
        bar_width = 0.8
        bin_positions = np.arange(num_bins)

        # Para cada bin, plotar os itens como barras empilhadas
        bottom = np.zeros(num_bins)

        # Criar uma paleta de cores única para os dois gráficos
        colors = plt.cm.viridis(np.linspace(0, 1, 20))

        # Ordenar os bins por preenchimento (mais cheios primeiro)
        sorted_indices = sorted(range(num_bins),
                               key=lambda i: solution[i].used,
                               reverse=True)
        sorted_solution = [solution[i] for i in sorted_indices]

        # Plotar cada item dentro de cada bin
        for bin_idx, container in enumerate(sorted_solution):
            for item_idx, item in enumerate(container.elements):
                color_idx = item % len(colors)
                ax.bar(bin_positions[bin_idx], item, bar_width,
                      bottom=bottom[bin_idx], color=colors[color_idx],
                      edgecolor='white', linewidth=0.5)
                bottom[bin_idx] += item

        # Adicionar linha de capacidade máxima dos bins
        ax.axhline(y=max_capacity, color='r', linestyle='--',
                  label='Capacidade Máxima')

        # Configurações do subplot
        ax.set_title(title)
        ax.set_xlabel('Número do Bin')
        ax.set_ylabel('Ocupação')
        ax.set_xticks(bin_positions)
        ax.set_xticklabels([f'{i+1}' for i in range(num_bins)])
        ax.set_ylim(0, max_capacity * 1.1)

        # Adicionar texto com o número total de bins
        ax.text(0.5, -0.1, f'Total de Bins: {num_bins}',
               ha='center', va='center', transform=ax.transAxes,
               fontsize=12, fontweight='bold')

    # Plotar ambas as soluções
    plot_solution(original_solution, ax1, "Solução Original")
    plot_solution(improved_solution, ax2, "Solução Melhorada")

    # Configurações finais
    plt.suptitle(title, fontsize=16)
    plt.tight_layout()

    # Salvar o gráfico se o caminho for fornecido
    if save_path:
        plt.savefig(save_path, bbox_inches='tight', dpi=300)
        print(f"Comparação de soluções salva em: {save_path}")

    if VISUALIZATION_CONFIG.get('show_plots', True):
        plt.show()

    plt.close()


def ensure_visualization_directory():
    """
    Garante que o diretório para salvar as visualizações exista.
    """
    plots_directory = VISUALIZATION_CONFIG.get('plots_directory',
                                              '/workspaces/Bin-Paking-Problem/resultados')
    if not os.path.exists(plots_directory):
        os.makedirs(plots_directory)
    return plots_directory
