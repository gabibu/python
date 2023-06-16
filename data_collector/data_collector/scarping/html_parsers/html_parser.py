from bs4 import BeautifulSoup
from typing import Set
import re
from typing import Optional

from data_collector.scarping.entities.page_data import Link


class HtmlParser:

    URL_REGEX = re.compile("^http?(s)://")

    def __init__(self, html: str):
        self._soup = BeautifulSoup(html, 'html.parser')

    def get_title(self) -> Optional[str]:
        return self._soup.title.string if self._soup.title is not None else None

        title_element = self._soup.find('title')
        return title_element.text if title_element is not None else None

    def get_urls(self) -> Optional[Set[Link]]:
        urls = {Link(url=link.get('href'), text=link.text) for link in
                self._soup.findAll('a', attrs={'href': HtmlParser.URL_REGEX})}

        return urls if len(urls) > 0 else None


class HtmlParserFactory:

    def create_html_parser(self, html: str) -> HtmlParser:
        return HtmlParser(html)
