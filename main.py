from fastapi import FastAPI
import uvicorn
from sqlalchemy.sql.functions import user


from db import database

app = FastAPI()


async def startup_event():
    await database.connect()


async def shutdown_event():
    await database.disconnect()


app.add_event_handler("startup", startup_event)
app.add_event_handler("shutdown", shutdown_event)

app.include_router(user.app, tags=['users'])

if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host='localhost',
        port=8000,
        reload=True
    )