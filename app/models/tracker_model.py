from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class Location(BaseModel):
    city: Optional[str] = None
    region: Optional[str] = None
    country: Optional[str] = None
    loc: Optional[str] = None


class CheckTracker(BaseModel):
    message: str
    visitor_ip: str
    user_agent: str
    timestamp_utc: datetime
    location: Optional[Location] = None
    page: Optional[str] = "Website"
    ref: Optional[str] = None
    status: str
