from pydantic import BaseModel, Field, validator
from typing import List
from datetime import datetime


class UploadedFileInDB(BaseModel):
    filename: str = Field(description="Name of the file")
    uid: str = Field(description="Unique ID of the file")
    uploaded_date: datetime = Field(
        description="Date of the file upload", alias="uploadedDate"
    )
    total_contacts: int = Field(
        description="Total number of contacts in the file", alias="totalContacts"
    )
