from pydantic import BaseModel
from typing import List, Optional
from datetime import date

class CardBase(BaseModel):
    question: str
    answer: str

class CardCreate(CardBase):
    pass

class CardUpdate(BaseModel):
    question: Optional[str] = None
    answer: Optional[str] = None

class CardResponse(CardBase):
    id: int
    ease_factor: float
    interval: int
    review_count: int
    due_date: date

    class Config:
        orm_mode = True

class DeckBase(BaseModel):
    name: str

class DeckCreate(DeckBase):
    pass

class DeckResponse(DeckBase):
    id: int

    class Config:
        orm_mode = True

class CardDeckCreate(BaseModel):
    card_id: int
    deck_id: int