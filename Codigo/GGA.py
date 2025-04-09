import random
from copy import deepcopy
from Container import Container
from Tabu_Search import Tabu_Search
#import optuna
import numpy as np
import bisect
from collections import Counter


class GGA:

    def __init__(self, elements):
        """
        Initializes the genetic algorithm parameters for the bin packing problem.

        Args:
            elements (dict): A dictionary containing the following keys:
                - 'weights' (list): A list of item weights.
                - 'bin_capacity' (int): The capacity of each bin.
                - 'num_generations' (int): The number of generations to run the algorithm. Default is 100.
                - 'population_size' (int): The size of the population. Default is 20.
                - 'stagnation_limit' (int): The number of generations with no improvement before stopping. Default is 50.
                - 'tournament_size' (int): The number of individuals to participate in tournament selection. Default is 3.
                - 'mutation_rate' (float): The probability of mutation. Default is 0.1.
                - 'elite_rating' (float): The percentage of the population to be considered elite. Default is 0.1.
                - 'tabu_max_iterations' (int): Maximum number of iterations for Tabu Search. Default is 30.
                - 'tabu_tenure' (int): Number of iterations a move remains in the tabu list. Default is 5.
                - 'tabu_max_neighbors' (int): Maximum number of neighbors to consider in each iteration. Default is 20.
        """
        self.elements = elements.get('weights', [])
        self.container_capacity = elements.get('bin_capacity', 0)
        self.num_generations = elements.get('num_generations', 142)
        self.population_size = elements.get('population_size', 23)
        self.stagnation_limit = elements.get('stagnation_limit', 50)
        self.tournament_size = elements.get('tournament_size', 3)
        self.mutation_rate = elements.get('mutation_rate', 0.15)
        self.elite_rating = elements.get('elite_rating', 0.37)

        # Parâmetros da Tabu Search
        self.tabu_max_iterations = elements.get('tabu_max_iterations', 32)
        self.tabu_tenure = elements.get('tabu_tenure', 2)
        self.tabu_max_neighbors = elements.get('tabu_max_neighbors', 38)

    def generate_initial_solution(self, elements=None):
        if elements is None:
            elements = self.elements
        # Ordenar em ordem decrescente
        elements = [e for e in elements if e is not None]
        sorted_elements = sorted(elements, reverse=True)
        # Listas para armazenar os contêineres e seus espaços restantes
        containers = []
        remaining_spaces = []
        for element in sorted_elements:
            # Encontrar o índice do primeiro contêiner que pode acomodar o elemento
            index = bisect.bisect_left(remaining_spaces, element)
            if index < len(remaining_spaces):
                # Contêiner encontrado
                container = containers[index]
                container.add_element(element)
                # Atualizar o espaço restante
                rem_space = container.remaining_space()
                # Remover o contêiner e seu espaço das listas
                del remaining_spaces[index]
                del containers[index]
                # Inserir novamente na posição correta para manter a lista ordenada
                insert_index = bisect.bisect_left(remaining_spaces, rem_space)
                remaining_spaces.insert(insert_index, rem_space)
                containers.insert(insert_index, container)
            else:
                # Nenhum contêiner adequado encontrado, criar um novo
                new_container = Container(self.container_capacity)
                new_container.add_element(element)
                rem_space = new_container.remaining_space()
                # Inserir o novo contêiner na posição correta
                insert_index = bisect.bisect_left(remaining_spaces, rem_space)
                remaining_spaces.insert(insert_index, rem_space)
                containers.insert(insert_index, new_container)
        return containers

    def fitness(self, solution):
        """
            penalizar soluções onde os contêineres não estão bem preenchidos. 
            Ajustando a função de fitness para considerar o espaço desperdiçado 
            em cada contêiner
        """
        total_waste = sum(container.remaining_space()
                          for container in solution)
        return len(solution) + (total_waste / self.container_capacity)


# -------------------------------- Metodos de Seleção -------------------------------- #

    # Seleção por torneio


    def tournament_selection(self, population, fitnesses, tournament_size=3):
        selected = random.sample(
            list(zip(population, fitnesses)), tournament_size)
        selected.sort(key=lambda x: x[1])  # Ordenar em ordem crescente
        return selected[0][0]

    def stoic_tournament_selection(self, population, fitnesses, tournament_size=3):
        selected = random.sample(
            list(zip(population, fitnesses)), tournament_size)
        # Selecionar o mínimo
        best_individual = min(selected, key=lambda x: x[1])
        if random.random() < 0.75:
            return best_individual[0]
        else:
            return random.choice(selected)[0]

    def roulette_wheel_selection(self, population, fitnesses):
        # Converter fitnesses para um array NumPy
        fitnesses = np.array(fitnesses)

        # Inverter os fitnesses para que menores valores tenham maiores probabilidades
        max_fitness = fitnesses.max()
        adjusted_fitnesses = max_fitness - fitnesses + 1  # +1 para evitar zeros

        # Calcular as probabilidades normalizadas
        total_fitness = adjusted_fitnesses.sum()
        probabilities = adjusted_fitnesses / total_fitness

        # Calcular as probabilidades cumulativas
        cumulative_probabilities = np.cumsum(probabilities)

        # Gerar um número aleatório e encontrar o indivíduo correspondente
        r = np.random.rand()
        index = np.searchsorted(cumulative_probabilities, r)
        return population[index]


# -------------------------------- Metodos de Cruzamento -------------------------------- #

    # Função de cruzamento divisão unica


    def single_point_crossover(self, parent1, parent2):
        """
        Perform crossover operation between two parent solutions to generate two offspring.

        This method takes two parent solutions, extracts their elements, and combines them
        to create two new offspring solutions. The elements from the parents are split at
        the midpoint and recombined to form the offspring.

        Args:
            parent1 (list): The first parent solution, where each element is a container with elements.
            parent2 (list): The second parent solution, where each element is a container with elements.

        Returns:
            tuple: A tuple containing two offspring solutions, each represented as a list of containers.
        """
        # Coleta todos os elementos dos dois pais
        elements1 = [
            element for container in parent1 for element in container.elements]
        elements2 = [
            element for container in parent2 for element in container.elements]

        # Divide os elementos em dois grupos para criar dois filhos
        midpoint = len(elements1) // 2
        child1_elements = elements1[:midpoint] + elements2[midpoint:]
        child2_elements = elements2[:midpoint] + elements1[midpoint:]

        # Gera dois filhos redistribuindo os elementos entre os contêineres
        child1 = self.pack_elements(child1_elements)
        child2 = self.pack_elements(child2_elements)

        return child1, child2

    # Função de cruzamento divisão Multi-Pontos
    def multi_point_crossover(self, parent1, parent2):
        elements1 = [
            element for container in parent1 for element in container.elements]
        elements2 = [
            element for container in parent2 for element in container.elements]

        # Verificar se ambos os pais têm os mesmos elementos (e contagens)
        if sorted(elements1) != sorted(elements2):
            raise ValueError("Os pais devem conter os mesmos elementos.")

        length = len(elements1)
        if length < 2:
            return parent1, parent2

        # Escolher dois pontos de cruzamento
        point1, point2 = sorted(random.sample(range(length), 2))

        # Iniciar filhos com None
        child1_elements = [None] * length
        child2_elements = [None] * length

        # Copiar segmento intermediário dos pais para os filhos
        child1_elements[point1:point2] = elements1[point1:point2]
        child2_elements[point1:point2] = elements2[point1:point2]

        # Utilizar Counters para rastrear a contagem de elementos
        child1_counter = Counter(child1_elements[point1:point2])
        child2_counter = Counter(child2_elements[point1:point2])

        total_counter = Counter(elements1)  # Contagem total de elementos

        # Função para preencher o filho considerando a contagem de elementos
        def fill_child(child, other_parent, child_counter):
            length = len(child)
            current_pos = point2 % length
            for element in other_parent:
                total_count = total_counter[element]
                current_count = child_counter.get(element, 0)
                if current_count < total_count:
                    # Encontrar a próxima posição vazia
                    while child[current_pos] is not None:
                        current_pos = (current_pos + 1) % length
                    child[current_pos] = element
                    child_counter[element] = current_count + 1
                    current_pos = (current_pos + 1) % length

        # Preencher os filhos utilizando a função corrigida
        fill_child(child1_elements, elements2, child1_counter)
        fill_child(child2_elements, elements1, child2_counter)

        # Verificar se não há None nas listas dos filhos
        assert None not in child1_elements, "child1_elements contém None após o preenchimento."
        assert None not in child2_elements, "child2_elements contém None após o preenchimento."

        # Gerar filhos redistribuindo os elementos entre os contêineres
        child1 = self.pack_elements(child1_elements)
        child2 = self.pack_elements(child2_elements)

        return child1, child2

    def pmx_crossover(self, parent1, parent2):
        """
        Implementa o cruzamento PMX (Partially Matched Crossover) adaptado para o GGA.
        Realiza o cruzamento entre dois pais e garante que os itens não sejam duplicados nos filhos.
        """

        # Coleta todos os itens dos dois pais
        elements1 = [
            element for container in parent1 for element in container.elements]
        elements2 = [
            element for container in parent2 for element in container.elements]

        # Verifica se ambos os pais têm o mesmo número de elementos
        if len(elements1) != len(elements2):
            raise ValueError(
                "Os pais devem conter o mesmo número de elementos.")

        # Escolhe dois pontos de cruzamento
        point1, point2 = sorted(random.sample(range(len(elements1)), 2))

        # Inicializa os filhos como cópias dos pais
        child1_elements = elements1[:]
        child2_elements = elements2[:]

        # Troca os segmentos entre os dois pais
        child1_elements[point1:point2], child2_elements[point1:
                                                        point2] = elements2[point1:point2], elements1[point1:point2]

        # Mapeamento das trocas entre as subsequências para ambos os filhos
        mapping_1_to_2 = {elements1[i]: elements2[i]
                          for i in range(point1, point2)}
        mapping_2_to_1 = {elements2[i]: elements1[i]
                          for i in range(point1, point2)}

        # Corrige as colisões em ambos os filhos com os mapeamentos
        self._pmx_fix_collisions(
            child1_elements, mapping_1_to_2, point1, point2)
        self._pmx_fix_collisions(
            child2_elements, mapping_2_to_1, point1, point2)

        # Reorganiza os itens para criar os filhos a partir dos elementos ajustados
        child1 = self.pack_elements(child1_elements)
        child2 = self.pack_elements(child2_elements)

        return child1, child2

    def uniform_crossover(self, parent1, parent2):
        return None

    def arithmetic_Crossover(self, parent1, parent2):
        return None

    def order_Crossover(self, parent1, parent2):
        return None

    def cicly_Crossover(self, parent1, parent2):
        return None
# -------------------------------- Metodo de Mutações -------------------------------- #

    # Função de mutação
    def mutate(self, solution, mutation_rate):
        if random.random() < mutation_rate:
            solution = self._bitflip_Mutation(solution)
            solution = self._remove_empty_containers(solution)
        return solution

    # Funções para as Mutações

    def _swap_Mutation(self, solution):
        """
        Realiza a mutação de troca entre dois elementos de contêineres diferentes.
        """
        # Evitar modificar a solução original
        mutated_solution = solution.copy()

        # Filtra os índices dos contêineres que possuem pelo menos um elemento
        eligible_indices = [i for i, c in enumerate(
            mutated_solution) if c.elements]
        if len(eligible_indices) < 2:
            return mutated_solution

        # Seleciona aleatoriamente dois índices de contêineres distintos
        idx1, idx2 = random.sample(eligible_indices, 2)
        container1 = mutated_solution[idx1]
        container2 = mutated_solution[idx2]

        # Seleciona um elemento aleatório de cada contêiner
        element1 = random.choice(container1.elements)
        element2 = random.choice(container2.elements)

        # Verifica se a troca é viável para ambos os contêineres
        if (container1.remaining_space() + element1 - element2 >= 0 and
                container2.remaining_space() + element2 - element1 >= 0):

            # Fazer cópias dos contêineres para evitar modificar os originais
            container1 = container1.copy()
            container2 = container2.copy()
            mutated_solution[idx1] = container1
            mutated_solution[idx2] = container2

            # Realiza a troca de elementos entre os contêineres
            container1.remove_element(element1)
            container2.remove_element(element2)
            container1.add_element(element2)
            container2.add_element(element1)

        return mutated_solution

    def _inversion_Mutation(self, solution):
        """
        Realiza a mutação de inversão em uma solução.
        """
        # Evitar modificar a solução original
        mutated_solution = solution.copy()

        # Filtra índices de contêineres que possuem pelo menos dois itens
        eligible_indices = [i for i, c in enumerate(
            mutated_solution) if len(c.elements) >= 2]
        if not eligible_indices:
            return mutated_solution

        # Seleciona aleatoriamente um índice de contêiner elegível
        idx = random.choice(eligible_indices)
        container = mutated_solution[idx]

        # Fazer uma cópia do contêiner para evitar modificar o original
        container = container.copy()
        mutated_solution[idx] = container

        # Seleciona dois índices para definir a subsequência a ser invertida
        idx1, idx2 = sorted(random.sample(range(len(container.elements)), 2))

        # Inverte a subsequência de itens entre idx1 e idx2
        container.elements[idx1:idx2] = reversed(container.elements[idx1:idx2])

        return mutated_solution

    def _insertion_Mutation(self, solution):
        """
        Realiza uma mutação de inserção na solução.
        """
        mutated_solution = solution.copy()

        if len(mutated_solution) < 2:
            return mutated_solution

        # Seleciona aleatoriamente dois índices de contêineres diferentes
        idx1, idx2 = random.sample(range(len(mutated_solution)), 2)
        container1 = mutated_solution[idx1]
        container2 = mutated_solution[idx2]

        if container1.elements:
            # Fazer cópias dos contêineres
            container1 = container1.copy()
            container2 = container2.copy()
            mutated_solution[idx1] = container1
            mutated_solution[idx2] = container2

            # Seleciona um item aleatório do container1
            element = random.choice(container1.elements)
            container1.remove_element(element)

            # Tenta inserir o item em container2
            if container2.remaining_space() >= element:
                container2.add_element(element)
            else:
                # Se container2 não tiver espaço, cria um novo contêiner
                new_container = Container(self.container_capacity)
                if new_container.remaining_space() >= element:
                    new_container.add_element(element)
                    mutated_solution.append(new_container)
                else:
                    # Se o item não couber, devolve o item ao container1
                    container1.add_element(element)

        return mutated_solution

    def _scramble_Mutation(self, solution):
        """
        Realiza uma mutação de embaralhamento em um contêiner.
        """
        mutated_solution = solution.copy()

        # Filtra índices de contêineres com pelo menos dois elementos
        eligible_indices = [i for i, c in enumerate(
            mutated_solution) if len(c.elements) > 1]
        if not eligible_indices:
            return mutated_solution

        # Seleciona um índice de contêiner aleatório
        idx = random.choice(eligible_indices)
        container = mutated_solution[idx]

        # Fazer uma cópia do contêiner
        container = container.copy()
        mutated_solution[idx] = container

        # Seleciona dois índices e embaralha os elementos nessa subsequência
        idx1, idx2 = sorted(random.sample(range(len(container.elements)), 2))
        subsequence = container.elements[idx1:idx2]
        random.shuffle(subsequence)
        container.elements[idx1:idx2] = subsequence

        return mutated_solution

    def _gausian_Mutation(self, solution):
        """
        Realiza uma mutação baseada em distribuição gaussiana sem alterar os pesos dos itens.
        """
        mutated_solution = solution.copy()

        num_containers = len(mutated_solution)
        if num_containers < 2:
            return mutated_solution

        # Seleciona um índice de contêiner com base em uma distribuição gaussiana
        mean = num_containers / 2
        std_dev = num_containers / 4
        max_attempts = 10
        attempts = 0
        while attempts < max_attempts:
            index_from = int(np.random.normal(mean, std_dev))
            if 0 <= index_from < num_containers and mutated_solution[index_from].elements:
                break
            attempts += 1
        else:
            return mutated_solution

        # Fazer cópias dos contêineres
        container_from = mutated_solution[index_from].copy()
        mutated_solution[index_from] = container_from

        index_to = random.choice(
            [i for i in range(num_containers) if i != index_from])
        container_to = mutated_solution[index_to].copy()
        mutated_solution[index_to] = container_to

        # Seleciona um item aleatório do contêiner de origem
        item = random.choice(container_from.elements)

        # Verifica se o item cabe no contêiner de destino
        if container_to.remaining_space() >= item:
            container_from.remove_element(item)
            container_to.add_element(item)
        else:
            # Tenta criar um novo contêiner
            new_container = Container(self.container_capacity)
            if new_container.remaining_space() >= item:
                container_from.remove_element(item)
                new_container.add_element(item)
                mutated_solution.append(new_container)
            else:
                # Não foi possível mover o item
                mutated_solution[index_from] = solution[index_from]
                mutated_solution[index_to] = solution[index_to]

        # Remove contêineres vazios
        mutated_solution = self._remove_empty_containers(mutated_solution)

        return mutated_solution

    def _bitflip_Mutation(self, solution):
        """
        Realiza uma mutação de bit-flip na solução fornecida.

        Esta mutação seleciona aleatoriamente dois contêineres diferentes da solução.
        Se o primeiro contêiner selecionado tiver elementos, ele seleciona aleatoriamente
        um elemento deste contêiner e tenta movê-lo para o segundo contêiner selecionado.
        Se o segundo contêiner não tiver espaço suficiente, um novo contêiner é criado
        para acomodar o elemento. Se o elemento não puder ser movido, ele é devolvido ao
        contêiner original.

            solution (list): Uma lista de contêineres representando a solução atual.

            list: Uma nova solução com a mutação de bit-flip aplicada.
        """
        mutated_solution = solution.copy()

        if len(mutated_solution) < 2:
            return mutated_solution

        # Seleciona aleatoriamente dois índices de contêineres diferentes
        idx1, idx2 = random.sample(range(len(mutated_solution)), 2)
        container1 = mutated_solution[idx1]
        container2 = mutated_solution[idx2]

        if container1.elements:
            # Fazer cópias dos contêineres
            container1 = container1.copy()
            container2 = container2.copy()
            mutated_solution[idx1] = container1
            mutated_solution[idx2] = container2

            # Seleciona um item aleatório do container1
            element = random.choice(container1.elements)
            container1.remove_element(element)

            # Tenta inserir o item em container2
            if container2.remaining_space() >= element:
                container2.add_element(element)
            else:
                # Se container2 não tiver espaço, cria um novo contêiner
                new_container = Container(self.container_capacity)
                if new_container.remaining_space() >= element:
                    new_container.add_element(element)
                    mutated_solution.append(new_container)
                else:
                    # Se o item não couber, devolve o item ao container1
                    container1.add_element(element)

        return mutated_solution

# -------------------------------- Metodos Auxiliares -------------------------------- #

    def _remove_empty_containers(self, solution):
        return [container for container in solution if container.elements]

    # Função auxiliar para redistribuir os elementos em contêineres
    def pack_elements(self, elements):
        """
        Empacota os elementos fornecidos em contêineres usando um método de geração de solução inicial.

        Args:
            elements (list): Uma lista de elementos a serem empacotados em contêineres.

        Returns:
            list: Uma lista de contêineres com os elementos empacotados.
        """
        original_elements = self.elements
        self.elements = elements
        containers = self.generate_initial_solution()
        self.elements = original_elements
        return containers

    # Função principal que executa o algoritmo genético
    def run(self):
        """
        Executa o algoritmo genético para otimização.

        Inicializa a população e itera por um número definido de gerações,
        avaliando a aptidão (fitness) de cada indivíduo e criando novas populações
        até que a estagnação seja atingida ou o número máximo de gerações seja alcançado.

        Retorna a melhor solução encontrada.

        Returns:
            best_solution: O indivíduo com a melhor aptidão encontrado durante a execução do algoritmo.
        """
        self.initialize_population()
        best_fitness = float('inf')
        stagnation_counter = 0

        for generation in range(self.num_generations):
            fitnesses = [self.fitness(individual)
                         for individual in self.population]
            current_best_fitness = min(fitnesses)

            if current_best_fitness < best_fitness:
                best_fitness = current_best_fitness
                stagnation_counter = 0
            else:
                stagnation_counter += 1

            if stagnation_counter >= self.stagnation_limit:
                print(
                    f"Estagnação atingida na geração {generation}. Finalizando o algoritmo..."
                )
                break

            self.population = self.create_new_population(fitnesses)

        best_solution = min(self.population, key=self.fitness)
        print(f"Melhor fitness obtido: {best_fitness}")
        return best_solution

    def initialize_population(self):
        """
        Inicializa a população para o algoritmo genético.

        Este método gera uma população inicial de soluções chamando
        o método `generate_initial_solution` para cada indivíduo na
        população. O tamanho da população é determinado pelo atributo
        `population_size`.

        Retorna:
            None
        """
        self.population = [self.generate_initial_solution()
                           for _ in range(self.population_size)]

    def create_new_population(self, fitnesses):
        """
        Gera uma nova população para o algoritmo genético.

        Este método aplica elitismo para reter os indivíduos de melhor desempenho,
        melhora-os usando a Busca Tabu e preenche o restante da população
        usando operações de cruzamento e mutação.

        Args:
            fitnesses (list): Uma lista de valores de fitness correspondentes à população atual.

        Returns:
            list: Uma nova população de indivíduos.
        """
        # aplicação do elitismo
        elite_size = int(self.elite_rating * self.population_size)
        elite = sorted(self.population, key=self.fitness)[:elite_size]
        new_population = elite.copy()  # Garantir que a elite passe para a próxima geração

        TS = Tabu_Search(self, max_iterations=self.tabu_max_iterations,
                         tabu_tenure=self.tabu_tenure, max_neighbors=self.tabu_max_neighbors)
        improved_elite = []
        for individual in elite:
            improved_individual = TS.search(individual)
            improved_elite.append(improved_individual)
        new_population = improved_elite.copy()

        while len(new_population) < self.population_size:
            parent1 = self.stoic_tournament_selection(
                self.population, fitnesses)
            parent2 = self.stoic_tournament_selection(
                self.population, fitnesses)

            # multi_point_crossover
            child1, child2 = self.multi_point_crossover(parent1, parent2)
            child1 = self.mutate(child1, self.mutation_rate)
            child2 = self.mutate(child2, self.mutation_rate)

            new_population.append(child1)
            if len(new_population) < self.population_size:
                new_population.append(child2)

        return new_population

    def _pmx_fix_collisions(self, child_elements, mapping, point1, point2):
        """
        Corrige colisões causadas pelo cruzamento PMX, garantindo que cada item apareça apenas uma vez.

        Args:
            child_elements (list): Os elementos do filho gerado após a troca.
            mapping (dict): Mapeamento entre os itens trocados nos pais.
            point1 (int): Primeiro ponto de cruzamento.
            point2 (int): Segundo ponto de cruzamento.
        """
        swapped_elements = set(child_elements[point1:point2])

        # Percorre os elementos fora da faixa de cruzamento
        for i in list(range(0, point1)) + list(range(point2, len(child_elements))):
            # Se o elemento estiver em swapped_elements, ele precisa ser corrigido
            while child_elements[i] in swapped_elements:
                child_elements[i] = mapping[child_elements[i]]

# Função para otimização dos hiperparametross
# def call_optuna(self):


"""
def objective(trial):
    # Hiperparâmetros a serem otimizados
    hyperparameters = {
        'num_generations': trial.suggest_int('num_generations', 50, 200),
        'population_size': trial.suggest_int('population_size', 10, 100),
        'mutation_rate': trial.suggest_float('mutation_rate', 0.01, 0.5),
        'elite_rating': trial.suggest_float('elite_rating', 0.01, 0.5),
        'tabu_max_iterations': trial.suggest_int('tabu_max_iterations', 10, 100),
        'tabu_tenure': trial.suggest_int('tabu_tenure', 1, 20),
        'tabu_max_neighbors': trial.suggest_int('tabu_max_neighbors', 5, 50),
        'weights': [random.randint(1, 100) for _ in range(50)],
        'bin_capacity': 150
    }

    # Inicializar e executar o GGA
    gga = GGA(hyperparameters)

    best_solution = gga.run()
    best_fitness = gga.fitness(best_solution)

    # O Optuna minimiza por padrão, então fitness negativo pode ser necessário se maior for melhor
    return best_fitness


# Alterar para "maximize" se necessário
study = optuna.create_study(direction="minimize")
study.optimize(objective, n_trials=50)

# Exibir os melhores hiperparâmetros
print("Melhores hiperparâmetros encontrados:", study.best_params)
# return study.best_params
"""
