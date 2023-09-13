from pydantic import BaseModel, Field, validator
from typing import List


class ErrorResponse(BaseModel):
    status: int = Field(description="HTTP status code of the error")
    details: str = Field(description="Details of the error")

    @validator("status")
    def validate_status(cls, v):
        if 400 <= v <= 599:
            return v
        raise ValueError(f"Incorrect HTTP status code value for error: {v}")
    

class UploadFileResponse(BaseModel):
    id: str = Field(description="File UID of uploaded file", alias="contacs_file_uid")
    filename: str = Field(description="Filename of uploaded file")
    content_type: str = Field(description="Content type of uploaded file", alias="Content-Type")


class GetContactsByDateResponse(BaseModel):
    contacts: List[UploadedFileInDB] = Field(description="List of contacts file as stored in DB")
    total_contacts: int = Field(description="Total count of found contacts file", alias="totalContacts")


class DeleteFileResponse(UploadFileResponse):
    deletion_status: Field(description="Status of delete operation", alias="deletionStatus")
