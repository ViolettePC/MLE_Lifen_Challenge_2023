from pydantic import BaseModel, model_validator
from lifen_app.labels.documents import NeedsOCRCase


class CoordinatesSchema(BaseModel):
    x_min: float
    x_max: float
    y_min: float
    y_max: float


class WordSchema(BaseModel):
    text: str
    bbox: CoordinatesSchema


class PageSchema(BaseModel):
    words: list[WordSchema]


class DocumentInputSchema(BaseModel):
    pages: list[PageSchema]
    original_page_count: int
    needs_ocr_case: NeedsOCRCase

    @model_validator(mode="before")
    def validate_page_count_coherency(cls, values):
        if len(values["pages"]) != values["original_page_count"]:
            raise ValueError(
                f'Page number inconsistency (expected: {values["original_page_count"]}'
                f', received:({len(values["pages"])}).'
            )

        return values
