from fastapi import FastAPI
from .api.cards import router as cards_router
from .api.decks import router as decks_router
from .api.card_deck import router as card_deck_router
from .models.database import engine, init_db

app = FastAPI()

# Initialize the database tables
init_db()

# Include the routers
app.include_router(cards_router)
app.include_router(decks_router)
app.include_router(card_deck_router)

@app.get("/")
def read_root():
    return {"message": "Welcome to Your SRS Clone API"}