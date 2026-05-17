import uuid
from dataclasses import dataclass, field

TICKET_NAMESPACE = uuid.UUID(int=5)


def ticket_id(customer: str, issue: str) -> str:
    return str(uuid.uuid5(TICKET_NAMESPACE, f"{customer}:{issue}"))


@dataclass
class SupportTicket:
    customer: str
    issue: str
    id: str = field(init=False)

    def __post_init__(self) -> None:
        self.id = ticket_id(self.customer, self.issue)

    def __str__(self) -> str:
        return (
            "=================================="
            f"Processing ticket id: {self.id}"
            f"Customer: {self.customer}"
            f"Issue: {self.issue}"
            "=================================="
        )

    def process(self) -> None:
        print(str(self))
