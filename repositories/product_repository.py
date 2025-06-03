from sqlmodel import Session, select, func
from models.product import Product


class ProductRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_by_id(self, product_id: int) -> Product | None:
        return self.session.get(entity=Product, ident=product_id)

    def list(
        self, title_filter: str | None, page: int = 0, limit_per_page: int = 10
    ) -> list[Product]:
        st_product = select(Product)
        if title_filter:
            st_product = st_product.where(
                func.lower(Product.title).like(f"%{title_filter.lower()}%")
            )
        st_product = st_product.offset(page).limit(limit_per_page)
        results = self.session.exec(st_product)

        return list(results)

    def create(self, product: Product) -> Product:
        self.session.add(product)
        self.session.commit()
        self.session.refresh(product)

        return product

    def update(self, product: Product) -> Product:
        self.session.add(product)
        self.session.commit()
        self.session.refresh(product)

        return product

    def delete(self, product: Product) -> None:
        self.session.delete(product)
        self.session.commit()
