from decimal import Decimal
from fastapi import UploadFile

from models.product import Product
from utils.const import FOLDER_NAME_IMG_UPLOAD
from utils.file_utils import save_image, delete_file
from repositories.product_repository import ProductRepository


class ProductService:
    def __init__(self, repository: ProductRepository):
        self.repository = repository

    def list_product(self, title: str | None, page: int, limit_per_page: int):
        return self.repository.list(title, page, limit_per_page)

    def get_product(self, product_id: int) -> Product:
        product = self.repository.get_by_id(product_id)
        if not product:
            raise KeyError("Producto no encontrado")
        return product

    def create_product(
        self,
        title: str,
        seller: str,
        price: Decimal,
        rating: float,
        image_file: UploadFile,
    ) -> Product:
        # Guardar la img en el servidor
        if image_file.size == 0:
            raise ValueError("Ingresa una imagen correcta")
        image_path = save_image(file=image_file, folder=FOLDER_NAME_IMG_UPLOAD)
        new_product = Product(
            title=title,
            seller_full_name=seller,
            price=price,
            rating=rating,
            image=image_path,
        )
        return self.repository.create(new_product)

    def update_product(
        self,
        product_id: int,
        title: str | None,
        seller: str | None,
        price: Decimal | None,
        rating: float | None,
        image_file: UploadFile | None,
    ) -> Product:
        product = self.get_product(product_id)

        if image_file:
            delete_file(product.image)
            product.image = save_image(file=image_file, folder=FOLDER_NAME_IMG_UPLOAD)
        if title is not None and title != "":
            product.title = title
        if seller is not None and seller != "":
            product.seller_full_name = seller
        if price is not None and price != "":
            product.price = price
        if rating is not None and rating != "":
            product.rating = rating

        return self.repository.update(product)

    def delete_product(self, product_id: int) -> None:
        product = self.get_product(product_id)

        delete_file(product.image)
        self.repository.delete(product)
