"""
SQLite engine/session setup via SQLAlchemy. Tables are created at app startup
(see main.py) since there's no migration tool yet — fine for this stage,
will need a real migration tool (e.g. Alembic) once the schema needs to
change without losing data.
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from app.config import settings

# check_same_thread=False is needed because FastAPI's default dependency
# injection may use the connection from a different thread than the one
# that created it; SQLite otherwise refuses.
engine = create_engine(
    settings.database_url, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


class Base(DeclarativeBase):
    pass


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
