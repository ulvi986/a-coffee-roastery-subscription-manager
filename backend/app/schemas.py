"""Pydantic schemas for the generated API."""
from pydantic import BaseModel, Field, field_validator


def _clean_title(value: str) -> str:
    value = value.strip()
    if not value:
        raise ValueError("title must not be blank")
    return value


class ItemCreate(BaseModel):
    title: str = Field(min_length=1, max_length=300)

    _clean = field_validator("title")(_clean_title)


class ItemUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=300)
    completed: bool | None = None

    _clean = field_validator("title")(_clean_title)


class Item(BaseModel):
    id: int
    title: str
    completed: bool
    createdAt: str
