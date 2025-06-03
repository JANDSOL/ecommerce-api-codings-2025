from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from db import create_db_and_table
from utils.logging_config import logger
from utils.const import ACTUAL_VERSION, UPLOAD_ROOT, V1, PRODUCTS_NAME_PATH
from api.v1.products import router as v1_product_router


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

app.mount(
    path=f"/{UPLOAD_ROOT}", app=StaticFiles(directory=UPLOAD_ROOT), name=UPLOAD_ROOT
)


@app.get("/")
def read_root():
    return {"message": "E-Commerce API en funcionamiento"}


app.include_router(
    router=v1_product_router,
    prefix=f"/api/{V1}",
    tags=[f"{PRODUCTS_NAME_PATH.title()} {V1.upper()}"],
)
