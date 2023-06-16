
from typing import List, Dict
from transformers import pipeline
from data_collector.services.models.topic_classification.topic_classifier import TopicClassifier


class ZeroShotTopicClassifier(TopicClassifier):

    def __init__(self, model: str = 'valhalla/distilbart-mnli-12-1'):

        self._classifier = pipeline('zero-shot-classification', model=model)

    def classify(self, texts: List[str], topic: List[str]) -> List[Dict]:
        return self._classifier(texts, topic)



