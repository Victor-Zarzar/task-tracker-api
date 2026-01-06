from typing import Annotated, Union

from pydantic import AnyHttpUrl, BaseModel, StringConstraints, field_validator


class TrackerSchema(BaseModel):
    page: Annotated[
        AnyHttpUrl,
        StringConstraints(min_length=1, max_length=50),
    ]

    @field_validator("page", mode="before")
    @classmethod
    def normalize_page(cls, v: Union[str, AnyHttpUrl]):
        if isinstance(v, AnyHttpUrl):
            return v

        if isinstance(v, str) and not v.startswith(("http://", "https://")):
            return f"https://{v}"

        return v
