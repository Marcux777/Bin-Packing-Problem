from copy import deepcopy


class Container:
    def __init__(self, capacity):
        self.elements = []  # Lista de elementos (tamanhos) dentro do container
        self.capacity = capacity
        self.used = 0  # Espaço já utilizado no container

    def __deepcopy__(self, memo):
        new_container = Container(self.capacity)
        new_container.elements = deepcopy(self.elements, memo)
        # Copiar outros atributos, se houver
        return new_container

    def add_element(self, element):
        if self.used + element <= self.capacity:
            self.elements.append(element)
            self.used += element
        else:
            raise Exception("Capacidade excedida no container!")

    def remove_element(self, element):
        if element in self.elements:
            self.elements.remove(element)
            self.used -= element

    def is_full(self):
        return self.used >= self.capacity

    def remaining_space(self):
        return self.capacity - self.used

    def __repr__(self):
        return f"Container({self.elements}, usado: {self.used}/{self.capacity})"

    def copy(self):
        new_container = Container(self.capacity)
        new_container.elements = self.elements.copy()
        new_container.used = self.used
        return new_container
