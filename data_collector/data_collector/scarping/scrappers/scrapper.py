import logging

from data_collector.scarping.html_fetching.html_fetcher import HtmlFetcher
from data_collector.scarping.html_parsers.html_parser import HtmlParserFactory
from data_collector.scarping.entities.scraping_data import ScrappingData


class Scrapper:

    def __init__(self, html_fetcher: HtmlFetcher, html_parser_factory: HtmlParserFactory):
        self._html_fetcher = html_fetcher
        self._html_parser_factory = html_parser_factory

    def run(self, url: str) -> ScrappingData:

        try:

            html = self._html_fetcher.scrap(url)
            html_parser = self._html_parser_factory.create_html_parser(html)
            page_title = html_parser.get_title()
            page_links = html_parser.get_urls()
            return ScrappingData(page_url=url, page_title=page_title, page_links=page_links)

        except Exception as e:
            logging.exception(url)
            raise e
