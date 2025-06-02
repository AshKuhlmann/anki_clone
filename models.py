from typing import Optional
from datetime import datetime

# SQLAlchemy imports
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship, declarative_base

# Initialize SQLAlchemy's declarative base
Base = declarative_base()

class DeckModel(Base):
    __tablename__ = 'decks'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False, index=True)

    # Relationship to CardModel (CardModel will be defined in the next prompt)
    cards = relationship("CardModel", back_populates="deck")

    def __repr__(self):
        return f"<DeckModel(id={self.id}, name='{self.name}')>"

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

class UserConfig:
    def __init__(self,
                 default_new_card_interval: int = 1,
                 starting_ease_factor: float = 2.5):
        self.default_new_card_interval = default_new_card_interval
        self.starting_ease_factor = starting_ease_factor

    def __repr__(self):
        return (f"UserConfig(default_new_card_interval={self.default_new_card_interval}, "
                f"starting_ease_factor={self.starting_ease_factor})")

class CardModel(Base):
    __tablename__ = 'cards'

    id = Column(Integer, primary_key=True, index=True)
    front_text = Column(String, nullable=False)
    back_text = Column(String, nullable=False)
    due_date = Column(DateTime, nullable=False)
    interval = Column(Integer, nullable=False, default=1)
    ease_factor = Column(Float, nullable=False, default=2.5)
    lapses = Column(Integer, nullable=False, default=0)
    last_studied = Column(DateTime, nullable=True)

    deck_id = Column(Integer, ForeignKey('decks.id'), nullable=False, index=True) # Foreign key to DeckModel
    deck = relationship("DeckModel", back_populates="cards") # Relationship back to DeckModel

    def __repr__(self):
        return f"<CardModel(id={self.id}, front_text='{self.front_text[:20]}...')>"