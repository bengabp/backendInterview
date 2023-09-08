from fastapi import FastAPI
import uvicorn

from contacts.router import router as contact_router
import config

app = FastAPI()

app.include_router(contact_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=config.HOST, port=config.PORT)