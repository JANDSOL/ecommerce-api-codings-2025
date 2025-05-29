from decimal import Decimal
from typing import Annotated

from sqlmodel import SQLModel, Field, Column, Numeric


class ProductBase(SQLModel):
    title: str
    image: str
    seller_full_name: str
    price: Decimal = Field(sa_column=Column(Numeric(6, 2)))  # (Valor máximo=9999.99)
    rating: Annotated[float, Field(le=5)]


class Product(ProductBase, table=True):
    id: Annotated[int | None, Field(primary_key=True)] = None
