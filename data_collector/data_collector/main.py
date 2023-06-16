import argparse
import logging

from data_collector.scarping.html_fetching.html_fetcher import HtmlFetcher
from data_collector.scarping.html_parsers.html_parser import HtmlParserFactory
from data_collector.services.datacollection_dal import DataCollectionDalSqlLite
from data_collector.scarping.scrapping_manager import ScrappingManager
from data_collector.data_collection_orchestrator import DataCollectionOrchestrator
from data_collector.services.models.topic_classification.web_page_topic_classifier import WebPageTopicClassifier
from data_collector.services.models.topic_classification.zero_shot_topic_classifier import ZeroShotTopicClassifier

if __name__ == '__main__':


    parser = argparse.ArgumentParser()
    parser.add_argument("--url", help="url tp scrape", type=str, required=True)
    parser.add_argument("--depth", help="scraping depth",
                        type=int, required=True)
    parser.add_argument("--fetch_concurrency", type=int, default=1, required=False)
    parser.add_argument("--parse_concurrency", type=int, default=1, required=False)
    parser.add_argument('--db_file', type=str, required=False, default='/data/scraping_db')

    args = parser.parse_args()

    logging.info(f'run scrapping with {args}')

    data_collection_dal = DataCollectionDalSqlLite(args.db_file)

    scrapping_manager = ScrappingManager(HtmlFetcher(), HtmlParserFactory(), args.fetch_concurrency,
                                         args.parse_concurrency)

    data_collection_orchestrator = DataCollectionOrchestrator(scrapping_manager, data_collection_dal,
                               WebPageTopicClassifier(ZeroShotTopicClassifier()) )

    data_collection_orchestrator.collect_data(args.url, args.depth)

    logging.info('scrapping completed')
