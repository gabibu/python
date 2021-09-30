
from abc import ABC, abstractmethod
from shellapp.entities.newsitems import TopStories, HackerNewsItem

class NewsClient(ABC):

    @abstractmethod
    def get_top_stories(self) -> TopStories:
        pass

    @abstractmethod
    def get_story_details(self, item_id: int) -> HackerNewsItem:
        pass