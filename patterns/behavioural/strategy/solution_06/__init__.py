from .main import main
from .support import (
    CustomerSupport,
    ProcessingTypes,
    STRATEGIES,
    SupportTicket,
    TicketOrderingStrategy,
)
from .support.app import fifo_strategy, filo_strategy, random_strategy

__all__ = [
    "CustomerSupport",
    "ProcessingTypes",
    "STRATEGIES",
    "SupportTicket",
    "TicketOrderingStrategy",
    "fifo_strategy",
    "filo_strategy",
    "main",
    "random_strategy",
]
