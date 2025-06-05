from decimal import Decimal, InvalidOperation
from typing import Annotated
from fastapi import (
    Form,
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
from utils.const import PRODUCTS_NAME_PATH, UPLOAD_ROOT, FOLDER_NAME_IMG_UPLOAD
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
    title: Annotated[str, Form()],
    image: UploadFile,
    seller_full_name: Annotated[str, Form()],
    price: Annotated[Decimal, Form(ge=0, max_digits=6, decimal_places=2)],
    rating: Annotated[float, Form(ge=0, le=5)],
    service: Annotated[ProductService, Depends(get_service)],
):
    """Create a product with form data and image file."""
    product = service.create_product(
        title,
        seller_full_name,
        price,
        rating,
        image,
    )
    logger.info("Product created: %s", product.id)
    return product


@router.get(
    path=f"/{PRODUCTS_NAME_PATH}/",
    response_model=list[ProductRead],
    status_code=status.HTTP_200_OK,
    summary="Get products with pagination and filter by title",
    responses={
        200: {
            "description": "List of products obtained.\n\nIt may be empty if there are no matches.",
            "content": {
                "application/json": {
                    "examples": {
                        "empty": {"summary": "Without products", "value": []},
                        "populated": {
                            "summary": "With products",
                            "value": [
                                {
                                    "id": 1,
                                    "title": "Producto X",
                                    "image": f"/{UPLOAD_ROOT}/{FOLDER_NAME_IMG_UPLOAD}/asf0a7gasf33.jpg",
                                    "seller_full_name": "Ana Prado",
                                    "price": "25.99",
                                    "rating": 4.75,
                                },
                                {
                                    "id": 2,
                                    "title": "Producto Y",
                                    "image": f"/{UPLOAD_ROOT}/{FOLDER_NAME_IMG_UPLOAD}/099afa8sfasf.png",
                                    "seller_full_name": "Jesús Adrian",
                                    "price": "99.99",
                                    "rating": 5,
                                },
                            ],
                        },
                    }
                }
            },
        },
        422: {
            "description": "Validation error in query parameters.",
            "content": {
                "application/json": {
                    "example": {
                        "detail": [
                            {
                                "type": "int_parsing",
                                "loc": ["query", "page"],
                                "msg": "Input should be a valid integer, unable to parse string as an integer",
                                "input": "asffs",
                            },
                            {
                                "type": "int_parsing",
                                "loc": ["query", "limit-per-page"],
                                "msg": "Input should be a valid integer, unable to parse string as an integer",
                                "input": "3asd",
                            },
                        ]
                    }
                }
            },
        },
        500: {
            "description": "Internal server error. May occur due to unexpected failures.",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Error interno del servidor. Por favor, intente de nuevo."
                    }
                }
            },
        },
    },
)
async def get_products(
    service: Annotated[ProductService, Depends(get_service)],
    title: Annotated[
        str | None, Query(description="Optional filter by product title")
    ] = None,
    page: Annotated[int, Query(ge=0, description="Page number (starts at 0)")] = 0,
    limit_per_page: Annotated[
        int,
        Query(gt=0, alias="limit-per-page", description="Number of results per page"),
    ] = 10,
):
    """
    Returns a paginated list of products.

    - You can return an empty list if no matches with the filter `title`.
    - The result will always be `application/json`.
    - Code 422 if parameters `page` or `limit-per-page` are not valid integers.
    - Code 500 for server-internal errors.
    """

    products = service.list_product(title, page, limit_per_page)
    return products


@router.get(path="/%s/{product_id}" % PRODUCTS_NAME_PATH, response_model=ProductRead)
async def get_product(
    product_id: int, service: Annotated[ProductService, Depends(get_service)]
):
    """Get a product by your ID"""
    try:
        product = service.get_product(product_id)
        return product
    except KeyError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Producto no encontrado"
        ) from e


@router.patch(path="/%s/{product_id}" % PRODUCTS_NAME_PATH, response_model=ProductRead)
async def update_product(
    product_id: int,
    service: Annotated[ProductService, Depends(get_service)],
    title: Annotated[str | None, Form()] = None,
    image: UploadFile | None = None,
    seller_full_name: Annotated[str | None, Form()] = None,
    price: Annotated[Decimal | None, Form(ge=0, max_digits=6, decimal_places=2)] = None,
    rating: Annotated[float | None, Form(ge=0, le=5)] = None,
):
    """Update (partially) an existing product; replace the image if sent."""
    try:
        # decimal_price = Decimal(price) if price not in (None, "") else None
        product = service.update_product(
            product_id, title, seller_full_name, price, rating, image
        )
        logger.info("Product updated: %s", product.id)
        return product
    except InvalidOperation as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Precio no es un decimal válido",
        ) from e
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La calificación del producto no es un decimal válido",
        ) from e
    except KeyError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Producto no encontrado"
        ) from e


@router.delete(
    path="/%s/{product_id}" % PRODUCTS_NAME_PATH, status_code=status.HTTP_204_NO_CONTENT
)
async def delete_product(
    product_id: int, service: Annotated[ProductService, Depends(get_service)]
):
    """Remove a product by its ID, also deleting its image from the server."""
    try:
        service.delete_product(product_id)
        logger.info("Product deleted: %s", product_id)
        return JSONResponse(status_code=status.HTTP_204_NO_CONTENT, content={})
    except KeyError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Producto no encontrado"
        ) from e
