import asyncio

from bson import ObjectId
from fastapi.encoders import jsonable_encoder
from motor.motor_asyncio import AsyncIOMotorClient

from config import MONGO_DB_URL, MONGODB_NAME
from contacts.request_schemas import Contact
from contacts.response_schemas import ContactListResponse


class ContactDatabase():
    cluster = AsyncIOMotorClient(MONGO_DB_URL)
    cluster.get_io_loop = asyncio.get_running_loop
    db_name = cluster[MONGODB_NAME]
    contact_collection = db_name["Contacts"]

    # for testing purpose use local mongodb

    # cluster = AsyncIOMotorClient("mongodb://localhost:27017")
    # cluster.get_io_loop = asyncio.get_running_loop
    # db_name = cluster[MONGODB_NAME]
    # contact_collection = db_name["Contacts"]
# //////////////////////////////////////////////////////////////

    async def create(payload: Contact):
        document = jsonable_encoder(payload)
        result = await ContactDatabase.contact_collection.insert_one(document)
        document["_id"] = result.inserted_id
        return document

    async def get_by_id(id_res: ObjectId):
        result = await ContactDatabase.contact_collection.find_one({"_id": id_res})
        print(result)
        return result

    async def delete_by_id(user_id: str):
        result = await ContactDatabase.contact_collection.delete_many({"user_id": user_id})
        return result

    async def get_all_contacts(params: dict):
        contacts_list = []
        filter = {"created_at": {"$lte": (params["start_date"]),  '$options': 'i'}}
        if (params["end_date"]) is not None:
            filter = {
                "created_at":  {"$gte": (params["start_date"]),"$lte": (params["end_date"])},
            }
        contacts = await ContactDatabase.contact_collection.aggregate([
            {
                "$match": {"created_at": filter}
            },
            {"$project": {
                "uid": "$user_id",
                "uploadDate": "$created_at",
                "totalContacts": {"$count": {"$push": "$user_id"}}},
             }
        ]).to_list(None)
        if contacts:
            contacts = ContactListResponse(**contacts[0])
            contacts_list.append(contacts)
        return contacts_list

    async def get_all(id_res: str):
        contact_list = await ContactDatabase.contact_collection.aggregate([
            {
                "$match": {"user_id": str(id_res)}
            }]).to_list(None),
        return contact_list

    # generic database method
    async def get_by_where_clause(self, where_clause: dict):
        data = await ContactDatabase.contact_collection.find_one(where_clause)
        return data

    # async def get_all(params):
    #     contacts = []
    #     filter = {"created_at": params["start_date"]}
    #     if (params["end_date"]) is not None :
    #         filter = {
    #             "created_at": {'$regex': params['start_date', "end_date"],  '$options': 'i'},
    #         }
    #     cursor = await ContactDatabase.find(filter, {"name": 1, "role": 1, "effectiveFromYear": 1}).sort(
    #         params["order_by"], params["order_direction"]).skip(params["skip"]).limit(params["size"])
    #     async for document in cursor:
    #         document["id"] = str(document["_id"])
    #         del document["_id"]
    #         contacts.append(document)
