from asyncio import Protocol
from dataclasses import dataclass, field
from typing import Callable, Dict, List, Set
from collections import defaultdict

from ..product import Product


NOTIFY_FUNCTION = Callable[[Product], None]


@dataclass
class Store:
    name: str
    products: Set[Product] = field(default_factory=set)
    product_notifiers: Dict[Product, List[NOTIFY_FUNCTION]] = field(
        default_factory=lambda: defaultdict(list)
    )

    def subscribe(
        self, notifier: NOTIFY_FUNCTION, relevant_products: List[Product]
    ) -> None:
        for product in relevant_products:
            self.product_notifiers[product].append(notifier)
            if product in self.products:
                notifier(product)

    def is_subscribed(self, notifier: NOTIFY_FUNCTION) -> bool:
        all_notifiers: List[NOTIFY_FUNCTION] = sum(self.product_notifiers.values(), [])
        return notifier in all_notifiers

    def add_product(self, product: Product) -> None:
        self.products.add(product)
        self.notify(product)

    def notify(self, product: Product) -> None:
        for notifier in self.product_notifiers[product]:
            notifier(product)
