from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Database URL format: dialect+driver://username:password@host:port/database
DATABASE_URL = "sqlite:///./test.db"

# Create the SQLAlchemy engine
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# Create a configured "Session" class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create the database tables
def init_db():
    from .base import Base  # Import here to avoid circular imports
    Base.metadata.create_all(bind=engine)

# Dependency that gets the DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()