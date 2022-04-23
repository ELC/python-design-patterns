from dataclasses import dataclass, field
from typing import List, Set

from ..product import Product
from ..customer import Customer


@dataclass
class Store:
    name: str
    products: Set[Product] = field(default_factory=set)
    customers: List[Customer] = field(default_factory=list)

    def subscribe(self, customer: Customer) -> None:
        self.customers.append(customer)
        for product in self.products:
            customer.notify(product)

    def add_product(self, product: Product) -> None:
        self.products.add(product)

        for customer in self.customers:
            customer.notify(product)
