from dataclasses import dataclass
from typing import List

from ..store import Store

from ..product import Product


@dataclass
class Customer:
    name: str
    interests: List[Product]
    satisfied: bool = False

    def ask_for_interests(self, store: Store) -> None:
        for product in self.interests:
            if not store.is_available(product):
                return

        self.satisfied = True
