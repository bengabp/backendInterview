
import json
import os
from datetime import datetime
from io import BytesIO
from uuid import UUID

import pandas as pd
from fastapi import APIRouter, File, Query, UploadFile, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import FileResponse, JSONResponse

from contacts.manager import ContactManager
from contacts.request_schemas import Contact
from contacts.response_message import SERVER_TO_BUSY, ResponseMessage

router = APIRouter()
excel_file_path = "example.csv"


class ContctController():
    def __init__(self):
        self.contact_manager = ContactManager()

    @router.post("/import-csv/", tags=["Contacts"], status_code=status.HTTP_200_OK, response_model=Contact,
                 responses={status.HTTP_401_UNAUTHORIZED: {"model": ResponseMessage},
                            status.HTTP_400_BAD_REQUEST: {"model": ResponseMessage},
                            status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": ResponseMessage}},
                 summary="Import Contacts",
                 description="Import Contacts using CSV file.")
    async def create(user_id: UUID, file: UploadFile = File(...)):
        try:
            if str(file.filename.split('.')[-1]) != 'csv':
                return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                                    content={"status": False, "message": "Accepts only .csv file."})
            contents = file.file.read()
            buffer = BytesIO(contents)
            df = pd.read_csv(buffer)
            buffer.close()
            test = df.to_json(orient='records')
            csv_data = json.loads(test)
            file.file.seek(0, os.SEEK_END)
            file.file.close()
            created_contacts = await ContactManager.create(user_id, csv_data)
            return JSONResponse(status_code=status.HTTP_200_OK,
                                content=jsonable_encoder(created_contacts))
        
        except Exception as e:
            print("Exception", e)
            error = {
                "status": False,
                "message": SERVER_TO_BUSY
            }
            return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content=error)

    @router.get("/Download CSV file/", tags=["Contacts"])
    async def serve_excel(user_id: UUID):
        try:
            db_response = await ContactManager.get_csv_export(user_id)
            if db_response:

                headers = {
                    'Content-Disposition': 'attachment; filename="example.csv"'}

                return FileResponse(
                    excel_file_path, headers=headers
                )
        except Exception as e:
            message = ResponseMessage(
                success=False, message=SERVER_TO_BUSY)
            response = JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content=jsonable_encoder(message))
            return response    

    @router.get("/", tags=["Contacts"],
                summary="Get Contact list",
                description="Returns a contact list",
                status_code=status.HTTP_200_OK,
                response_model="",
                responses={status.HTTP_401_UNAUTHORIZED: {"model": ResponseMessage},
                           status.HTTP_422_UNPROCESSABLE_ENTITY: {"model": ResponseMessage},
                           status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": ResponseMessage}}
                )
    async def get(start_date: str = datetime.now(),
                  end_date: str = Query(None, description="End date for the date range")):

        params = {
            "start_date": start_date,
            "end_date": end_date,
        }

        try:
            response = await ContactManager.get_list(params)
            return JSONResponse(status_code=status.HTTP_200_OK, content=jsonable_encoder(response))

        except Exception as e:
            message = ResponseMessage(
                success=False, message=SERVER_TO_BUSY)
            response = JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content=jsonable_encoder(message))
            return response


    @router.get("/{Uid}/",
                summary="Get Contact by id",
                description="Returns contact details", tags=["Contacts"],
                responses={status.HTTP_200_OK: {"model": Contact},
                           status.HTTP_401_UNAUTHORIZED: {"model": ResponseMessage},
                           status.HTTP_404_NOT_FOUND: {"model": ResponseMessage},
                           status.HTTP_422_UNPROCESSABLE_ENTITY: {"model": ResponseMessage},
                           status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": ResponseMessage}})
    async def get_by_id(Uid: str) -> ResponseMessage:
        try:
            db_response = await ContactManager.get_by_id(Uid)
            if not isinstance(db_response, ResponseMessage):
                return JSONResponse(status_code=status.HTTP_200_OK, content=jsonable_encoder(db_response))
            return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content=jsonable_encoder(db_response))

        except Exception as e:
            message = ResponseMessage(
                success=False, message=SERVER_TO_BUSY)
            response = JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content=jsonable_encoder(message))
            return response


    @router.delete("/{user_id}/",
                   status_code=status.HTTP_204_NO_CONTENT,
                   response_model=[],
                   tags=["Contacts"],
                   responses={
                       status.HTTP_401_UNAUTHORIZED: {"model": ResponseMessage},
                       status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": ResponseMessage},
                       status.HTTP_422_UNPROCESSABLE_ENTITY: {"model": ResponseMessage},
                       status.HTTP_403_FORBIDDEN: {"model": ResponseMessage},
                       status.HTTP_404_NOT_FOUND: {"model": ResponseMessage}},
                   summary="Deleted All contacts by user_id",
                   description="Deleted Contact by id")
    async def delete_by_id(user_id: str) -> ResponseMessage:
        try:
            response = await ContactManager.delete_by_id(user_id)
            if response.success:
                return JSONResponse(status_code=status.HTTP_200_OK, content=jsonable_encoder(response))
            return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content=jsonable_encoder(response))

        except Exception as e:
            message = ResponseMessage(
                success=False, message=SERVER_TO_BUSY)
            response = JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content=jsonable_encoder(message))
            return response
