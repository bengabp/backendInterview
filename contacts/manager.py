import csv
from datetime import datetime
from uuid import UUID

from bson.errors import InvalidId

from contacts.database import ContactDatabase
from contacts.pyobject_id import PyObjectId
from contacts.request_schemas import Contact
from contacts.response_message import ResponseMessage
from contacts.response_schemas import (ContactCSV, ContactResponseModel,
                                       ContactsList)


class ContactManager():
    async def create(uid: UUID, csv_data: list):
        response_list = []
        error_list = []
        for raw_data in csv_data:

            if raw_data["First Name"] is not None or raw_data["Last Name"] is not None:
                try:
                    raw_data = {x.replace(' ', '_').lower(
                    ): v for x, v in raw_data.items()}
                    raw_data.update({"user_id": str(uid)})
                    contact_data = Contact(**raw_data)
                    contact_data.created_at = datetime.now()
                    print(contact_data)
                    where_clause = {
                        "user_id": contact_data.user_id,
                        "first_name": contact_data.first_name,
                        "last_name": contact_data.last_name,
                        "email": contact_data.email
                    }
                    check_already_exist = await ContactDatabase.get_by_where_clause(where_clause)
                    if check_already_exist:
                        continue
                    database_response = await ContactDatabase.create(contact_data)
                    if database_response:
                        response_list.append("successfully inserted")
                    else:
                        error_list.append("Not inerted")

                except Exception as e:
                    error_list.append({"Error": str(repr(e.args))})
        return ResponseMessage(success=True, message=f"{len(response_list)} Contacts have been created. and {len(error_list)} Contacts have incorrent data.")

    async def get_by_id(Uid: str):
        response = ContactManager.validate_id(Uid)
        if isinstance(response, ResponseMessage):
            return response
        data_id = response
        response = await ContactDatabase.get_by_id(data_id)
        if response:
            data = ContactResponseModel(**response)
            return data
        return ResponseMessage(success=False, message=f"Contact was not found.")

    def validate_id(id: str):
        try:
            id = PyObjectId(id)
            return id
        except InvalidId:
            return ResponseMessage(success=False, message=f" Uid '{id}' is invalid.")


# delete all contacts that store on user_id

    async def delete_by_id(Uid: UUID):
        user_id = str(Uid)
        response = await ContactDatabase.delete_by_id(user_id)
        if response.deleted_count == 0:
            return ResponseMessage(success=False, message=f"Contacts with {user_id} was not found.")
        return ResponseMessage(success=True, message=f"Contacts with {user_id} deleted.")



    async def get_list(params: dict):
        contacts_list = await ContactDatabase.get_all_contacts(params)
        if contacts_list:
            contacts = len(contacts_list)
            data_list = ContactsList(
                contacts=contacts_list, total_contacts_number=contacts)
            return data_list


    async def get_csv_export(user_id: str):
        response = await ContactDatabase.get_all(user_id)
        if response:
            header = ["First Name", "Last Name", "Company Name", "email"]
            with open('example.csv', 'w', newline='') as csvfile:
                csv_writer = csv.writer(csvfile)

                # Write the header row
                csv_writer.writerow(header)
                for contact in response[0]:
                    data = ContactCSV(**contact)
                    list_data = []
                    dict_data = dict(data)
                    for data in dict_data:
                        list_data.append(dict_data[data])

                    csv_writer.writerow(list_data)
        return csvfile

# The CSV file is automatically closed when you exit the 'with' block
# This code will create a CSV file named "example.csv" with a header row followed by the data rows.
