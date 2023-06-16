import logging

from data_collector.scarping.scrapping_manager import ScrappingManager
from data_collector.services.datacollection_dal import DataCollectionDal
from data_collector.services.models.topic_classification.web_page_topic_classifier import WebPageTopicClassifier

class DataCollectionOrchestrator:


    def __init__(self, scrapping_manager: ScrappingManager, data_collection_dal: DataCollectionDal,
                 topic_classifier: WebPageTopicClassifier):
        self._scrapping_manager = scrapping_manager
        self._data_collection_dal = data_collection_dal
        self._topic_classifier = topic_classifier

    def collect_data(self, url: str, depth: str):

        pages = self._scrapping_manager.scrape(url, depth)

        if pages is None or len(pages) == 0:
            logging.info(f'No pages for {url} with depth {depth}')
            return

        self._data_collection_dal.inset_pages_data(pages)

        urls_topics = self._topic_classifier.predict(pages)

        self._data_collection_dal.insert_urls_topic(urls_topics)





