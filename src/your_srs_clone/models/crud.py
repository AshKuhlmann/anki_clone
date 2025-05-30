from sqlalchemy.orm import Session
from .card import CardModel

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