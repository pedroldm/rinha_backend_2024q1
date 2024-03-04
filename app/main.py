from app.db.database import create_tables, create_context
from contextlib import asynccontextmanager
from app.api.routers.clients import client_router
from fastapi import FastAPI
import os

@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_tables()
    await create_context(os.path.dirname(os.path.abspath(__file__)) + "/db/context.sql")
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(client_router, prefix="/clientes")
