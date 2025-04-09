def display_solution(arquivo, solution, execution_time):
    """
    Exibe os resultados da solução de uma instância do problema.

    Args:
        arquivo (str): Nome do arquivo da instância
        solution (list): Lista de contêineres na solução
        execution_time (float): Tempo de execução em segundos
    """
    print(f"\nMelhor solução encontrada para {arquivo}:")
    print("=" * 100)
    for i, container in enumerate(solution, 1):
        print(f"Contêiner {i}: {container}")
    print("=" * 100)
    print("Quantidade de contêineres usados: ", len(solution))
    print("=" * 100)
    print("Tempo total de solução: {:.2f} segundos".format(execution_time))
    print("=" * 100)
