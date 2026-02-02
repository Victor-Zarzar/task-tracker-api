from pydantic import BaseModel


class Location(BaseModel):
    city: str | None = None
    region: str | None = None
    country: str | None = None
    loc: str | None = None
    lat: float | None = None
    lon: float | None = None
