from fastapi import UploadFile
from fastapi.routing import APIRouter

from config import logger


contacts_router = APIRouter(prefix="/contacts", tags=["Contacts"])


@contacts_router.post(
    "/",
    summary="Upload contacts",
    description="This endpoint takes contacts from an user in form of a CSV file",
    responses={},
)
async def upload_csv(csv_file: UploadFile):
    return {}


@contacts_router.get(
    "/",
    summary="Get contacts from date",
    description="This endpoint returns contacts files uploaded on the date or the range specified",
    responses={},
)
async def get_contacts_by_date(date: str):
    logger.debug(date)
    return {}


@contacts_router.get(
    "/{contacts_file_uid}",
    summary="Get contacts from file uid",
    description="This endpoint returns contacts files or their structured data of the given file uid",
    responses={},
)
async def get_contacts_by_uid(contacts_file_uid: str, response: str):
    logger.debug(contacts_file_uid)
    logger.debug(response)
    return {}


@contacts_router.delete(
    "/{contacts_file_uid}",
    summary="Delete contacts from file uid",
    description="This endpoint deletes contacts files of the given file uid",
    responses={},
)
async def delete_contacts(contacts_file_uid: str):
    logger.debug(contacts_file_uid)
    return {}
