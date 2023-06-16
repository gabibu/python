import logging
from typing import List, Generator
from concurrent.futures._base import TimeoutError

from data_collector.scarping.entities.scraping_request import ScrappingRequest, PageHtml
from data_collector.scarping.entities.page_data import PageData
from data_collector.scarping.html_parsers.html_parser import HtmlParserFactory
from concurrent.futures import as_completed, ThreadPoolExecutor, Future
from data_collector.scarping.html_fetching.html_fetcher import HtmlFetcher


class ScrappingManager:

    def __init__(self, html_fetcher: HtmlFetcher, html_parser_factory: HtmlParserFactory,
                 fetch_concurrency: int, parsing_concurrency: int):

        self._html_parser_factory = html_parser_factory
        self._html_fetcher = html_fetcher
        self._parsing_pool = ThreadPoolExecutor(max_workers=parsing_concurrency)
        self._fetch_pool = ThreadPoolExecutor(max_workers=fetch_concurrency)

    def _run_fetcher(self, request: ScrappingRequest) -> PageHtml:

        try:

            html = self._html_fetcher.get_html(request.page_url)

            page_html = PageHtml(page_url=request.page_url,
                                 source_url=request.source_url,
                                 depth_from_initial=request.depth_from_initial,
                                 html=html)

            return page_html
        except:
            logging.exception(request)

            return PageHtml(page_url=request.page_url,
                            source_url=request.source_url,
                            depth_from_initial=request.depth_from_initial,
                            html=None)

    def _run_parser(self, page_html: PageHtml) -> PageData:

        html_parser = self._html_parser_factory.create_html_parser(page_html.html)

        page_links = html_parser.get_urls()
        title = html_parser.get_title()

        return PageData(page_url=page_html.page_url,
                        source_url=page_html.source_url, depth=page_html.depth_from_initial,
                        page_title=title, page_links=page_links)

    def _collect_futures_results(self, futures: List[Future], timeout: int = 10) -> Generator:

        if len(futures) == 0:
            return

        try:
            for future in as_completed(futures, timeout=timeout):
                yield future

        except TimeoutError:
            return

    def scrape(self, url: str, depth: int) -> List[PageData]:

        logging.info(f'scrape {url} with depth {depth}')

        source_url_request = ScrappingRequest(page_url=url, source_url=None, depth_from_initial=0)
        fetch_future_source_url = self._fetch_pool.submit(self._run_fetcher, source_url_request)

        fetch_futures = [fetch_future_source_url]
        parse_futures = []
        pages_data = []

        while len(fetch_futures) > 0 or len(parse_futures) > 0:

            if len(fetch_futures) > 0:

                completed_fetched = []
                for future in self._collect_futures_results(fetch_futures):
                    completed_fetched.append(future)
                    page_html = future.result()

                    parser_future = self._parsing_pool.submit(self._run_parser, page_html)
                    parse_futures.append(parser_future)

                fetch_futures = [future for future in fetch_futures if future not in completed_fetched]

                logging.info(f'fetch_futures {len(fetch_futures)}')

                completed_parsing = []
                for future in self._collect_futures_results(parse_futures):
                    completed_parsing.append(future)
                    page_data: PageData = future.result()
                    pages_data.append(page_data)

                    if page_data.depth < depth and page_data.page_links is not None and len(page_data.page_links) > 0:
                        new_fetch_futures = [
                            self._fetch_pool.submit(self._run_fetcher, ScrappingRequest(page_url=page_link.url,
                                                                                        source_url=None,
                                                                                        depth_from_initial=page_data.depth + 1))
                            for page_link in page_data.page_links]

                        fetch_futures.extend(new_fetch_futures)

                parse_futures = [future for future in parse_futures if future not in completed_parsing]
                logging.info(f'parse_futures {len(parse_futures)}')

                logging.info(f'collected len({pages_data}) pages')

        return pages_data
