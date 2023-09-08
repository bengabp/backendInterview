from fastapi import FastAPI, status, Request, Response, Depends
from contacts.schemas import Contact
from contacts.router import router as contact_router

app = FastAPI()

app.include_router(contact_router)
#app.add_route()