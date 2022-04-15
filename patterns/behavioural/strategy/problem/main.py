from .support.app import CustomerSupport, ProcessingTypes
from .support.ticket import SupportTicket


def main():
    app = CustomerSupport()

    tickets = [
        SupportTicket("John Smith", "My computer makes strange sounds!"),
        SupportTicket("Linus Sebastian", "I can't upload any videos, please help."),
        SupportTicket("Arjan Codes", "VSCode doesn't automatically solve my bugs."),
    ]

    for ticket in tickets:
        app.add_ticket(ticket)

    app.process_tickets(ProcessingTypes.RANDOM, seed=5)


if __name__ == "__main__":
    main()
