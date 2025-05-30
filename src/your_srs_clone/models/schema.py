from pydantic import BaseModel
from datetime import date, datetime
from typing import Optional

class CardBase(BaseModel):
    question: str
    answer: str

class CardCreate(CardBase):
    pass

class CardUpdate(CardBase):
    pass

class CardResponse(CardBase):
    id: int
    review_count: int = 0
    ease_factor: float = 2.5
    interval: int = 0
    due_date: Optional[datetime] = None

    class Config:
        orm_mode = True