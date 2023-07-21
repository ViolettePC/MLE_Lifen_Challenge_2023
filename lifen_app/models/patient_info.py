from pydantic import BaseModel


class PatientName(BaseModel):
    first_name: str | None
    last_name: str | None
