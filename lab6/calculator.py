class Calculator:
    """Класс калькулятора с базовыми математическими операциями"""

    def add(self, a, b):
        """Сложение двух чисел"""
        return a + b

    def subtract(self, a, b):
        """Вычитание"""
        return a - b

    def multiply(self, a, b):
        """Умножение"""
        return a * b

    def divide(self, a, b):
        """Деление с проверкой деления на ноль"""
        if b == 0:
            raise ValueError("Деление на ноль невозможно")
        return a / b

    def is_prime_number(self, n):
        """Проверка, является ли число простым"""
        if n <= 1:
            return False
        if n <= 3:
            return True
        if n % 2 == 0 or n % 3 == 0:
            return False

        i = 5
        while i * i <= n:
            if n % i == 0 or n % (i + 2) == 0:
                return False
            i += 6
        return True

    def power(self, base, exponent):
        """Возведение в степень"""
        return base ** exponent