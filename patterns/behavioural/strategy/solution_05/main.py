from functools import partial

from .support import CustomerSupport, random_strategy, SupportTicket


def main() -> None:
    app = CustomerSupport()

    tickets = [
        SupportTicket("John Smith", "My computer makes strange sounds!"),
        SupportTicket("Linus Sebastian", "I can't upload any videos, please help."),
        SupportTicket("Arjan Codes", "VSCode doesn't automatically solve my bugs."),
    ]

    for ticket in tickets:
        app.add_ticket(ticket)

    random_strategy_with_seed = partial(random_strategy, seed=5)

    app.process_tickets(random_strategy_with_seed)


if __name__ == "__main__":
    main()
