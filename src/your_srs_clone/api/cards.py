from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import date

from ..models.crud import create_card, get_all_cards, get_card, update_card, delete_card
from ..models.schema import CardCreate, CardResponse, CardUpdate
from ..models.database import get_db
from ..models.models import Card

router = APIRouter(
    prefix="/cards",
    tags=["cards"]
)

@router.post("/", response_model=CardResponse)
def create_card_route(card: CardCreate, db: Session = Depends(get_db)):
    db_card = create_card(db, card.question, card.answer)
    return db_card

@router.get("/", response_model=List[CardResponse])
def read_cards(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    cards = get_all_cards(db, skip=skip, limit=limit)
    return cards

@router.get("/{card_id}", response_model=CardResponse)
def read_card(card_id: int, db: Session = Depends(get_db)):
    db_card = get_card(db, card_id)
    if db_card is None:
        raise HTTPException(status_code=404, detail="Card not found")
    return db_card

@router.put("/{card_id}", response_model=CardResponse)
def update_card_route(card_id: int, card_update: CardUpdate, db: Session = Depends(get_db)):
    db_card = update_card(db, card_id, card_update.question, card_update.answer)
    if db_card is None:
        raise HTTPException(status_code=404, detail="Card not found")
    return db_card

@router.delete("/{card_id}", response_model=CardResponse)
def delete_card_route(card_id: int, db: Session = Depends(get_db)):
    db_card = delete_card(db, card_id)
    if db_card is None:
        raise HTTPException(status_code=404, detail="Card not found")
    return db_card

@router.post("/{card_id}/review", response_model=CardResponse)
def review_card(card_id: int, response: str, db: Session = Depends(get_db)):
    """Review a card and update its SM-2 parameters.

    Args:
        card_id: The ID of the card to review.
        response: The user's response ('correct', 'incorrect', 'hard', or 'good').
        db: The database session.

    Returns:
        The updated card.
    """
    db_card = get_card(db, card_id)
    if db_card is None:
        raise HTTPException(status_code=404, detail="Card not found")

    # Update the card's SM-2 parameters based on the response
    db_card.update_after_review(response)
    db.commit()
    db.refresh(db_card)

    return db_card

@router.get("/due", response_model=List[CardResponse])
def get_due_cards(db: Session = Depends(get_db)):
    """Get all cards that are due for review.

    Returns:
        A list of cards that are due for review.
    """
    today = date.today()
    cards = db.query(Card).filter(
        (Card.due_date <= today) |
        ((Card.review_count == 0) & (Card.due_date <= today))
    ).all()

    return cards