from typing import List, Optional

from data_collector.services.models.topic_classification.topic_classifier import TopicClassifier
from data_collector.scarping.entities.page_data import PageData
from data_collector.entities.url_topic import UrlTopic


class WebPageTopicClassifier:

    DEFAULT_TOPICS = ["weather", "news", "technology", "sports", "entertainment", "travel", "cooking", "politics",
                      "shopping", "productivity"]

    def __init__(self, base_model: TopicClassifier, topics: Optional[List[str]] = None):
        self._base_model = base_model
        self._topics = topics if topics is not None else WebPageTopicClassifier.DEFAULT_TOPICS

    def _build_text(self, page_data: PageData) -> str:

        texts = []

        if page_data.page_title is not None:
            texts.append(page_data.page_title)

        if page_data.page_links is not None:
            texts.extend([link.text for link in page_data.page_links])

        return ' '.join(texts)

    def predict(self, pages: List[PageData]) -> List[UrlTopic]:

        urls_topic = []
        texts_and_pages = [(self._build_text(page), page) for page in pages]

        texts = [text for (text, _) in texts_and_pages]
        classification_results = self._base_model.classify(texts, self._topics)

        text_to_prediction = {classification_result['sequence']: classification_result
                              for classification_result in classification_results}

        for (text, page_data) in texts_and_pages:
            predicted_topic = text_to_prediction[text]['labels'][0]

            urls_topic.append(UrlTopic(url=page_data.page_url, topic=predicted_topic))

        return urls_topic
