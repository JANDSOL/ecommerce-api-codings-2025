"""Módulo que configura el logger de la aplicación."""

import logging


logger = logging.getLogger(__name__)

logger.setLevel(logging.DEBUG)


formatter = logging.Formatter(
    fmt="%(asctime)s - %(levelname)s - [%(filename)s] - %(message)s",
    datefmt="%d/%m/%Y %H:%M:%S",
)


file_handler = logging.FileHandler(filename="app.log", encoding="utf-8")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
