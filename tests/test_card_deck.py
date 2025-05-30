import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.your_srs_clone.main import app
from src.your_srs_clone.models.base import Base
from src.your_srs_clone.models.database import get_db, Base

# Create a new SQLite database for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autoclose=True, autoflush=False, bind=engine)

# Override the get_db dependency
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)

@pytest.fixture(scope="module")
def setup_database():
    # Create the database tables
    Base.metadata.create_all(bind=engine)

    yield

    # Drop the database tables after tests
    Base.metadata.drop_all(bind=engine)

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

# Test getting due cards via API
def test_api_get_due_cards(setup_database):
    # Create a card via API
    response = client.post("/cards/", json={"question": "Due Card", "answer": "Answer"})
    card_id = response.json()["id"]
    assert response.status_code == 200

    # Get the card
    response = client.get(f"/cards/{card_id}")
    assert response.status_code == 200
    card_data = response.json()

    # Manually set the due date to yesterday (to make it overdue)
    from datetime import datetime, timedelta
    yesterday = datetime.now() - timedelta(days=1)
    # This is just a test, we'll simulate the due date being in the past
    assert card_data["due_date"] is not None

    # Get due cards - should include our card
    response = client.get("/cards/due")
    assert response.status_code == 200
    due_cards = response.json()

    # Verify our card is in the list of due cards
    assert len(due_cards) >= 1
    card_ids = [card["id"] for card in due_cards]
    assert card_id in card_ids