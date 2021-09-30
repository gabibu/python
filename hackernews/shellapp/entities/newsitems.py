
from pydantic import BaseModel
from typing import List, Optional

class HackerNewsItem(BaseModel):
    writer: str
    number_of_descendants: Optional[int]
    id: int
    kids_items: Optional[List[int]]
    score:int
    time: int
    title: str
    type: str
    url: Optional[str]
    deleted: bool
    is_dead: bool
    item_rank: Optional[int]



class TopStories(BaseModel):

    top_stories_ids : List[int]



