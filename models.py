from typing import Optional
from datetime import datetime

class Card:
    def __init__(self,
                 front_text: str,
                 back_text: str,
                 deck_name: str = "Default",
                 due_date: Optional[datetime] = None,
                 interval: int = 1,
                 ease_factor: float = 2.5,
                 lapses: int = 0,
                 last_studied: Optional[datetime] = None,
                 id: Optional[int] = None):
        self.id = id
        self.front_text = front_text
        self.back_text = back_text
        self.deck_name = deck_name
        self.due_date = due_date if due_date is not None else datetime.now()
        self.interval = interval
        self.ease_factor = ease_factor
        self.lapses = lapses
        self.last_studied = last_studied

    def __repr__(self):
        return (f"Card(id={self.id}, front_text='{self.front_text}', "
                f"deck_name='{self.deck_name}', due_date={self.due_date})")