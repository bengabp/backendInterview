import logging
import json
import motor.motor_asyncio as motor_aio

from pydantic_settings import BaseSettings
from logging import Formatter
from typing import Set


class Config(BaseSettings):
    APP_NAME: str = "contacts-app"
    LOG_LEVEL: str = "DEBUG"
    MANDATORY_HEADERS: Set[str] = {"firstName", "lastName", "email", "companyName"}
    MONGO_URI: str
    MONGO_DB_NAME: str
    DATE_FORMAT: str = "%Y-%m-%d"
    MAX_ON_MEMORY_FILE_SIZE: int = 1024000000
    JWT_SECRET: str


class HTTPStatus:
    OK = 200
    ACCEPTED = 202

    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    NOT_FOUND = 404
    UNPROCESSABLE_ENTITY = 422


class JsonFormatter(Formatter):
    def __init__(self):
        super(JsonFormatter, self).__init__()

    def format(self, record):
        json_record = {}
        json_record["message"] = record.getMessage()
        json_record["level"] = record.levelname
        json_record["logger"] = record.name
        json_record["module"] = record.module
        json_record["file"] = record.filename
        json_record["line"] = record.lineno

        if "req" in record.__dict__:
            json_record["req"] = record.__dict__["req"]
        if "res" in record.__dict__:
            json_record["res"] = record.__dict__["res"]
        if record.levelno == logging.ERROR and record.exc_info:
            json_record["err"] = self.formatException(record.exc_info)
        return json.dumps(json_record)


def connect_db():
    return motor_aio.AsyncIOMotorClient(config.MONGO_URI)[config.MONGO_DB_NAME]


config = Config()

logger = logging.getLogger(config.APP_NAME)
handler = logging.StreamHandler()
handler.setFormatter(JsonFormatter())
logger.handlers = [handler]
logger.setLevel(config.LOG_LEVEL)
logging.getLogger("uvicorn.access").disabled = True

db = connect_db()
