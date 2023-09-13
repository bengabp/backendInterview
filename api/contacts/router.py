from fastapi import UploadFile
from fastapi.routing import APIRouter

from config import logger

contacts_router = APIRouter()


@contacts_router.post("/contacts")
async def upload_csv(csv_file: UploadFile):
    logger.debug(csv_file.content_type)
    logger.debug(csv_file.filename)
    return {}


@contacts_router.get("/contacts")
async def get_contacts_by_date(date: str):
    logger.debug(date)
    return {}


@contacts_router.get("/contacts/{uid}")
async def get_contacts_by_uid(uid: str, response: str):
    logger.debug(uid)
    logger.debug(response)
    return {}


@contacts_router.delete("/contacts/{uid}")
async def delete_contacts(uid: str):
    logger.debug(uid)
    return {}
