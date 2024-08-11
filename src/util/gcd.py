from typing import List, Optional

from attr import define, field


@define
class ExtendedEuclideanAlgorithmStep:
    """
    Representa uma etapa no algoritmo euclidiano estendido.

    Atributos:
        quociente (int): o quociente obtido na etapa.
        restante (int): O restante obtido na etapa.
        s (int): o valor de s obtido na etapa.
        t (int): o valor de t obtido na etapa.
    """
    quotient: int
    remainder: int
    s: int
    t: int


@define
class ExtendedEuclideanAlgorithm:
    """
    Classe que representa o algoritmo euclidiano estendido.

    O algoritmo euclidiano estendido é usado para encontrar o máximo divisor comum (gcd) de dois números,
    bem como os coeficientes s e t tais que a * s + b * t = gcd(a, b).

    Atributos:
        __steps (List[ExtendedEuclideanAlgorithmStep]): lista de etapas executadas durante o algoritmo.

    Métodos:
        execute(a: int, b: int) -> ExtendedEuclideanAlgorithm: método estático que executa o algoritmo euclidiano estendido.
        are_coprime() -> bool: Verifica se os dois números (a e b) dados ao algoritmo são coprimos.
        modular_inverse(a: int, b: int) -> int: Calcula o inverso modular de um módulo b.
    """
    __steps: List[ExtendedEuclideanAlgorithmStep] = field(factory=list)

    @property
    def steps(self) -> List[ExtendedEuclideanAlgorithmStep]:
        """
        Método: etapas

        Retorna a lista de etapas executadas no algoritmo euclidiano estendido.

        :return: uma lista de objetos ExtendedEuclideanAlgorithmStep que representam as etapas executadas no algoritmo euclidiano estendido.
        """
        return self.__steps

    @staticmethod
    def execute(a: int, b: int) -> 'ExtendedEuclideanAlgorithm':
        """
        :param a: Um inteiro que representa o valor de 'a' no algoritmo euclidiano estendido.
        :param b: Um número inteiro que representa o valor de 'b' no algoritmo euclidiano estendido.
        :return: Uma instância da classe 'ExtendedEuclideanAlgorithm'.

        Este método executa o algoritmo euclidiano estendido para encontrar o máximo divisor comum (MDC) de 'a' e 'b',
        bem como os coeficientes de Bézout 's' e 't' que satisfazem a equação 'ax + by = gcd(a, b)'.

        O algoritmo funciona da seguinte maneira:
        1. Inicialize uma lista vazia de 'etapas' para armazenar as etapas intermediárias do algoritmo.
        2. Defina 'old_r' e 'r' para os valores de 'a' e 'b', respectivamente.
        3. Defina 'old_s' e 's' como 1 e 0, respectivamente.
        4. Defina 'old_t' e 't' como 0 e 1, respectivamente.
        5. Insira um loop que continua até que o valor de 'r' se torne 0:
           6. Calcule o quociente de 'old_r' dividido por 'r' e armazene-o na variável 'quociente'.
           7. Crie uma instância da classe 'ExtendedEuclideanAlgorithmStep', com os valores de 'quociente', 'r', 's' e 't',
              e anexe-o à lista de 'etapas'.
           8. Atualize os valores de 'old_r' e 'r' da seguinte maneira:
              - 'old_r' torna-se 'r'.
              - 'r' torna-se a diferença entre 'old_r' e o produto de 'quociente' e 'r'.
           9. Atualize os valores de 'old_s' e 's' da seguinte maneira:
              - 'old_s' torna-se 's'.
              - 's' torna-se a diferença entre 'old_s' e o produto de 'quociente' e 's'.
           10. Atualize os valores de 'old_t' e 't' da seguinte maneira:
              - 'old_t' torna-se 't'.
              - 't' torna-se a diferença entre 'old_t' e o produto de 'quociente' e 't'.
        10. Crie uma instância final da classe 'ExtendedEuclideanAlgorithmStep', com os valores 'quociente'=0,
            'remainder'=old_r', 's'=old_s' e 't'=old_t', e anexe-o à lista 'steps'.
        11. Crie uma instância da classe 'ExtendedEuclideanAlgorithm', passando a lista 'etapas' e retorne-a como resultado.

        Observação: presume-se que a classe 'ExtendedEuclideanAlgorithmStep' seja definida em outro lugar e represente uma única etapa no
        algoritmo euclidiano estendido, com atributos para 'quociente', 'resto', 's' e 't'.

        Exemplo de uso:
            resultado = ExtendedEuclideanAlgorithm.execute(24, 18)
        """
        steps: List[ExtendedEuclideanAlgorithmStep] = []

        old_r, r = a, b
        old_s, s = 1, 0
        old_t, t = 0, 1

        while r != 0:
            quotient = old_r // r
            steps.append(ExtendedEuclideanAlgorithmStep(
                quotient=quotient,
                remainder=r,
                s=s,
                t=t
            ))
            old_r, r = r, old_r - quotient * r
            old_s, s = s, old_s - quotient * s
            old_t, t = t, old_t - quotient * t

        steps.append(ExtendedEuclideanAlgorithmStep(
            quotient=0,
            remainder=old_r,
            s=old_s,
            t=old_t
        ))

        return ExtendedEuclideanAlgorithm(steps)

    def are_coprime(self) -> bool:
        """
        Verifica se o restante da última etapa na lista de etapas fornecida é 1, indicando que os números são primos.

        :return: True se os números forem coprimos, False caso contrário.
        :rtype: bool
        """
        return self.steps[-1].remainder == 1

    def modular_inverse(self, a: int, b: int) -> int:
        """
        Calcula o inverso modular de 'a' módulo 'b'.

        :param a: O número cujo inverso modular deve ser calculado.
        :param b: O módulo.
        :return: O inverso modular de 'a' módulo 'b'.
        :raises ValueError: Se 'a' e 'b' não são coprimos, então o inverso modular não existe.
        """
        last_step = self.steps[-1]
        if last_step.remainder != 1:
            raise ValueError(f"{a} and {b} are not coprime, so the modular inverse does not exist.")
        return last_step.s % b