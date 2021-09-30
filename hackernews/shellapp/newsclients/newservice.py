
from typing import List

from shellapp.newsclients.newsclient import NewsClient
from shellapp.entities.newsitems import HackerNewsItem

class NewService:

    def __init__(self, news_api_client: NewsClient, max_top_storied_to_return: int):
        self._news_api_client = news_api_client
        self._max_top_storied_to_return = max_top_storied_to_return


    def _get_story_details(self, story_id: int, story_rank: int) -> HackerNewsItem:
        store_details = self._news_api_client.get_story_details(story_id)
        store_details.item_rank = story_rank
        return store_details

    def get_top_stories(self) -> List[HackerNewsItem]:

        top_stories_ids = self._news_api_client.get_top_stories()

        top_stories_details = [self._get_story_details(story_id, story_rank + 1) for
                       (story_rank, story_id) in enumerate(top_stories_ids.top_stories_ids[0: self._max_top_storied_to_return])]

        return top_stories_details
