from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, DeckModel, CardModel

# Database URL (using SQLite for simplicity)
DATABASE_URL = "sqlite:///./sparkdeck.db"

# Create engine and connect to database
engine = create_engine(DATABASE_URL, echo=True)

# Create all tables in the database
def init_db():
    Base.metadata.create_all(bind=engine)

# Create a new session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

if __name__ == "__main__":
    # Initialize the database (create tables)
    init_db()
    print("Database initialized with tables: decks and cards")