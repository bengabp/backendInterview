import logging

from contextlib import asynccontextmanager
from fastapi import FastAPI
from starlette.middleware.base import BaseHTTPMiddleware

from api.contacts.router import contacts_router
from config import logger


class LogMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        response = await call_next(request)
        logger.info(
            "Incoming request",
            extra={
                "req": {"method": request.method, "url": str(request.url)},
                "res": {
                    "status_code": response.status_code,
                },
            },
        )
        return response


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Initialising the app...")
    logger.info("Done")
    yield
    logger.info("Shutting down the app...")
    logger.info("Done")


app = FastAPI(lifespan=lifespan)
app.add_middleware(LogMiddleware)
app.include_router(contacts_router)
