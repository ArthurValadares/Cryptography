import random
from math import floor, sqrt

from attr import define
from rich.console import Console

from src.util.gcd import ExtendedEuclideanAlgorithm


@define
class RSA:
    __p: int  # Primeiro primo
    __q: int  # Segundo primo
    __e: int  # Chave Pública
    __d: int  # Chave Privada

    @property
    def n(self) -> int:
        return self.__p * self.__q

    @property
    def phi(self) -> int:
        return (self.__p - 1) * (self.__q - 1)

    @property
    def public_key(self) -> int:
        return self.__e

    @property
    def private_key(self) -> int:
        return self.__d

    @staticmethod
    def __is_prime(n: int) -> bool:
        if n <= 1:
            return False
        for i in range(2, floor(sqrt(n)) + 1):
            if n % i == 0:
                return False
        return True

    @staticmethod
    def __random_prime_number(start: int, stop: int, step: int = 1) -> int:
        while True:
            n = random.randrange(start, stop, step)
            if RSA.__is_prime(n):
                return n

    @staticmethod
    def with_random_prime_numbers(start: int, stop: int, step: int = 1) -> 'RSA':
        console = Console()

        p = RSA.__random_prime_number(start, stop, step)
        q = RSA.__random_prime_number(start, stop, step)
        while p == q:
            q = RSA.__random_prime_number(start, stop, step)

        phi = (p - 1) * (q - 1)

        while True:
            e = int(console.input(f"Escolha a sua chave pública 'e' (deve ser coprimo com φ(n) = {phi}): "))
            gcd_e_phi = ExtendedEuclideanAlgorithm.execute(e, phi)
            if gcd_e_phi.are_coprime():
                break
            console.print(f"Valor de 'e' inválido. {e} não é coprimo com φ(n) = {phi}. Tente novamente.")

        d = gcd_e_phi.modular_inverse(e, phi)

        return RSA(p, q, e, d)

    def encrypt(self, plaintext: str) -> str:
        return ''.join(chr(pow(ord(letter), self.__e) % self.n) for letter in plaintext)

    def decrypt(self, ciphertext: str) -> str:
        return ''.join(chr(pow(ord(letter), self.__d) % self.n) for letter in ciphertext)

    @staticmethod
    def encrypt_with(n: int, public_key: int, plaintext: str) -> str:
        return ''.join(chr(pow(ord(letter), public_key) % n) for letter in plaintext)

    @staticmethod
    def decrypt_with(n: int, public_key: int, ciphertext: str) -> str:
        return ''.join(chr(pow(ord(letter), public_key) % n) for letter in ciphertext)
