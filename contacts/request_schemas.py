from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


def to_snake_case(string: str) -> str:
    return ''.join(['_' + i.lower() if i.isupper() else i for i in string]).lstrip('_')


class Contact(BaseModel):
    user_id: str
    first_name: str = Field(description = "First name of contact" )
    last_name: str = Field(description = "Last name of contact")
    company_name: str = Field(description = "Company name of contact")
    email: str = Field(description = "Email of contact")
    created_at: Optional[datetime]


    class Config:
        alias_generator = to_snake_case


