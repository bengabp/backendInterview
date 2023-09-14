from pydantic import BaseModel, Field, validator
from typing import List
from datetime import datetime


class UploadedFileInDB(BaseModel):
    filename: str = Field(description="Name of the file")
    uid: str = Field(description="Unique ID of the file")
    uploaded_date: datetime = Field(
        description="Date of the file upload",
        alias="uploadedDate",
        default=datetime.utcnow(),
    )
    total_contacts: int = Field(
        description="Total number of contacts in the file", alias="totalContacts"
    )


class UploadedFileContentInDB(BaseModel):
    contacts_file_uid: str
    file_content: str


class ContactInDB(BaseModel):
    contact_uid: str = Field(description="Unique ID of the contact")
    first_name: str = Field(description="First name", alias="firstName")
    last_name: str = Field(description="Last name", alias="lastName")
    email: str = Field(description="Email")
    company_name: str = Field(description="Company name", alias="companyName")
    uploaded_date: datetime = Field(
        description="Date of upload", alias="uploadedDate", default=datetime.utcnow()
    )
    contacts_file_uid: str = Field(description="Unique ID of contacts file")
