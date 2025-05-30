from dataclasses import dataclass, field
from datetime import date

@dataclass
class Card:
    ease_factor: float = 2.5
    interval: int = 0  # days until next review
    review_count: int = 0
    due_date: date = field(default_factory=date.today)