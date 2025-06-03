from contextlib import asynccontextmanager

from fastapi import FastAPI

from db import create_db_and_table
from utils.logging_config import logger
from utils.const import ACTUAL_VERSION


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_table()
    logger.info("Starting the application and creating tables if necessary...")
    yield
    logger.info("Completing the application")


app = FastAPI(
    title="E-Commerce API",
    description="RESTful API to manage an e-commerce.",
    version=ACTUAL_VERSION,
    lifespan=lifespan,
)
