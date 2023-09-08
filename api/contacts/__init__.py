from fastapi import UploadFile,Depends,HTTPException, status
from api.contacts.request_schemas import UserInDB
from api.contacts.response_schemas import ContactFile,ContactFileResponseList
from api.contacts.schema import Contact
from api.config import FAKE_USERS_DB,MONGO_DB_URL,MONGO_DB_DATABASE,OAUTH2_SCHEMA
from typing import List,Annotated,Union,Tuple
from datetime import datetime
import pandas as pd
import pymongo
import uuid
import json






# Helper functions for Task 1
def is_valid_csv(file: UploadFile) -> Union[pd.DataFrame,bool]:
    # Implement validation logic to check if the uploaded file is a valid CSV
    try:
        
        df = pd.read_csv(file.file)
        unique_columns = set(df.columns.to_list())
        needed_columns = set([field.alias for _, field in Contact.model_fields.items()])
        if not needed_columns.issubset(unique_columns): # Check if user has uploaded a file which consist of all the needed columns.
            return False
        return df
    except pd.errors.EmptyDataError:
        return False
    except:
        return df
    
def parse_csv(df: pd.DataFrame) -> List[dict]:
   
    
    fields_required = [field.alias for _,field in Contact.model_fields.items()]
    df = df[fields_required]
    return df.to_json(orient = 'records')

def save_contacts_to_database(user_email:str, contacts_data: List[dict]):
    """Save Contact Data to our Underlying database"""

    contact_file_uuid = uuid.uuid4()
    contact_file_uuid_string = str(contact_file_uuid)
    
    client = pymongo.MongoClient(MONGO_DB_URL)
    db = client[MONGO_DB_DATABASE]
    # The user_contact_files collections stores all the contact_files uuid associated with a given user email
    users_contact_files = db["users_contact_files"]
    # The contact collections stores the actual content for all contacts associated with a given contact_files uuid
    contacts = db["contacts"]
    # If user is uploading for the first time, create a new document for him/her otherwise update his/her existing info with the new contact_file uid.
    user_email_query = {"_id": user_email}
    contact_file_uuid = {"$set": {contact_file_uuid_string: True}}
    users_contact_files.update_one(user_email_query, contact_file_uuid, upsert=True)
    current_datetime = datetime.now()
    # Insert the Contacts Info with revelant metadata for the given contact file.  
    contacts.insert_one({'_id':contact_file_uuid_string,'contact_info':contacts_data,
            'uploaded_date': datetime(current_datetime.year, current_datetime.month, current_datetime.day)})


def extract_dates(date_str:str) -> Tuple[Union[datetime,None],Union[datetime,None]]:
    """Extract date range from the given user string"""
    
    date_str = date_str.replace(" ", "")
    # Split the input string by the '-' character
    date_parts = date_str.split('-')
    if len(date_parts) == 1:
        try:
            end_date = datetime.strptime(date_parts[0], '%Y/%m/%d')
        except ValueError:
            return None,None
        return None,end_date
    # Parse the start date (first part of the split)
    try:
        start_date = datetime.strptime(date_parts[0], '%Y/%m/%d')
        end_date = datetime.strptime(date_parts[1], '%Y/%m/%d')
    except ValueError:
        return None,None

    return start_date, end_date

def get_contact_files_associated_with_users(user_email:str,date:Union[None,str]) -> Union[ContactFileResponseList,bool]:
    """Get the Contact Files Information for a given user for the given date range"""
    client = pymongo.MongoClient(MONGO_DB_URL)
    db = client[MONGO_DB_DATABASE]
    users_contact_files = db["users_contact_files"]
    matching_contact_files = users_contact_files.find_one({"_id": user_email})
    contacts = db["contacts"]
    contact_object_ids = [key for key in matching_contact_files if key!='_id']
    if date is None: # if not date-range is specified then return all the documents by the user
        query = {"_id": {"$in": contact_object_ids}}
    elif date is not None:
        start_date, end_date = extract_dates(date) # extract the given date-range
        if start_date and end_date: # Otherwise get a range of date
            query = {
                "$and": [
                    {"_id": {"$in": contact_object_ids}},
                    {"uploaded_date": {"$gte": start_date, "$lte": end_date}}
                ]
            }
        elif end_date: # If only single date value is provided then only get the documents equal to user provided date
            query = {
                "$and": [
                    {"_id": {"$in": contact_object_ids}},
                    {"uploaded_date": end_date}
                ]
            }
        
        elif start_date == None and end_date == None: # Not correct output
            return False
    matching_contact_documents = contacts.find(query)
    contact_file_list = []
    total_contacts_across_files = 0
    for contact in matching_contact_documents: 
        contact_info =  json.loads(contact['contact_info'])
        contact_file_list.append(ContactFile(uid = contact['_id'],
        uploadDate = contact['uploaded_date'].strftime("%Y/%m/%d"),
        totalContacts=len(contact_info)
        ))
        total_contacts_across_files+=len(contact_info)
    return ContactFileResponseList(Contacts = contact_file_list , totalContacts = total_contacts_across_files)


def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)

def fake_decode_token(token): ## This is just for dummy purposes
    user = get_user(FAKE_USERS_DB, token)
    return user

def fake_hash_password(password: str): ## This is just for dummy purposes
    return "fakehashed" + password

async def get_current_user(token: Annotated[str, Depends(OAUTH2_SCHEMA)]):
    user = fake_decode_token(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials"
        )
    return user
