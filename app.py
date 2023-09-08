from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contacts import router

app = FastAPI(prefix="/v1/")
app.include_router(router.router)
origins = ["http://localhost:3000", ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

