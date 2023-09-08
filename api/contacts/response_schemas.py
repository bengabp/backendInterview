from pydantic import BaseModel,Field
from typing import List

class SuccessRespose(BaseModel):
    message: str

class ErrorResponse(BaseModel):
    message: str

class Token(BaseModel):
    access_token:str
    token_type: str




class ContactFile(BaseModel):
    uid:str = Field(description = "Uniquely Identifies the Contact File", alias="uid")
    upload_date:str = Field(description = "Date at which file was uploaded", alias="uploadDate")
    total_contacts:int = Field(description = "Total Number of Contacts in the File", alias="totalContacts")


class ContactFileResponseList(BaseModel):
    contacts:List[ContactFile] = Field(description = "A List consisting of information about each contact file", alias="Contacts")
    total_contacts:int = Field(description="Total Number of Contacts in all the files",alias="totalContacts")