from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from app.models.location import Location


class CheckTracker(BaseModel):
    message: str
    visitor_ip: str
    user_agent: str
    timestamp_utc: datetime
    location: Optional[Location] = None
    page: Optional[str] = None
    ref: Optional[str] = None
    status: str
    url: str
    endpoint: str
    reason: Optional[str] = None
