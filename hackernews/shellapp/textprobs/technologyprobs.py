
from abc import ABC, abstractmethod
from typing import Dict, Set
import pandas as pd

class TechnologiesProbs(ABC):

    @abstractmethod
    def technologies(self) -> Set[str]:
        pass

    @abstractmethod
    def get_technology_prob(self, technology: str) -> float:
        pass



class StaticTechnologiesProbs(TechnologiesProbs):

    def __init__(self, probs: Dict[str, float]):

        super().__init__()

        if probs is None:
            raise Exception("probs cant be None")

        self._probs = probs

    def technologies(self) -> Set[str]:
        return set(self._probs.keys())

    def get_technology_prob(self, technology: str) -> float:

        if technology in self._probs:
            return self._probs[technology]

        raise Exception("technology {} is not supported")


class TechnologiesProbsFactory:

    @staticmethod
    def build(probs_file_path: str) -> TechnologiesProbs:
        if probs_file_path is None:
            raise Exception("probs_file_path cant be None")

        df = pd.read_parquet(probs_file_path)

        probs = dict(zip(df.technology, df.monthly_prob))


        return StaticTechnologiesProbs(probs)