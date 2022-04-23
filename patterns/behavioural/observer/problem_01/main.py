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

    late_customer = Customer(name="bob", interests=[cellphone, couch, mug])
    late_customer_arrival = 3

    store = Store(name="AllYouNeed")

    initial_time = time.time()

    products = [cellphone, couch, mug]
    estimated_time_arrivals = [1, 2, 4]

    notification_period = 1

    while True:
        current_time = time.time() - initial_time

        for product, eta in zip(products, estimated_time_arrivals):
            if current_time >= eta and product not in store.products:
                store.add_product(product)

        if current_time >= late_customer_arrival and late_customer not in customers:
            customers.append(late_customer)

        for customer in customers:
            customer.ask_for_interests(store)

        if all(customer.satisfied for customer in customers):
            break

        time.sleep(notification_period)


if __name__ == "__main__":
    main()
