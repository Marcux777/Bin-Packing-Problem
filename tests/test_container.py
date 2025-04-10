import sys
import os
import unittest

# Adicionar diretório raiz ao path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Codigo.models.container import Container

class TestContainer(unittest.TestCase):
    """
    Testes unitários para a classe Container
    """

    def setUp(self):
        """
        Configuração inicial para cada teste
        """
        self.capacity = 100
        self.container = Container(self.capacity)

    def test_init(self):
        """
        Testa a inicialização correta do Container
        """
        self.assertEqual(self.container.capacity, self.capacity)
        self.assertEqual(self.container.used, 0)
        self.assertEqual(self.container.elements, [])

    def test_add_element(self):
        """
        Testa a adição de elementos ao Container
        """
        self.container.add_element(30)
        self.assertEqual(self.container.used, 30)
        self.assertEqual(self.container.elements, [30])

        self.container.add_element(20)
        self.assertEqual(self.container.used, 50)
        self.assertEqual(self.container.elements, [30, 20])

    def test_add_element_error(self):
        """
        Testa a exceção ao tentar adicionar elemento que excede capacidade
        """
        self.container.add_element(70)
        with self.assertRaises(Exception):
            self.container.add_element(40)

    def test_remove_element(self):
        """
        Testa a remoção de elementos do Container
        """
        self.container.add_element(30)
        self.container.add_element(20)

        self.container.remove_element(30)
        self.assertEqual(self.container.used, 20)
        self.assertEqual(self.container.elements, [20])

    def test_is_full(self):
        """
        Testa a verificação se o Container está cheio
        """
        self.assertFalse(self.container.is_full())

        self.container.add_element(100)
        self.assertTrue(self.container.is_full())

    def test_remaining_space(self):
        """
        Testa o cálculo de espaço restante no Container
        """
        self.assertEqual(self.container.remaining_space(), 100)

        self.container.add_element(30)
        self.assertEqual(self.container.remaining_space(), 70)

    def test_copy(self):
        """
        Testa o método de cópia do Container
        """
        self.container.add_element(30)
        self.container.add_element(20)

        new_container = self.container.copy()
        self.assertEqual(new_container.capacity, self.container.capacity)
        self.assertEqual(new_container.used, self.container.used)
        self.assertEqual(new_container.elements, self.container.elements)

        # Verificar se é uma cópia independente
        self.container.add_element(10)
        self.assertNotEqual(new_container.used, self.container.used)

if __name__ == '__main__':
    unittest.main()
