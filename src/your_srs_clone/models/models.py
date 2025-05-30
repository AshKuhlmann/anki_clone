from sqlalchemy import Column, Integer, String, ForeignKey, Date, Float, Text
from sqlalchemy.orm import relationship
from .base import Base
from datetime import date  # Ensure date is imported

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    # Add other user fields if necessary, e.g., email, hashed_password

class Deck(Base):
    __tablename__ = 'decks'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))  # Assuming decks belong to users
    # For hierarchical decks:
    # parent_deck_id = Column(Integer, ForeignKey('decks.id'), nullable=True)
    # children = relationship('Deck', backref=backref('parent', remote_side=[id]))

    notes = relationship("Note", back_populates="deck")

class Note(Base):
    __tablename__ = 'notes'
    id = Column(Integer, primary_key=True, index=True)
    deck_id = Column(Integer, ForeignKey('decks.id'), nullable=False)
    front = Column(Text, nullable=False)  # Use Text for potentially longer content
    back = Column(Text, nullable=False)
    tags = Column(String, nullable=True)  # e.g., "tag1,tag2" or use a separate association table for many-to-many tags

    deck = relationship("Deck", back_populates="notes")
    cards = relationship("Card", back_populates="note")

class Card(Base):  # This is the SQLAlchemy model for a card
    __tablename__ = 'cards'
    id = Column(Integer, primary_key=True, index=True)
    note_id = Column(Integer, ForeignKey('notes.id'), nullable=False)
    # Fields from your_srs_clone.core.card.Card for persistence
    ease_factor = Column(Float, default=2.5, nullable=False)
    interval = Column(Integer, default=0, nullable=False)      # days
    review_count = Column(Integer, default=0, nullable=False)
    due_date = Column(Date, default=date.today, nullable=False)

    note = relationship('Note', back_populates="cards")
    review_logs = relationship("ReviewLog", back_populates="card")

class ReviewLog(Base):
    __tablename__ = 'review_logs'
    id = Column(Integer, primary_key=True, index=True)
    card_id = Column(Integer, ForeignKey('cards.id'), nullable=False)
    review_date = Column(Date, default=date.today, nullable=False)
    quality = Column(Integer, nullable=False)  # 0-5 rating

    card = relationship("Card", back_populates="review_logs")