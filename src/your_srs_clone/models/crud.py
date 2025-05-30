from sqlalchemy.orm import Session
from .models import Card, Deck, Note, ReviewLog

# CRUD operations for Card model
def get_card(db: Session, card_id: int):
    return db.query(Card).filter(Card.id == card_id).first()

def get_all_cards(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Card).offset(skip).limit(limit).all()

def create_card(db: Session, question: str, answer: str):
    db_card = Card(question=question, answer=answer)
    db.add(db_card)
    db.commit()
    db.refresh(db_card)
    return db_card

def update_card(db: Session, card_id: int, question: str = None, answer: str = None):
    db_card = db.query(Card).filter(Card.id == card_id).first()
    if db_card is None:
        return None

    if question is not None:
        db_card.question = question
    if answer is not None:
        db_card.answer = answer

    db.commit()
    db.refresh(db_card)
    return db_card

def delete_card(db: Session, card_id: int):
    db_card = db.query(Card).filter(Card.id == card_id).first()
    if db_card is None:
        return None

    db.delete(db_card)
    db.commit()
    return db_card