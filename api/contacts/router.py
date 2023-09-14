import csv
import codecs

from fastapi import UploadFile, Depends, BackgroundTasks
from fastapi.routing import APIRouter
from fastapi.responses import FileResponse, JSONResponse
from typing import Union
from bson import objectid

from config import logger, HTTPStatus
from api.contacts.response_schemas import (
    ErrorResponse,
    UploadFileResponse,
    GetContactsByDateResponse,
    DeleteFileResponse,
    ContactsFileInDBResponse,
)
from api.contacts.request_schemas import (
    GetContactsByDateQuery,
    GetContactsByUIDQuery,
    DeleteContactsByUIDQuery,
)
from api.contacts import (
    is_valid_file_csv_type,
    is_valid_csv_columns,
    get_csv_headers,
    process_csv_file_handler,
    # get_contacts_from_date_range,
)


contacts_router = APIRouter(prefix="/contacts", tags=["Contacts"])


@contacts_router.post(
    "/",
    summary="Upload contacts",
    description="This endpoint takes contacts from an user in form of a CSV file",
    responses={
        HTTPStatus.ACCEPTED: {"model": UploadFileResponse},
        HTTPStatus.BAD_REQUEST: {"model": ErrorResponse},
    },
)
async def upload_csv(csv_file: UploadFile, background_tasks: BackgroundTasks):
    if not is_valid_file_csv_type(csv_file.content_type):
        return ErrorResponse(
            status=HTTPStatus.BAD_REQUEST,
            details=f"Invalid content-type: {csv_file.content_type}",
        )

    csv_reader = csv.reader(codecs.iterdecode(csv_file.file, "utf-8"))
    csv_headers = get_csv_headers(csv_reader)
    if not is_valid_csv_columns(csv_headers):
        return ErrorResponse(
            status=HTTPStatus.BAD_REQUEST, details=f"Invalid columns: {csv_headers}"
        )

    contacts_file_uid = str(objectid.ObjectId())
    background_tasks.add_task(
        process_csv_file_handler, contacts_file_uid, csv_file, csv_reader
    )
    return JSONResponse(
        status_code=HTTPStatus.ACCEPTED,
        content={
            "contacts_file_uid": contacts_file_uid,
            "filename": csv_file.filename,
            "Content-Type": "text/csv",
        },
    )


@contacts_router.get(
    "/",
    summary="Get contacts from date",
    description="This endpoint returns contacts files uploaded on the date or the range specified",
    responses={
        HTTPStatus.OK: {"model": GetContactsByDateResponse},
        HTTPStatus.BAD_REQUEST: {"model": ErrorResponse},
    },
)
async def get_contacts_by_date(
    request: GetContactsByDateQuery = Depends(GetContactsByDateQuery),
):
    return {}


@contacts_router.get(
    "/{contacts_file_uid}",
    summary="Get contacts from file uid",
    description="This endpoint returns contacts files or their structured data of the given file uid",
    responses={
        HTTPStatus.OK: {"model": ContactsFileInDBResponse},
        HTTPStatus.NOT_FOUND: {"model": ErrorResponse},
    },
)
async def get_contacts_by_uid(
    request: GetContactsByUIDQuery = Depends(GetContactsByUIDQuery),
):
    logger.debug(request)
    return {}


@contacts_router.delete(
    "/{contacts_file_uid}",
    summary="Delete contacts from file uid",
    description="This endpoint deletes contacts files of the given file uid",
    responses={
        HTTPStatus.ACCEPTED: {"model": DeleteFileResponse},
        HTTPStatus.NOT_FOUND: {"model": ErrorResponse},
    },
)
async def delete_contacts(
    request: DeleteContactsByUIDQuery = Depends(DeleteContactsByUIDQuery),
):
    logger.debug(request)
    return {}
