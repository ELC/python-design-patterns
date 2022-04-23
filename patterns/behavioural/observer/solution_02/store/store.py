from dataclasses import dataclass, field
from typing import Dict, List, Set, Protocol
from collections import defaultdict

from ..product import Product


class Subscriber(Protocol):
    def notify(self, product: Product) -> None:
        ...


@dataclass
class Store:
    name: str
    products: Set[Product] = field(default_factory=set)
    product_subscribers: Dict[Product, List[Subscriber]] = field(
        default_factory=lambda: defaultdict(list)
    )

    def subscribe(
        self, subscriber: Subscriber, relevant_products: List[Product]
    ) -> None:
        for product in relevant_products:
            self.product_subscribers[product].append(subscriber)
            if product in self.products:
                subscriber.notify(product)

    def is_subscribed(self, subscriber: Subscriber) -> bool:
        all_subscribers: List[Subscriber] = sum(self.product_subscribers.values(), [])
        return subscriber in all_subscribers

    def add_product(self, product: Product) -> None:
        self.products.add(product)
        self.notify_subscribers(product)

    def notify_subscribers(self, product: Product) -> None:
        for subscriber in self.product_subscribers[product]:
            subscriber.notify(product)
