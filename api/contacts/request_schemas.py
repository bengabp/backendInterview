from enum import Enum
from datetime import datetime
from pydantic import BaseModel, validator, Field
from typing import Optional


class OutputForContacts(str, Enum):
    STRUCTURED = "structured"
    RAW = "raw"


class UIDQuery(BaseModel):
    contacts_file_uid: str = Field(description="UID of the file")


class DeleteContactsByUIDQuery(UIDQuery):
    pass


class GetContactsByUIDQuery(UIDQuery):
    output: OutputForContacts = Field(
        description="Output format", default=OutputForContacts.STRUCTURED
    )


class GetContactsByDateQuery(BaseModel):
    date: str = Field(descrition="Date or date range to get contacts")
    is_range: Optional[bool] = False

    @staticmethod
    def _validate_date(date):
        datetime.strptime(date, "%Y/%m/%d")
        return date

    @staticmethod
    def _validate_date_range(date_range):
        dates = date_range.split(" - ")
        datetime.strptime(dates[0], "%Y/%m/%d")
        datetime.strptime(dates[1], "%Y/%m/%d")
        return date_range

    @validator("date")
    def validate_date(cls, v, values):
        date = v[1:-1]
        validator_function = None
        if "-" in date:
            values["is_range"] = True
            validator_function = GetContactsByDateQuery._validate_date_range
        else:
            validator_function = GetContactsByDateQuery._validate_date

        try:
            return validator_function(date)
        except Exception as e:
            print("--------Here")
            print(type(e))
            print(str(e))
            return ValueError("Invalid date range")
