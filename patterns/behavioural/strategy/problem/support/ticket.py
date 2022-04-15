import uuid
from dataclasses import dataclass, field


@dataclass
class SupportTicket:
    customer: str
    issue: str
    id: str = field(init=False)

    def __post_init__(self):
        self.id = str(uuid.uuid4())

    def process(self) -> str:
        return (
            "=================================="
            f"Processing ticket id: {self.id}"
            f"Customer: {self.customer}"
            f"Issue: {self.issue}"
            "=================================="
        )
