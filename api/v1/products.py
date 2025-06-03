from decimal import Decimal, InvalidOperation
from typing import Annotated
from fastapi import (
    Form,
    File,
    Query,
    status,
    Depends,
    APIRouter,
    UploadFile,
    HTTPException,
)
from fastapi.responses import JSONResponse

from dependencies import SessionDep
from utils.logging_config import logger
from schemas.product import ProductRead
from utils.const import PRODUCTS_NAME_PATH
from services.product_service import ProductService
from repositories.product_repository import ProductRepository

router = APIRouter()


def get_service(session: SessionDep):
    repo = ProductRepository(session)
    return ProductService(repo)


@router.post(
    f"/{PRODUCTS_NAME_PATH}/",
    response_model=ProductRead,
    status_code=status.HTTP_201_CREATED,
)
async def create_product(
    title: str = Form(...),
    seller_full_name: str = Form(...),
    price: Decimal = Form(...),
    rating: float = Form(...),
    image: UploadFile = File(...),
    service: ProductService = Depends(get_service),
):
    """Create a product with form data and image file."""
    try:
        product = service.create_product(
            title,
            seller_full_name,
            price,
            rating,
            image,
        )
        logger.info(f"Product created: {product.id}")
        return product
    except Exception as e:
        logger.error(f"Error while creating a product: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="¡Ha ocurrido un error al intentar guardar un producto, vuelve a intentarlo!",
        )
