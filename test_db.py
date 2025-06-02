from datetime import datetime
from sqlalchemy.orm import Session

import models
from database import engine, SessionLocal

def main():
    # Create the database tables (if they don't exist)
    models.Base.metadata.create_all(bind=engine)

    # Create a new deck
    deck = models.DeckModel(name="Test Deck")

    # Create some cards and add them to the deck
    card1 = models.CardModel(
        front_text="What is SQLAlchemy?",
        back_text="SQLAlchemy is a SQL toolkit and Object-Relational Mapping (ORM) library for Python.",
        due_date=datetime.now(),
        deck=deck
    )

    card2 = models.CardModel(
        front_text="What is a flashcard?",
        back_text="A flashcard is a card with information on both sides, used for learning and memorization.",
        due_date=datetime.now(),
        deck=deck
    )

    # Add the deck and cards to the database
    with SessionLocal() as session:
        session.add(deck)
        session.commit()

        # Now add the cards (which have a foreign key to the deck)
        session.add(card1)
        session.add(card2)
        session.commit()

    # Query the database to verify our data
    with SessionLocal() as session:
        decks = session.query(models.DeckModel).all()
        print(f"Found {len(decks)} decks")

        for deck in decks:
            print(f"Deck: {deck.name}")
            print("Cards:")
            for card in deck.cards:
                print(f"  - {card.front_text}")

if __name__ == "__main__":
    main()