from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field


def to_snake_case(string: str) -> str:
    return ''.join(['_' + i.lower() if i.isupper() else i for i in string]).lstrip('_')


class ContactResponseModel(BaseModel):
    user_id: str
    first_name: str = Field(description = "First name of contact" )
    last_name: str = Field(description = "Last name of contact")
    company_name: str = Field(description = "Company name of contact")
    email: str = Field(description = "Email of contact")


    class Config:
        alias_generator = to_snake_case

class ContactListResponse(BaseModel):
    uid: str
    uploadDate: str
    totalContacts: int

class ContactsList(BaseModel):
    contacts : List[ContactResponseModel]
    total_contacts_number: int


class ContactCSV(BaseModel):
    first_name: str = Field(description = "First name of contact" )
    last_name: str = Field(description = "Last name of contact")
    company_name: str = Field(description = "Company name of contact")
    email: str = Field(description = "Email of contact")