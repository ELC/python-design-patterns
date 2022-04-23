from .support import CustomerSupport, random_strategy_generator, SupportTicket


def main():
    app = CustomerSupport()

    tickets = [
        SupportTicket("John Smith", "My computer makes strange sounds!"),
        SupportTicket("Linus Sebastian", "I can't upload any videos, please help."),
        SupportTicket("Arjan Codes", "VSCode doesn't automatically solve my bugs."),
    ]

    for ticket in tickets:
        app.add_ticket(ticket)

    app.process_tickets(random_strategy_generator(seed=1))


if __name__ == "__main__":
    main()
