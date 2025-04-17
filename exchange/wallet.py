import random

class Wallet:
    def __init__(self, currency_code, ratio, value=None):
        self.currency_code = currency_code
        self.ratio = ratio
        self.value = value if value is not None else random.uniform(1, 100)

    def __add__(self, other):
        if isinstance(other, Wallet):
            return (self.value * self.ratio + other.value * other.ratio) / self.ratio
        raise TypeError("Unsupported operand type(s) for +")

    def __repr__(self):
        return f"{self.currency_code}, Kurs do PLN: {self.ratio}, Saldo: {self.value:.2f}"
