from dataclasses import dataclass, field
from typing import List

from ..producer import Producer

from ..product import Product


@dataclass
class Store:
    name: str
    producers: List[Producer] = field(default_factory=list)

    def is_available(self, product: Product) -> bool:
        answer_from_producers = [
            producer.is_available(product) for producer in self.producers
        ]

        return any(answer_from_producers)
