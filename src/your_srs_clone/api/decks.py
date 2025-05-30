from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from ..models.schema import DeckCreate, DeckResponse
from ..models.database import get_db
from ..models.crud import create_deck, get_all_decks, get_deck, update_deck, delete_deck

router = APIRouter(
    prefix="/decks",
    tags=["decks"]
)

@router.post("/", response_model=DeckResponse)
def create_deck_route(deck: DeckCreate, db: Session = Depends(get_db)):
    db_deck = create_deck(db, deck.name)
    return db_deck

@router.get("/", response_model=List[DeckResponse])
def read_decks(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    decks = get_all_decks(db, skip=skip, limit=limit)
    return decks

@router.get("/{deck_id}", response_model=DeckResponse)
def read_deck(deck_id: int, db: Session = Depends(get_db)):
    db_deck = get_deck(db, deck_id)
    if db_deck is None:
        raise HTTPException(status_code=404, detail="Deck not found")
    return db_deck

@router.put("/{deck_id}", response_model=DeckResponse)
def update_deck_route(deck_id: int, deck_update: DeckCreate, db: Session = Depends(get_db)):
    db_deck = update_deck(db, deck_id, deck_update.name)
    if db_deck is None:
        raise HTTPException(status_code=404, detail="Deck not found")
    return db_deck

@router.delete("/{deck_id}", response_model=DeckResponse)
def delete_deck_route(deck_id: int, db: Session = Depends(get_db)):
    db_deck = delete_deck(db, deck_id)
    if db_deck is None:
        raise HTTPException(status_code=404, detail="Deck not found")
    return db_deck