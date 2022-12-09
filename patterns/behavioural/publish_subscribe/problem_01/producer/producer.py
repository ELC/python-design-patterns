from dataclasses import dataclass, field
from typing import List, Set

from ..store import Store
from ..product import Product


@dataclass
class Producer:
    name: str
    products: Set[Product] = field(default_factory=set)
    stores: List[Store] = field(default_factory=list)

    def is_available(self, product: Product) -> bool:
        if product in self.products:
            print(f"The product {product.name} is available at {self.name}")
            return True

        print(f"The product {product.name} is not available at {self.name}")
        return False

    def release_product(self, name: str, price: float) -> None:
        new_product = Product(name=name, brand=self.name, price=price)
        self.products.add(new_product)
