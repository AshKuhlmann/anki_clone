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

# API Tests
def test_api_add_card_to_deck(setup_database):
    # Create a card and deck via API
    response = client.post("/cards/", json={"question": "API Question", "answer": "API Answer"})
    card_id = response.json()["id"]
    assert response.status_code == 200

    response = client.post("/decks/", json={"name": "API Deck"})
    deck_id = response.json()["id"]
    assert response.status_code == 200

    # Add the card to the deck
    response = client.post(f"/card-deck/add?card_id={card_id}&deck_id={deck_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["card_id"] == card_id
    assert data["deck_id"] == deck_id

def test_api_remove_card_from_deck(setup_database):
    # Create a card and deck via API
    response = client.post("/cards/", json={"question": "API Question 2", "answer": "API Answer 2"})
    card_id = response.json()["id"]
    assert response.status_code == 200

    response = client.post("/decks/", json={"name": "API Deck 2"})
    deck_id = response.json()["id"]
    assert response.status_code == 200

    # Add the card to the deck
    response = client.post(f"/card-deck/add?card_id={card_id}&deck_id={deck_id}")
    assert response.status_code == 200

    # Remove the card from the deck
    response = client.delete(f"/card-deck/remove?card_id={card_id}&deck_id={deck_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["card_id"] == card_id
    assert data["deck_id"] == deck_id

# Test reviewing a card via API
def test_api_review_card(setup_database):
    # Create a card via API
    response = client.post("/cards/", json={"question": "API Question", "answer": "API Answer"})
    card_id = response.json()["id"]
    assert response.status_code == 200

    # Review the card as correct
    response = client.post(f"/cards/{card_id}/review?response=correct")
    assert response.status_code == 200
    data = response.json()

    # Verify the card's SM-2 parameters were updated
    assert data["review_count"] == 1
    assert data["ease_factor"] > 2.5  # Ease factor should increase for correct answer
    assert data["interval"] > 0      # Interval should be set

    # Review the card as incorrect
    response = client.post(f"/cards/{card_id}/review?response=incorrect")
    assert response.status_code == 200
    data = response.json()

    # Verify the card's SM-2 parameters were updated
    assert data["review_count"] == 2
    assert data["ease_factor"] < 2.5  # Ease factor should decrease for incorrect answer
    assert data["interval"] == 0      # Interval should be reset

    # Review the card as hard
    response = client.post(f"/cards/{card_id}/review?response=hard")
    assert response.status_code == 200
    data = response.json()

    # Verify the card's SM-2 parameters were updated
    assert data["review_count"] == 3
    assert data["ease_factor"] < 2.5  # Ease factor should decrease for hard question
    assert data["interval"] > 0       # Interval should be increased

    # Review the card as good
    response = client.post(f"/cards/{card_id}/review?response=good")
    assert response.status_code == 200
    data = response.json()

    # Verify the card's SM-2 parameters were updated
    assert data["review_count"] == 4
    assert data["ease_factor"] > 2.5  # Ease factor should increase for good question
    assert data["interval"] > 0       # Interval should be increased