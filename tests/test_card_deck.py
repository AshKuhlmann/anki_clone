import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from src.your_srs_clone.main import app
from src.your_srs_clone.models.database import get_db, engine
from src.your_srs_clone.models.crud import create_card, create_deck, add_card_to_deck
from src.your_srs_clone.models.card import CardModel
from src.your_srs_clone.models.deck import DeckModel

# Dependency override for testing
def override_get_db():
    db = Session(bind=engine)
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)

@pytest.fixture(scope="module")
def setup_database():
    # Create the tables
    CardModel.metadata.create_all(bind=engine)
    DeckModel.metadata.create_all(bind=engine)

    yield

    # Drop the tables
    CardModel.metadata.drop_all(bind=engine)
    DeckModel.metadata.drop_all(bind=engine)

def test_add_card_to_deck(setup_database):
    # Create a card and deck
    with Session(bind=engine) as session:
        card = create_card(session, "Question 1", "Answer 1")
        deck = create_deck(session, "Deck 1")

    # Add the card to the deck
    with Session(bind=engine) as session:
        result = add_card_to_deck(session, card.id, deck.id)
        assert result is True

    # Verify the relationship was created
    with Session(bind=engine) as session:
        card_in_deck = session.query(CardModel, DeckModel).join(
            "decks", CardModel.id == deck.id
        ).filter(CardModel.id == card.id).first()

        assert card_in_deck is not None
        assert card_in_deck[0].id == card.id
        assert card_in_deck[1].id == deck.id

def test_remove_card_from_deck(setup_database):
    # Create a card and deck
    with Session(bind=engine) as session:
        card = create_card(session, "Question 2", "Answer 2")
        deck = create_deck(session, "Deck 2")

    # Add the card to the deck
    with Session(bind=engine) as session:
        add_card_to_deck(session, card.id, deck.id)

    # Remove the card from the deck
    with Session(bind=engine) as session:
        stmt = "DELETE FROM cards_decks WHERE card_id = :card_id AND deck_id = :deck_id"
        session.execute(stmt, {"card_id": card.id, "deck_id": deck.id})
        session.commit()

    # Verify the relationship was removed
    with Session(bind=engine) as session:
        card_in_deck = session.query(CardModel, DeckModel).join(
            "decks", CardModel.id == deck.id
        ).filter(CardModel.id == card.id).first()

        assert card_in_deck is None