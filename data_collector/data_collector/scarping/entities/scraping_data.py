from pydantic import BaseModel
from typing import Optional, List

class ScrappingData(BaseModel):
    page_url: str
    page_title: str
    page_links: Optional[List[str]]