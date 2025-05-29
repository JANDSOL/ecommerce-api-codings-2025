import os
from pathlib import Path

from dotenv import load_dotenv
from sqlmodel import SQLModel, create_engine

env_pro = Path(".env.prod")
load_dotenv(dotenv_path=env_pro)

DATABASE_URL = os.getenv("DATABASE_URL")
if DATABASE_URL is None:
    DATABASE_URL = ""
engine = create_engine(url=DATABASE_URL, echo=False)


def create_db_and_table():
    SQLModel.metadata.create_all(engine)
