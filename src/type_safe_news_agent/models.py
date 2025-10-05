# Structured Output Model (Pydantic)
from datetime import datetime

from pydantic import BaseModel, HttpUrl


class NewsSummary(BaseModel):
    title: str
    url: HttpUrl
    summary: str
    published_at: datetime
    source: str
