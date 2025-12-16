from pydantic import BaseModel


class HealthCheckResponse(BaseModel):
    status: str
    message: str
    details: dict
    response_time_ms: float
