from sqlalchemy.orm import Session
from .card import CardModel
from .deck import DeckModel
from .card_deck import cards_decks

# Create a new card in the database
def create_card(db: Session, question: str, answer: str):
    db_card = CardModel(question=question, answer=answer)
    db.add(db_card)
    db.commit()
    db.refresh(db_card)
    return db_card

# Get a card by ID
def get_card(db: Session, card_id: int):
    return db.query(CardModel).filter(CardModel.id == card_id).first()

# Get all cards
def get_all_cards(db: Session, skip: int = 0, limit: int = 100):
    return db.query(CardModel).offset(skip).limit(limit).all()

# Update a card
def update_card(db: Session, card_id: int, question: str = None, answer: str = None):
    db_card = get_card(db, card_id)
    if not db_card:
        return None

    if question is not None:
        db_card.question = question
    if answer is not None:
        db_card.answer = answer

    db.commit()
    db.refresh(db_card)
    return db_card

# Delete a card
def delete_card(db: Session, card_id: int):
    db_card = get_card(db, card_id)
    if not db_card:
        return None

    db.delete(db_card)
    db.commit()
    return db_card

# Create a new deck in the database
def create_deck(db: Session, name: str):
    db_deck = DeckModel(name=name)
    db.add(db_deck)
    db.commit()
    db.refresh(db_deck)
    return db_deck

# Get a deck by ID
def get_deck(db: Session, deck_id: int):
    return db.query(DeckModel).filter(DeckModel.id == deck_id).first()

# Get all decks
def get_all_decks(db: Session, skip: int = 0, limit: int = 100):
    return db.query(DeckModel).offset(skip).limit(limit).all()

# Update a deck
def update_deck(db: Session, deck_id: int, name: str = None):
    db_deck = get_deck(db, deck_id)
    if not db_deck:
        return None

    if name is not None:
        db_deck.name = name

    db.commit()
    db.refresh(db_deck)
    return db_deck

# Delete a deck
def delete_deck(db: Session, deck_id: int):
    db_deck = get_deck(db, deck_id)
    if not db_deck:
        return None

    db.delete(db_deck)
    db.commit()
    return db_deck

# Add a card to a deck
def add_card_to_deck(db: Session, card_id: int, deck_id: int):
    db_card = get_card(db, card_id)
    db_deck = get_deck(db, deck_id)

    if not db_card or not db_deck:
        return False

    # Check if the relationship already exists
    existing_relationship = db.query(cards_decks).filter(
        cards_decks.c.card_id == card_id,
        cards_decks.c.deck_id == deck_id
    ).first()

    if existing_relationship:
        return True

    # Create the relationship
    stmt = cards_decks.insert().values(card_id=card_id, deck_id=deck_id)
    db.execute(stmt)
    db.commit()
    return True

# Remove a card from a deck
def remove_card_from_deck(db: Session, card_id: int, deck_id: int):
    db_card = get_card(db, card_id)
    db_deck = get_deck(db, deck_id)

    if not db_card or not db_deck:
        return False

    # Delete the relationship
    stmt = cards_decks.delete().where(
        cards_decks.c.card_id == card_id,
        cards_decks.c.deck_id == deck_id
    )
    db.execute(stmt)
    db.commit()
    return True