from datetime import UTC, datetime

import pytest
from pydantic import ValidationError

from app.models.check import CheckTracker
from app.models.health import HealthCheckResponse
from app.models.location import Location


def test_location_defaults_are_none():
    loc = Location()
    assert loc.city is None
    assert loc.region is None
    assert loc.country is None
    assert loc.loc is None
    assert loc.lat is None
    assert loc.lon is None


def test_location_accepts_partial_fields():
    loc = Location(city="São Paulo", country="BR")
    assert loc.city == "São Paulo"
    assert loc.country == "BR"
    assert loc.region is None


def test_location_lat_lon_must_be_numbers_when_provided():
    loc = Location(lat=-23.5505, lon=-46.6333)
    assert isinstance(loc.lat, float)
    assert isinstance(loc.lon, float)

    with pytest.raises(ValidationError):
        Location(lat="invalid", lon=-46.6)


def test_health_check_response_valid():
    model = HealthCheckResponse(
        status="ok",
        message="healthy",
        details={"db": "ok"},
        response_time_ms=12.34,
    )
    assert model.status == "ok"
    assert model.details["db"] == "ok"
    assert isinstance(model.response_time_ms, float)


def test_health_check_response_details_must_be_dict():
    with pytest.raises(ValidationError):
        HealthCheckResponse(
            status="ok",
            message="healthy",
            details=["not", "a", "dict"],
            response_time_ms=1.0,
        )


def test_health_check_response_response_time_must_be_float_like():
    model = HealthCheckResponse(
        status="ok",
        message="healthy",
        details={},
        response_time_ms=5,
    )
    assert isinstance(model.response_time_ms, float)

    with pytest.raises(ValidationError):
        HealthCheckResponse(
            status="ok",
            message="healthy",
            details={},
            response_time_ms="fast",
        )


def _base_check_tracker_payload(**overrides):
    payload = {
        "message": "tracked",
        "visitor_ip": "203.0.113.10",
        "user_agent": "Mozilla/5.0",
        "timestamp_utc": datetime(2026, 2, 2, 12, 0, 0, tzinfo=UTC),
        "location": None,
        "page": "https://example.com/home",
        "status": "ok",
        "url": "https://example.com/api/v1/tracker",
        "endpoint": "/api/v1/tracker",
        "reason": None,
    }
    payload.update(overrides)
    return payload


def test_check_tracker_valid_with_page_and_no_location():
    model = CheckTracker(**_base_check_tracker_payload())
    assert model.message == "tracked"
    assert model.location is None
    assert str(model.page) == "https://example.com/home"
    assert model.timestamp_utc.tzinfo is not None


def test_check_tracker_valid_with_nested_location_model():
    model = CheckTracker(
        **_base_check_tracker_payload(
            location={
                "city": "São Paulo",
                "region": "SP",
                "country": "BR",
                "lat": -23.5505,
                "lon": -46.6333,
            }
        )
    )
    assert model.location is not None
    assert isinstance(model.location, Location)
    assert model.location.city == "São Paulo"
    assert model.location.lat == -23.5505


def test_check_tracker_page_can_be_none():
    model = CheckTracker(**_base_check_tracker_payload(page=None))
    assert model.page is None


def test_check_tracker_invalid_page_must_be_http_url():
    with pytest.raises(ValidationError):
        CheckTracker(**_base_check_tracker_payload(page="notaurl"))

    with pytest.raises(ValidationError):
        CheckTracker(**_base_check_tracker_payload(page="ftp://example.com"))


def test_check_tracker_timestamp_must_be_datetime():
    with pytest.raises(ValidationError):
        CheckTracker(**_base_check_tracker_payload(timestamp_utc="not-a-date"))


def test_check_tracker_requires_mandatory_fields():
    payload = _base_check_tracker_payload()
    payload.pop("visitor_ip")
    with pytest.raises(ValidationError):
        CheckTracker(**payload)


def test_check_tracker_reason_optional_but_type_checked():
    model = CheckTracker(**_base_check_tracker_payload(reason="rate_limited"))
    assert model.reason == "rate_limited"

    with pytest.raises(ValidationError):
        CheckTracker(**_base_check_tracker_payload(reason=123))
