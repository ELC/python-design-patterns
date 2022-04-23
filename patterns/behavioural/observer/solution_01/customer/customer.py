from abc import ABC
from dataclasses import dataclass, field
from typing import List, Set

from ..product import Product


class Subscriber(ABC):
    def notify(self, product: Product):
        ...


@dataclass
class Customer(Subscriber):
    name: str
    interests: List[Product]
    satisfied: bool = False
    own_products: Set[Product] = field(default_factory=set)

    def notify(self, product: Product) -> None:
        if product not in self.interests:
            print(f"I'm {self.name} and I am not interested in {product.name}")
            return

        print(f"I'm {self.name} and I bought a {product.name}")
        self.own_products.add(product)
        self.satisfied = all(product in self.own_products for product in self.interests)
