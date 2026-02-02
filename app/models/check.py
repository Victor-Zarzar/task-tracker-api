from datetime import datetime

from pydantic import AnyHttpUrl, BaseModel

from app.models.location import Location


class CheckTracker(BaseModel):
    message: str
    visitor_ip: str
    user_agent: str
    timestamp_utc: datetime
    location: Location | None = None
    page: AnyHttpUrl | None = None
    status: str
    url: str
    endpoint: str
    reason: str | None = None
