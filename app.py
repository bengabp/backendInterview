from fastapi import FastAPI, Depends
from contacts.router import router as contact_router
from config import MONGODB_DB, MONGODB_URI
from pymongo import MongoClient
from db import MongoDB

app = FastAPI()

app.include_router(contact_router)