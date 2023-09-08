from pydantic import BaseModel



def to_snake_case(string: str) -> str:
    return ''.join(['_' + i.lower() if i.isupper() else i for i in string]).lstrip('_')


class ResponseMessage(BaseModel):
    success: bool
    message: str

    class Config:
        alias_generator = to_snake_case
    
SERVER_TO_BUSY = "Server is too busy at the moment"