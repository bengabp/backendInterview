import asyncio
import base64

from fastapi import UploadFile
from typing import List
from datetime import datetime
from bson.objectid import ObjectId

from config import config, db, logger
from api.contacts.schemas import ContactInDB, UploadedFileInDB, UploadedFileContentInDB


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


async def process_csv_file(csv_file: UploadFile, contacts_file_uid: str):
    await csv_file.seek(0)
    file_content = await csv_file.read()
    file_content_b64 = base64.b64encode(file_content).decode("utf-8")
    db_doc_file_meta = UploadedFileInDB(
        **{
            "filename": csv_file.filename,
            "uid": contacts_file_uid,
            "totalContacts": 0,
        }
    )
    logger.debug(f"{db_doc_file_meta=}")
    db_doc_file_content = UploadedFileContentInDB(
        **{
            "contacts_file_uid": contacts_file_uid,
            "file_content": file_content_b64,
        }
    )
    logger.debug(f"{db_doc_file_content=}")
    await asyncio.gather(
        store_file_metadata_in_db(db_doc_file_meta),
        store_file_content_in_db(db_doc_file_content),
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

    await asyncio.gather(*insert_one_tasks)


async def store_file_metadata_in_db(doc: UploadedFileInDB):
    file_metadata_collection = db["file_metadata"]
    return await file_metadata_collection.insert_one(doc.model_dump())


async def store_file_content_in_db(doc: UploadedFileContentInDB):
    file_content_collection = db["file_content"]
    return await file_content_collection.insert_one(doc.model_dump())


async def store_contact_in_db(doc: ContactInDB):
    csv_contact_collection = db["items"]
    return await csv_contact_collection.insert_one(doc.model_dump())
