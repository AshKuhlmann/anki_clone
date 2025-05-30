from sqlalchemy import Column, Integer, String
from .base import Base

class DeckModel(Base):
    __tablename__ = "decks"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)

    def __repr__(self):
        return f"<DeckModel(name={self.name})>"