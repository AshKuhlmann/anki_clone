from fastapi import FastAPI
from .api.cards import router as cards_router

app = FastAPI()

# Include the cards router
app.include_router(cards_router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Anki Clone API"}