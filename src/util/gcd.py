from typing import List, Optional

from attr import define, field


@define
class ExtendedEuclideanAlgorithmStep:
    quotient: int
    remainder: int
    s: int
    t: int


@define
class ExtendedEuclideanAlgorithm:
    __steps: List[ExtendedEuclideanAlgorithmStep] = field(factory=list)

    @property
    def steps(self) -> List[ExtendedEuclideanAlgorithmStep]:
        return self.__steps

    @staticmethod
    def execute(a: int, b: int) -> 'ExtendedEuclideanAlgorithm':
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
        return self.steps[-1].remainder == 1

    def modular_inverse(self, a: int, b: int) -> int:
        last_step = self.steps[-1]
        if last_step.remainder != 1:
            raise ValueError(f"{a} and {b} are not coprime, so the modular inverse does not exist.")
        return last_step.s % b