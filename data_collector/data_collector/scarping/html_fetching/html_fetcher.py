import requests
import logging

class HtmlFetcher:

    def __init__(self):
        pass

    def get_html(self, url) -> str:
        try:

            html = requests.get(url).text
            return html
        except Exception as e:
            logging.exception(url)
            raise e
