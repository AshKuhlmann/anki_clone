from sqlalchemy import Column, Integer, String, Date
from .base import Base

class CardModel(Base):
    __tablename__ = "cards"

    id = Column(Integer, primary_key=True, index=True)
    question = Column(String, index=True)
    answer = Column(String, index=True)
    ease_factor = Column(Integer, default=250)  # Stored as integer (250 = 2.5)
    interval = Column(Integer, default=0)
    review_count = Column(Integer, default=0)
    due_date = Column(Date)

    def to_card(self):
        from your_srs_clone.core.card import Card
        from datetime import date

        # Convert SQLAlchemy model to application model
        return Card(
            ease_factor=self.ease_factor / 100.0,
            interval=self.interval,
            review_count=self.review_count,
            due_date=self.due_date or date.today()
        )

    @classmethod
    def from_card(cls, card):
        # Convert application model to SQLAlchemy model
        return cls(
            question=card.question,
            answer=card.answer,
            ease_factor=int(card.ease_factor * 100),
            interval=card.interval,
            review_count=card.review_count,
            due_date=card.due_date
        )