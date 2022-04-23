from dataclasses import dataclass, field
from typing import Set

from ..product import Product


@dataclass
class Store:
    name: str
    products: Set[Product] = field(default_factory=set)

    def is_available(self, product: Product) -> bool:
        if product in self.products:
            print(f"The product {product.name} is available")
            return True

        print(f"The product {product.name} is not available")
        return False

    def add_product(self, product: Product) -> None:
        self.products.add(product)
