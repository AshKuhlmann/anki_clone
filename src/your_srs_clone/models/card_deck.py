from sqlalchemy import Column, Integer, ForeignKey
from .base import Base

class CardDeckModel(Base):
    __tablename__ = "card_deck"

    card_id = Column(Integer, ForeignKey("cards.id"), primary_key=True)
    deck_id = Column(Integer, ForeignKey("decks.id"), primary_key=True)

    def __repr__(self):
        return f"<CardDeckModel(card_id={self.card_id}, deck_id={self.deck_id})>"