from ..iterables import Aggregate

from typing import Protocol


class PrintableItem(Protocol):
    def __str__(self) -> str:
        ...


class ConsolePrinter:
    def print(self, collection: Aggregate[PrintableItem]):

        iterator = collection.create_iterator()

        while iterator.has_more():
            item = iterator.next()
            print(item)
