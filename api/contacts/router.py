import csv
import codecs

from fastapi import UploadFile, Depends, BackgroundTasks
from fastapi.routing import APIRouter
from fastapi.responses import JSONResponse, StreamingResponse
from bson import objectid

from config import HTTPStatus, config
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
    OutputForContacts,
)
from api.contacts import (
    is_valid_file_csv_type,
    is_valid_csv_columns,
    get_csv_headers,
    process_csv_file_handler,
    get_contacts_from_date_query,
    file_exists_for_user,
    delete_contacts_by_contacts_file_uid,
    get_contacts_file_content_by_uid,
    get_contacts_file_metadata_by_uid,
    get_download_file_buffer,
    get_user,
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
async def upload_csv(
    csv_file: UploadFile,
    background_tasks: BackgroundTasks,
    user_id: str = Depends(get_user),
):
    if not is_valid_file_csv_type(csv_file.content_type):
        return JSONResponse(
            status_code=HTTPStatus.BAD_REQUEST,
            content=dict(
                status=HTTPStatus.BAD_REQUEST,
                details=f"Invalid content-type: {csv_file.content_type}",
            ),
        )

    csv_reader = csv.reader(codecs.iterdecode(csv_file.file, "utf-8"))
    csv_headers = get_csv_headers(csv_reader)
    if not is_valid_csv_columns(csv_headers):
        return JSONResponse(
            status_code=HTTPStatus.BAD_REQUEST,
            content=dict(
                status=HTTPStatus.BAD_REQUEST,
                details=f"Invalid columns: {csv_headers}",
            ),
        )

    contacts_file_uid = str(objectid.ObjectId())
    background_tasks.add_task(
        process_csv_file_handler, user_id, contacts_file_uid, csv_file, csv_reader
    )
    return JSONResponse(
        status_code=HTTPStatus.ACCEPTED,
        content={
            "contacts_file_uid": contacts_file_uid,
            "filename": csv_file.filename,
            "Content-Type": config.CSV_MIME_TYPE,
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
    user_id: str = Depends(get_user),
):
    response_list = [
        item async for item in get_contacts_from_date_query(request, user_id)
    ]
    return GetContactsByDateResponse(contacts=response_list)


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
    user_id: str = Depends(get_user),
):
    if not await file_exists_for_user(request.contacts_file_uid, user_id):
        return JSONResponse(
            content=dict(
                status=HTTPStatus.NOT_FOUND, details="No file found with given uid"
            ),
            status_code=HTTPStatus.NOT_FOUND,
        )
    if request.output == OutputForContacts.STRUCTURED:
        contacts_file_metadata = await get_contacts_file_metadata_by_uid(
            request.contacts_file_uid
        )
        return ContactsFileInDBResponse(**contacts_file_metadata)
    else:
        contacts_file_content = await get_contacts_file_content_by_uid(
            request.contacts_file_uid
        )
        csv_file_buffer = get_download_file_buffer(contacts_file_content)
        return StreamingResponse(
            content=csv_file_buffer,
            status_code=HTTPStatus.OK,
            media_type=config.CSV_MIME_TYPE,
            headers={
                "Content-Type": config.CSV_MIME_TYPE,
                "Content-Disposition": f"attachment; filename={str(contacts_file_content['_id'])}.csv",
            },
        )


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
    background_tasks: BackgroundTasks,
    request: DeleteContactsByUIDQuery = Depends(DeleteContactsByUIDQuery),
    user_id: str = Depends(get_user),
):
    if not await file_exists_for_user(request.contacts_file_uid, user_id):
        return JSONResponse(
            content=dict(
                status=HTTPStatus.NOT_FOUND, details="No file found with given uid"
            ),
            status_code=HTTPStatus.NOT_FOUND,
        )
    background_tasks.add_task(
        delete_contacts_by_contacts_file_uid, request.contacts_file_uid
    )
    return JSONResponse(
        status_code=HTTPStatus.ACCEPTED,
        content={"deletion_status": "Scheduled for deletion"},
    )
