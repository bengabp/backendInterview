from fastapi import UploadFile
from fastapi.routing import APIRouter


contacts_router = APIRouter()


@contacts_router.post("/contacts")
async def upload_csv(csv_file: UploadFile):
    print(csv_file.content_type)
    print(csv_file.filename)
    return {}


@contacts_router.get("/contacts")
async def get_contacts_by_date(date: str):
    print(date)
    return {}


@contacts_router.get("/contacts/{uid}")
async def get_contacts_by_uid(uid: str, response: str):
    print(uid)
    print(response)
    return {}


@contacts_router.delete("/contacts/{uid}")
async def delete_contacts(uid: str):
    print(uid)
    return {}
