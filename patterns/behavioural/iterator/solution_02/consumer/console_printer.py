from collections.abc import Iterable

from typing import Protocol


class PrintableItem(Protocol):
    def __str__(self) -> str:
        ...


class ConsolePrinter:
    def print(self, collection: Iterable[PrintableItem]):

        iterator = iter(collection)

        while True:
            try:
                item = next(iterator)
                print(item)
            except StopIteration:
                break
