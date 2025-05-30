from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from ..models.crud import add_card_to_deck, remove_card_from_deck
from ..models.schema import CardDeckCreate
from ..models.database import get_db

router = APIRouter(
    prefix="/card-deck",
    tags=["card-deck"]
)

@router.post("/add", response_model=CardDeckCreate)
def add_card_to_deck_route(card_id: int, deck_id: int, db: Session = Depends(get_db)):
    result = add_card_to_deck(db, card_id, deck_id)
    if not result:
        raise HTTPException(status_code=404, detail="Card or Deck not found")
    return CardDeckCreate(card_id=card_id, deck_id=deck_id)

@router.delete("/remove", response_model=CardDeckCreate)
def remove_card_from_deck_route(card_id: int, deck_id: int, db: Session = Depends(get_db)):
    result = remove_card_from_deck(db, card_id, deck_id)
    if not result:
        raise HTTPException(status_code=404, detail="Card or Deck not found")
    return CardDeckCreate(card_id=card_id, deck_id=deck_id)