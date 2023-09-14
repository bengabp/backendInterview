from pydantic import BaseModel, Field, validator, model_validator
from typing import List
from datetime import datetime

from api.contacts.schemas import UploadedFileInDB


class ErrorResponse(BaseModel):
    status: int = Field(description="HTTP status code of the error")
    details: str = Field(description="Details of the error")

    @validator("status")
    def validate_status(cls, v):
        if 400 <= v <= 599:
            return v
        raise ValueError(f"Incorrect HTTP status code value for error: {v}")


class UploadFileResponse(BaseModel):
    id: str = Field(description="File UID of uploaded file", alias="contacts_file_uid")
    filename: str = Field(description="Filename of uploaded file")
    content_type: str = Field(
        description="Content type of uploaded file", alias="Content-Type"
    )


class GetContactsByDateResponse(BaseModel):
    contacts: List[UploadedFileInDB] = Field(
        description="List of contacts file as stored in DB"
    )
    total_contacts: int = Field(
        description="Total count of found contacts file",
        alias="totalContacts",
        default=0,
    )

    @model_validator(mode="after")
    def update_total_contacts(cls, obj):
        contacts: List[UploadedFileInDB] = obj.contacts
        for contact in contacts:
            obj.total_contacts += contact.total_contacts
        return obj


class ContactsFileInDBResponse(UploadedFileInDB):
    pass


class DeleteFileResponse(UploadFileResponse):
    deletion_status: str = Field(
        description="Status of delete operation", alias="deletionStatus"
    )
