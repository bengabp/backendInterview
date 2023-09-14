from enum import Enum
from datetime import datetime
from pydantic import BaseModel, model_validator, Field
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
    _start_date: Optional[datetime] = None
    _end_date: Optional[datetime] = None
    _date: Optional[datetime] = None

    @staticmethod
    def _validate_date(date):
        return datetime.strptime(date, "%Y/%m/%d")

    @staticmethod
    def _validate_date_range(date_range):
        dates = date_range.split(" - ")
        return datetime.strptime(dates[0], "%Y/%m/%d"), datetime.strptime(
            dates[1], "%Y/%m/%d"
        )

    @model_validator(mode="after")
    def validate_date(cls, obj):
        date = obj.date[1:-1]
        try:
            if "-" in date:
                obj.is_range = True
                (
                    obj._start_date,
                    obj._end_date,
                ) = GetContactsByDateQuery._validate_date_range(date)
            else:
                obj._date = GetContactsByDateQuery._validate_date(date)
            return obj

        except Exception as e:
            print("--------Here")
            print(type(e))
            print(str(e))
            return ValueError("Invalid date")
