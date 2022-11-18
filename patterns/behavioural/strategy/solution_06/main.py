from functools import partial
from typing import Any, Dict

from .support import CustomerSupport, STRATEGIES, SupportTicket, ProcessingTypes


def main(strategy: str, strategy_args: Dict[str, Any]) -> None:
    app = CustomerSupport()

    tickets = [
        SupportTicket("John Smith", "My computer makes strange sounds!"),
        SupportTicket("Linus Sebastian", "I can't upload any videos, please help."),
        SupportTicket("Arjan Codes", "VSCode doesn't automatically solve my bugs."),
    ]

    for ticket in tickets:
        app.add_ticket(ticket)

    strategy_name = strategy.upper()
    if strategy_name not in ProcessingTypes.__members__:
        raise ValueError(f"Not Valid Strategy: {strategy}")

    strategy_type = ProcessingTypes[strategy_name]
    strategy_function = STRATEGIES[strategy_type]

    random_strategy_with_seed = partial(strategy_function, **strategy_args)

    app.process_tickets(random_strategy_with_seed)


if __name__ == "__main__":
    main(strategy="random", strategy_args={"seed": 5})
