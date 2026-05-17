from .main import main
from .support import (
    CustomerSupport,
    SupportTicket,
    TicketOrderingStrategy,
    fifo_strategy,
    filo_strategy,
    random_strategy_generator,
)

__all__ = [
    "CustomerSupport",
    "SupportTicket",
    "TicketOrderingStrategy",
    "fifo_strategy",
    "filo_strategy",
    "main",
    "random_strategy_generator",
]
