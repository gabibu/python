
from pydantic import BaseModel
from typing import Optional

class ScrappingRequest(BaseModel):

    page_url: str
    source_url: Optional[str]
    depth_from_initial: int

class PageHtml(BaseModel):
    page_url: str
    source_url: Optional[str]
    depth_from_initial: int
    html: Optional[str]
