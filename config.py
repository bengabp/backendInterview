import logging
import json

from pydantic_settings import BaseSettings
from logging import Formatter
from enum import Enum


class Config(BaseSettings):
    APP_NAME: str = "contacts-app"
    LOG_LEVEL: str = "DEBUG"


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


config = Config()
logger = logging.getLogger(config.APP_NAME)
handler = logging.StreamHandler()
handler.setFormatter(JsonFormatter())
logger.handlers = [handler]
logger.setLevel(config.LOG_LEVEL)
logging.getLogger("uvicorn.access").disabled = True
