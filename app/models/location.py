from typing import Optional

from pydantic import BaseModel


class Location(BaseModel):
    city: Optional[str] = None
    region: Optional[str] = None
    country: Optional[str] = None
    loc: Optional[str] = None
    lat: Optional[float] = None
    lon: Optional[float] = None
