"""Tools for file handling"""

import os
import shutil
from uuid import uuid4
from fastapi import UploadFile

from .const import UPLOAD_ROOT

os.makedirs(UPLOAD_ROOT, exist_ok=True)


def save_image(file: UploadFile, folder: str = "") -> str:
    filename = file.filename or ""
    file_extension = os.path.splitext(filename)[1]
    unique_filename = f"{uuid4().hex}{file_extension}"

    subfolder_path = os.path.join(UPLOAD_ROOT, folder) if folder else UPLOAD_ROOT
    os.makedirs(subfolder_path, exist_ok=True)

    file_path = os.path.join(subfolder_path, unique_filename)

    with open(file=file_path, mode="wb") as buffer:
        shutil.copyfileobj(fsrc=file.file, fdst=buffer)

    return file_path.replace(os.sep, "/")


def delete_file(file_path: str) -> None:
    if os.path.exists(file_path):
        os.remove(file_path)
