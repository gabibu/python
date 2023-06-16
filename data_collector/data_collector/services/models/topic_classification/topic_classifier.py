from abc import  ABC, abstractmethod
from typing import List, Dict

class TopicClassifier(ABC):

    @abstractmethod
    def classify(self, texts: List[str], topic: List[str]) -> List[Dict]:
        pass

