from sqlalchemy import Column, Integer, String, Date
from .base import Base
from datetime import date, timedelta

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

    def calculate_next_review(self):
        """Calculate the next review date using the SM-2 algorithm."""
        today = date.today()

        # First review is always tomorrow
        if self.review_count == 0:
            next_review = today + timedelta(days=1)
        else:
            # Calculate the interval based on the SM-2 algorithm
            ease_factor = self.ease_factor / 100.0  # Convert to float
            next_interval = int(self.interval * ease_factor)
            next_review = today + timedelta(days=next_interval)

        return next_review

    def update_after_review(self, response):
        """Update the card's SM-2 parameters after a review.

        Args:
            response: The user's response to the card ('correct', 'incorrect',
                      'hard', or 'good').
        """
        # Update review count
        self.review_count += 1

        # Convert ease factor to float for calculations
        ease_factor = self.ease_factor / 100.0

        # Adjust ease factor based on response
        if response == 'correct':
            ease_factor = min(2.9, ease_factor + 0.1)
        elif response == 'incorrect':
            ease_factor = max(1.3, ease_factor - 0.15)
        elif response == 'hard':
            ease_factor = max(1.3, ease_factor - 0.15)
        elif response == 'good':
            ease_factor = min(2.9, ease_factor + 0.05)

        # Convert back to integer for storage
        self.ease_factor = int(ease_factor * 100)

        # Update interval
        if response == 'incorrect':
            self.interval = 0  # Reset interval for incorrect answers
        else:
            if response == 'hard':
                self.interval = int(self.interval * 1.2)  # Increase interval for hard questions
            elif response == 'good':
                self.interval = int(self.interval * 1.1)  # Slightly increase interval for good questions
            else:
                self.interval = int(self.interval * ease_factor)  # Normal increase for correct answers

        # Calculate next due date
        self.due_date = self.calculate_next_review()