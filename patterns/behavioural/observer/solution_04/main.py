import time
from .customer import Customer
from .product import Product
from .store import Store


def main() -> None:
    cellphone = Product("MobileX", "TechS", 300)
    couch = Product("GiantSofa", "AllComfort", 800)
    mug = Product("CoffeeM", "IndustrialTea", 20)

    customers = [
        Customer(name="John", interests=[cellphone]),
        Customer(name="Mary", interests=[couch, mug]),
        Customer(name="Alicia", interests=[cellphone, mug]),
    ]

    store = Store(name="AllYouNeed")

    for customer in customers:
        store.subscribe(customer, customer.interests)

    late_customer = Customer(name="bob", interests=[cellphone, couch, mug])
    late_customer_arrival = 3

    customers.append(late_customer)

    initial_time = time.time()

    products = [cellphone, couch, mug]
    estimated_time_arrivals = [1, 2, 4]

    while True:
        current_time = time.time() - initial_time

        for product, eta in zip(products, estimated_time_arrivals):
            if current_time >= eta and product not in store.products:
                store.add_product(product)

        if current_time >= late_customer_arrival and not store.is_subscribed(
            late_customer
        ):
            store.subscribe(late_customer, late_customer.interests)

        if all(customer.satisfied for customer in customers):
            break

        time.sleep(0.05)  # To avoid blocking CPU


if __name__ == "__main__":
    main()
