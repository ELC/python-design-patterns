from typing import Any, NamedTuple


class Product(NamedTuple):
    name: str
    brand: str
    price: float

    def __eq__(self, other: Any):
        if not isinstance(other, Product):
            return False
        return other.name == self.name and other.brand == self.brand
