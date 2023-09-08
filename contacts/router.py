from fastapi import APIRouter, status, Request, Response, UploadFile
from contacts.schemas import Contact
from contacts.response_schemas import Error, response as res
import csv
from db import MongoDB
from config import MONGODB_DB, MONGODB_URI

# all contact related end point
router = APIRouter()

#get db
db = MongoDB(MONGODB_URI, MONGODB_DB)

db.ping_db()

#get single contact
@router.get("/{contact_id}",
         tags=["contacts"],
         summary="Get Contact",
         description="This is a decription",
         responses={
             status.HTTP_200_OK:{"model": Contact}
         }
)
async def get_single_contact(request: Request, response: Response):
    """ Gets a signle contact """
    response.status_code = status.HTTP_200_OK

    data = Contact(firstName="edi", lastName="abdullah", companyName="the company", email="some.email@email.com")
    error = Error(code=0, message="success") 
    res_data = res()
    res_data.set_data(data)
    res_data.set_status(error)

    return res_data

# upload csv data to db
@router.post("/upload-contact-file", 
             tags=["contact"],
             summary="This endpoint to upload user csv file",
             responses={
                 status.HTTP_200_OK:{"model": Contact}
             })

async def upload_csv_file(file: UploadFile):
    """ upload csv file """

    res_data = res()

    if file.content_type != "text/csv":
        res_data.set_status(Error(code=1, message="file is not allowed!"))
        return res_data
    
    #contents = await file.read()

    contacts = []
    contents = await file.read()
    decoded_contents = contents.decode("utf-8").splitlines()

    try:
        reader = csv.DictReader(decoded_contents)
        for row in reader:
            contact = Contact(**row)
            contacts.append(contact.dict())
    except Exception as e:
        res_data.set_status(Error(code=2, message="error at parsing file!"))
        return res_data

    # write content in database
    cursor = db.insert_many("contacts", contacts)
    

    if cursor.inserted_ids == None:
        res_data.set_status(Error(code=1, message="file is not allowed!"))
        return res_data
    

    return res_data.set_status(Error(code=0, message="success"))