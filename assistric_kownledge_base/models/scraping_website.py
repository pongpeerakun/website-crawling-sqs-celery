from pydantic import BaseModel

class ScrapingWebsite(BaseModel):
    id: str
    url: str   
