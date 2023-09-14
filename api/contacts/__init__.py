import asyncio
import base64

from fastapi import UploadFile
from typing import List
from datetime import datetime
from bson.objectid import ObjectId

from config import config, db, logger
from api.contacts.schemas import ContactInDB, UploadedFileInDB, UploadedFileContentInDB
from api.contacts.request_schemas import GetContactsByDateQuery


def is_valid_file_csv_type(content_type: str):
    return content_type == "text/csv"


def is_valid_csv_columns(csv_columns: List[str]):
    return config.MANDATORY_HEADERS.issubset(set(csv_columns))


def get_csv_headers(csv_reader):
    csv_headers = []
    for row in csv_reader:
        csv_headers = row.copy()
        return csv_headers
    return []


async def process_csv_file_handler(
    contacts_file_uid: str, csv_file: UploadFile, csv_reader
):
    total_contacts = await process_csv_file_contact_items(csv_reader, contacts_file_uid)
    await store_file_content_in_db(contacts_file_uid, csv_file)
    return await store_file_metadata_in_db(
        contacts_file_uid, csv_file.filename, len(total_contacts)
    )


async def process_csv_file_contact_items(csv_reader, contacts_file_uid: str):
    insert_one_tasks = []
    for row in csv_reader:
        db_doc = ContactInDB(
            **{
                "contact_uid": str(ObjectId()),
                "firstName": row[0],
                "lastName": row[1],
                "email": row[2],
                "companyName": row[3],
                "contacts_file_uid": contacts_file_uid,
            }
        )
        logger.debug(f"{db_doc=}")
        insert_one_tasks.append(store_contact_in_db(db_doc))

    return await asyncio.gather(*insert_one_tasks)


async def store_file_metadata_in_db(
    contacts_file_uid: str, csv_filename: str, total_contacts: int
):
    db_doc_file_meta = UploadedFileInDB(
        **{
            "filename": csv_filename,
            "uid": contacts_file_uid,
            "totalContacts": total_contacts,
        }
    )
    logger.debug(f"{db_doc_file_meta=}")
    file_metadata_collection = db["file_metadata"]
    return await file_metadata_collection.insert_one(
        db_doc_file_meta.model_dump(by_alias=True)
    )


async def store_file_content_in_db(contacts_file_uid: str, csv_file: UploadFile):
    await csv_file.seek(0)
    file_content = await csv_file.read()
    file_content_b64 = base64.b64encode(file_content).decode("utf-8")
    db_doc_file_content = UploadedFileContentInDB(
        **{
            "contacts_file_uid": contacts_file_uid,
            "file_content": file_content_b64,
        }
    )
    logger.debug(f"{db_doc_file_content=}")
    file_content_collection = db["file_content"]
    return await file_content_collection.insert_one(
        db_doc_file_content.model_dump(by_alias=True)
    )


async def store_contact_in_db(doc: ContactInDB):
    csv_contact_collection = db["items"]
    return await csv_contact_collection.insert_one(doc.model_dump(by_alias=True))


async def get_contacts_from_date(date_request: GetContactsByDateQuery):
    if date_request.is_range:
        mongo_query = {
            "uploadedDate": {
                "$gte": date_request._start_date,
                "$lte": date_request._end_date,
            }
        }
    else:
        mongo_query = {"uploadedDate": date_request._date}
    file_metadata_collection = db["file_metadata"]
    return file_metadata_collection.find(mongo_query)
