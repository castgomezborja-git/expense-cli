from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from expense_cli.models import Base

DATABASE_URL = "sqlite:///expenses.db"

engine = create_engine(DATABASE_URL)


def init_db() -> None:
    Base.metadata.create_all(engine)


def get_session() -> Session:
    return Session(engine)