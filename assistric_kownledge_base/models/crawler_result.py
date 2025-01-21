from pydantic import BaseModel

class CrawlerResult(BaseModel):
    url: str