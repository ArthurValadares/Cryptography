import random
from math import floor, sqrt

from attr import define
from rich.console import Console

from src.util.gcd import ExtendedEuclideanAlgorithm


@define
class RSA:
    """Classe RSA

    Essa classe implementa o algoritmo de criptografia RSA. Ele fornece métodos para gerar pares de chaves, criptografar e descriptografar mensagens.

    Atributos:
        __p (int): O primeiro número primo.
        __q (int): O segundo número primo.
        __e (int): a chave pública.
        __d (int): a chave privada.

    Propriedades:
        n (int): O produto das variáveis privadas __p e __q, representando o valor de n.
        phi (int): O valor de phi (função totiente de Euler) para os parâmetros fornecidos.
        public_key (int): a chave pública.
        private_key (int): a chave privada.

    Métodos:
        __is_prime(n: int) -> bool: Método estático para verificar se um número é primo.
        __random_prime_number(start: int, stop: int, step: int = 1) -> int: Método estático para gerar um número primo aleatório dentro de um determinado intervalo.
        with_random_prime_numbers(start: int, stop: int, step: int = 1) -> 'RSA': Método estático para criar um objeto RSA com números primos aleatórios.
        encrypt(plaintext: str) -> str: Criptografa uma determinada mensagem de texto simples.
        decrypt(ciphertext: str) -> str: Descriptografa uma determinada mensagem de texto cifrado.
        encrypt_with(n: int, public_key: int, plaintext: str) -> str: Método estático para criptografar uma mensagem usando um determinado n e chave pública.
        decrypt_with(n: int, public_key: int, ciphertext: str) -> str: Método estático para descriptografar uma mensagem usando um determinado n e chave pública.
    """
    __p: int
    __q: int
    __e: int
    __d: int

    @property
    def n(self) -> int:
        """
        Método para calcular o produto dos atributos privados p e q.

        :return: Valor inteiro que representa o produto de p e q.
        """
        return self.__p * self.__q

    @property
    def phi(self) -> int:
        """
        Retorne o valor de phi (função totiente de Euler) para os parâmetros fornecidos.

        :return: O valor de phi (função totiente de Euler).
        :rtype: int
        """
        return (self.__p - 1) * (self.__q - 1)

    @property
    def public_key(self) -> int:
        """
        Retorna a chave pública.

        :return: a chave pública.
        :rtype: int
        """
        return self.__e

    @property
    def private_key(self) -> int:
        """
        :return: a chave privada do objeto.

        :rtype: int
        """
        return self.__d

    @staticmethod
    def __is_prime(n: int) -> bool:
        """
        Verifique se um número é primo.

        :param n: O número a ser verificado.
        :return: True se o número for primo, False caso contrário.
        """
        if n <= 1:
            return False
        for i in range(2, floor(sqrt(n)) + 1):
            if n % i == 0:
                return False
        return True

    @staticmethod
    def __random_prime_number(start: int, stop: int, step: int = 1) -> int:
        """
        Gera um número aleatório com base no intervalo informado e retorna-o caso ele seja primo
        :param start: início do intervalo
        :param stop:
        :param step:
        :return:
        """
        while True:
            n = random.randrange(start, stop, step)
            if RSA.__is_prime(n):
                return n

    @staticmethod
    def with_random_prime_numbers(start: int, stop: int, step: int = 1) -> 'RSA':
        """
        :param start: o número inicial para gerar números primos aleatórios.
        :param stop: o número de parada para gerar números primos aleatórios.
        :param step: o tamanho da passo para gerar números primos aleatórios. O padrão é 1.
        :return: Uma instância da classe 'RSA' com números primos gerados aleatoriamente.

        Este método gera dois números primos aleatórios dentro do intervalo especificado (início e parada),
        com o tamanho de passo fornecido (se fornecido). Ele verifica se os números gerados são iguais e, em caso afirmativo,
        gera um novo número até que sejam diferentes.

        Em seguida, ele calcula o valor de phi (a função totiente de Euler) com base nos números primos gerados.
        Em seguida, ele solicita que o usuário escolha um valor para a chave pública 'e', que deve ser coprimo com phi.

        O método usa o Algoritmo Euclidiano Estendido para verificar se o valor 'e' escolhido é coprimo com phi.
        Se não for coprimo, o usuário será solicitado a escolher um novo valor até que um valor coprimo seja selecionado.

        Finalmente, ele calcula a chave privada 'd' usando o inverso modular de 'e' em relação a phi.

        O método retorna uma instância da classe 'RSA' inicializada com os números primos gerados e as chaves.

        Exemplo de uso:
        rsa_instance = RSA.with_random_prime_numbers(2, 1000, 2)
        """
        console = Console()

        p = RSA.__random_prime_number(start, stop, step)
        console.print(f"O primeiro número aleatório gerado foi: {p}")

        q = RSA.__random_prime_number(start, stop, step)
        console.print(f"O segundo número aleatório gerado foi: {q}")
        while p == q:
            q = RSA.__random_prime_number(start, stop, step)

        phi = (p - 1) * (q - 1)
        console.print(f"O valor de phi é: {phi}")

        while True:
            e = int(console.input(f"Escolha a sua chave pública 'e' (deve ser coprimo com φ(n) = {phi}): "))
            gcd_e_phi = ExtendedEuclideanAlgorithm.execute(e, phi)
            if gcd_e_phi.are_coprime():
                break
            console.print(f"Valor de 'e' inválido. {e} não é coprimo com φ(n) = {phi}. Tente novamente.")

        d = gcd_e_phi.modular_inverse(e, phi)

        return RSA(p, q, e, d)

    def encrypt(self, plaintext: str) -> str:
        """
        Criptografa o texto simples fornecido usando criptografia RSA.

        :param: texto simples: o texto simples a ser criptografado.
        :return: O texto cifrado criptografado.
        """
        return ''.join(chr(pow(ord(letter), self.__e) % self.n) for letter in plaintext)

    def decrypt(self, ciphertext: str) -> str:
        """
        Descriptografa um determinado texto cifrado usando a chave privada.

        :param ciphertext: o texto criptografado a ser descriptografado.
        :return: O texto simples descriptografado.
        """
        return ''.join(chr(pow(ord(letter), self.__d) % self.n) for letter in ciphertext)

    @staticmethod
    def encrypt_with(n: int, public_key: int, plaintext: str) -> str:
        """
        Criptografa o texto simples fornecido usando o public_key e o módulo fornecidos.

        :param n: O valor do módulo usado na criptografia.
        :param public_key: a chave pública usada na criptografia.
        :param plaintext: o texto simples a ser criptografado.
        :return: O texto cifrado criptografado como uma cadeia de caracteres.
        """
        return ''.join(chr(pow(ord(letter), public_key) % n) for letter in plaintext)

    @staticmethod
    def decrypt_with(n: int, public_key: int, ciphertext: str) -> str:
        """
        :param n: O módulo usado no processo de descriptografia.
        :param public_key: a chave pública usada no processo de descriptografia.
        :param ciphertext: o texto criptografado a ser descriptografado.
        :return: o texto descriptografado.

        """
        return ''.join(chr(pow(ord(letter), public_key) % n) for letter in ciphertext)
