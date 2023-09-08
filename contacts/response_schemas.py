from pydantic import BaseModel
from typing import Generic, List, Optional, TypeVar

# response shemas: default response
DataT = TypeVar('DataT')

class DataModel(BaseModel):
    contacts: List

class Error(BaseModel):
    code: int
    message: str

class response(BaseModel, Generic[DataT]):
    data: Optional[DataT] = None
    meta: Optional[DataT] = None
    status: Optional[DataT] = None

    def set_data(self, DataModel):
        self.data = DataModel
    
    def set_meta(self, meta=None):
        self.meta = meta

    def set_status(self, Error):
        self.status = Error