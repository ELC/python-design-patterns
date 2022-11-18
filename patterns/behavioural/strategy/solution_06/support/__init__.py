from .app import (
    CustomerSupport,
    random_strategy,
    fifo_strategy,
    filo_strategy,
    ProcessingTypes,
)
from .ticket import SupportTicket


STRATEGIES = {
    ProcessingTypes.FIFO: fifo_strategy,
    ProcessingTypes.FILO: filo_strategy,
    ProcessingTypes.RANDOM: random_strategy,
}


__all__ = [
    "CustomerSupport",
    "SupportTicket",
    "STRATEGIES",
    "ProcessingTypes"
]
