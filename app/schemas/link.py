from pydantic import BaseModel
from datetime import datetime


class CreateLink(BaseModel):

    original_url: str
    custom_alias: str | None = None
    expires_at: datetime | None = None


class UpdateLink(BaseModel):

    original_url: str


class LinkStats(BaseModel):

    original_url: str
    created_at: datetime
    clicks: int
    last_used: datetime | None

