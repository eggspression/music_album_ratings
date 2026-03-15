from app.config import get_required_env, load_env_file
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

load_env_file()

DATABASE_URL = get_required_env("DATABASE_URL")

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
