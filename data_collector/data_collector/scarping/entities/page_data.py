from pydantic import BaseModel
from typing import Optional, List


class Link(BaseModel):
    url: str
    text: Optional[str]

    def __hash__(self):
        return hash((hash(self.url) + hash(self.text)))

    def __eq__(self, other):
        return isinstance(other, Link) and self.url == other.url and self.text == other.text


class PageData(BaseModel):
    page_url: str
    source_url: Optional[str]
    depth: int
    page_title: Optional[str]
    page_links: Optional[List[Link]]
