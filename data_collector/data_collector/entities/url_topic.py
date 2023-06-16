
from pydantic import BaseModel
class UrlTopic(BaseModel):

    url: str
    topic: str
