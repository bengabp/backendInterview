from fastapi import APIRouter, status, Request, Response
from contacts.schemas import Contact
from contacts.response_schemas import DataModel, Error, response as res

# all contact related end point
router = APIRouter()

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

    # data = Contact()
    # data.company_name = "the company"
    # data.last_name = "abdullah"
    # data.email = "edi.abdullah@email.com"
    # data.first_name = "edi"
    data = Contact(firstName="edi", lastName="abdullah", companyName="the company", email="some.email@email.com")
    error = Error(code=0, message="success") 
    res_data = res()
    res_data.set_data(data)
    res_data.set_status(error)

    return res_data

    #return {"contact": {"name": "edi", "address": "semarang"}}

# upload csv data to db
