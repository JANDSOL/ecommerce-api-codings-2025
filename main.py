from contextlib import asynccontextmanager

from fastapi import FastAPI

from db import create_db_and_table
from utils.const import ACTUAL_VERSION


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_table()
    yield


app = FastAPI(
    title="E-Commerce API",
    description="RESTful API to manage an e-commerce.",
    version=ACTUAL_VERSION,
    lifespan=lifespan,
)
