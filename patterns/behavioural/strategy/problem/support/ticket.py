import uuid
from dataclasses import dataclass, field


@dataclass
class SupportTicket:
    customer: str
    issue: str
    id: str = field(init=False)

    def __post_init__(self) -> None:
        self.id = uuid.uuid4().hex

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
