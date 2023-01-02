
import requests
from os import path
from http import HTTPStatus

from shellapp.entities.newsitems import TopStories, HackerNewsItem
from shellapp.newsclients.hackernewapiutils import HackerNewApiUtils
from shellapp.newsclients.newsclient import NewsClient

class HackerNewsAPIClient(NewsClient):

    BASE_URL = "hacker-news.firebaseio.com"
    API_VERSION = "v0"
    TOP_STORIES_API = "topstories.json"
    API_PROTOCOL = "https://"
    ITEM_DETAILS_SERVICE_NAME = "item"
    JSON_PREFIX = ".json"
    FORMAT_ENTITY = "{}"


    def __init__(self):

        self._top_stories_url = path.join(HackerNewsAPIClient.API_PROTOCOL,
                                          HackerNewsAPIClient.BASE_URL,
                                          HackerNewsAPIClient.API_VERSION,
                                          HackerNewsAPIClient.TOP_STORIES_API)

        self._item_details_url_format =  path.join(HackerNewsAPIClient.API_PROTOCOL, HackerNewsAPIClient.BASE_URL,
                                                   HackerNewsAPIClient.API_VERSION,
                                                   HackerNewsAPIClient.ITEM_DETAILS_SERVICE_NAME,
                                                   HackerNewsAPIClient.FORMAT_ENTITY, HackerNewsAPIClient.JSON_PREFIX)


    def get_top_stories(self) -> TopStories:
        top_stories_ids = self._call_api(self._top_stories_url)

        return TopStories(top_stories_ids = top_stories_ids)

    def get_story_details(self, item_id: int) -> HackerNewsItem:

        try:
            url = self._item_details_url_format.format(item_id)

            response = self._call_api(url)
            hey_toptional = lambda json_dict, key, default_val: json_dict[key] if key in json_dict else default_val

            #TODO: CHANGE TO MISSING EXCEPTIOPN
            return HackerNewsItem(writer =
                           hey_toptional(response, HackerNewApiUtils.WRITER, None),
                           number_of_descendants = hey_toptional(response, HackerNewApiUtils.NUMBER_OF_DESCENDANTS, None),
                           id = hey_toptional(response, HackerNewApiUtils.ID, None),
                           kids_items  = hey_toptional(response, HackerNewApiUtils.KIDS_ITEMS_IDS, []),
                           score = hey_toptional(response, HackerNewApiUtils.SCORE, None),
                           time = hey_toptional(response, HackerNewApiUtils.TIME, None),
                           title = hey_toptional(response, HackerNewApiUtils.TITLE, None),
                           type = hey_toptional(response, HackerNewApiUtils.TYPE, None),
                           url = hey_toptional(response, HackerNewApiUtils.URL, None),
                           deleted = hey_toptional(response, HackerNewApiUtils.DELETED, False),
                           is_dead = hey_toptional(response, HackerNewApiUtils.IS_DEAD, False)

                           )
        except Exception as e:
            print(e)
            print(item_id)
            raise e

    def _call_api(self, url: str):
        response = requests.get(url)

        if response.status_code != HTTPStatus.OK:
            raise Exception("response {} for url {}".format(response.status_code, url))

        return response.json()



# api = HackerNewsAPIClient()
# r = api.get_top_stories()
#
# for x in r.top_stories_ids:
#     api.get_item_details(x)


# print(r)