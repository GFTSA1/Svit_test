from sqlalchemy.orm import sessionmaker, declarative_base
from sqlmodel import create_engine

SQLALCHEMY_DATABASE_URL = "sqlite:///test_svit.db"


engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
