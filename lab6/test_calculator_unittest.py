import unittest
from calculator import Calculator


class TestCalculator(unittest.TestCase):
    """Тесты для класса Calculator с использованием unittest"""

    def setUp(self):
        """Настройка перед каждым тестом"""
        self.calc = Calculator()

    def tearDown(self):
        """Очистка после каждого теста"""
        pass

    # Тесты для метода add
    def test_add_positive_numbers(self):
        """Тест сложения положительных чисел"""
        self.assertEqual(self.calc.add(2, 3), 5)
        self.assertEqual(self.calc.add(10, 15), 25)

    def test_add_negative_numbers(self):
        """Тест сложения отрицательных чисел"""
        self.assertEqual(self.calc.add(-2, -3), -5)
        self.assertEqual(self.calc.add(-10, 5), -5)

    def test_add_zero(self):
        """Тест сложения с нулем"""
        self.assertEqual(self.calc.add(0, 5), 5)
        self.assertEqual(self.calc.add(5, 0), 5)
        self.assertEqual(self.calc.add(0, 0), 0)

    # Тесты для метода subtract
    def test_subtract_positive_numbers(self):
        """Тест вычитания положительных чисел"""
        self.assertEqual(self.calc.subtract(5, 3), 2)
        self.assertEqual(self.calc.subtract(10, 15), -5)

    def test_subtract_negative_numbers(self):
        """Тест вычитания отрицательных чисел"""
        self.assertEqual(self.calc.subtract(-2, -3), 1)
        self.assertEqual(self.calc.subtract(-10, 5), -15)

    # Тесты для метода multiply
    def test_multiply_positive_numbers(self):
        """Тест умножения положительных чисел"""
        self.assertEqual(self.calc.multiply(2, 3), 6)
        self.assertEqual(self.calc.multiply(10, 15), 150)

    def test_multiply_by_zero(self):
        """Тест умножения на ноль"""
        self.assertEqual(self.calc.multiply(0, 5), 0)
        self.assertEqual(self.calc.multiply(5, 0), 0)
        self.assertEqual(self.calc.multiply(0, 0), 0)

    # Тесты для метода divide
    def test_divide_positive_numbers(self):
        """Тест деления положительных чисел"""
        self.assertEqual(self.calc.divide(6, 3), 2)
        self.assertAlmostEqual(self.calc.divide(5, 2), 2.5)

    def test_divide_negative_numbers(self):
        """Тест деления отрицательных чисел"""
        self.assertEqual(self.calc.divide(-6, 3), -2)
        self.assertEqual(self.calc.divide(6, -3), -2)
        self.assertEqual(self.calc.divide(-6, -3), 2)

    def test_divide_by_zero_raises_exception(self):
        """Тест возникновения исключения при делении на ноль"""
        with self.assertRaises(ValueError) as context:
            self.calc.divide(5, 0)

        self.assertEqual(str(context.exception), "Деление на ноль невозможно")

    # Тесты для метода is_prime_number
    def test_is_prime_number_positive_cases(self):
        """Тест простых чисел (должны возвращать True)"""
        primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
        for prime in primes:
            with self.subTest(prime=prime):
                self.assertTrue(self.calc.is_prime_number(prime))

    def test_is_prime_number_negative_cases(self):
        """Тест непростых чисел (должны возвращать False)"""
        non_primes = [1, 4, 6, 8, 9, 10, 12, 14, 15, 16, 18, 20]
        for non_prime in non_primes:
            with self.subTest(non_prime=non_prime):
                self.assertFalse(self.calc.is_prime_number(non_prime))

    def test_is_prime_number_edge_cases(self):
        """Тест граничных случаев"""
        self.assertFalse(self.calc.is_prime_number(1))
        self.assertFalse(self.calc.is_prime_number(0))
        self.assertFalse(self.calc.is_prime_number(-5))

    # Тесты для метода power
    def test_power_positive_exponent(self):
        """Тест возведения в положительную степень"""
        self.assertEqual(self.calc.power(2, 3), 8)
        self.assertEqual(self.calc.power(5, 2), 25)

    def test_power_zero_exponent(self):
        """Тест возведения в нулевую степень"""
        self.assertEqual(self.calc.power(5, 0), 1)
        self.assertEqual(self.calc.power(0, 0), 1)

    def test_power_negative_exponent(self):
        """Тест возведения в отрицательную степень"""
        self.assertAlmostEqual(self.calc.power(2, -1), 0.5)
        self.assertAlmostEqual(self.calc.power(4, -2), 0.0625)


if __name__ == '__main__':
    unittest.main(verbosity=2)