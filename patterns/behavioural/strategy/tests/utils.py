from collections.abc import Iterable


def assert_customers_in_order(output: str, customers: Iterable[str]) -> None:
    positions = [output.index(customer) for customer in customers]
    assert positions == sorted(positions)
