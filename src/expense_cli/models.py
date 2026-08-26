from typing import Optional
from decimal import Decimal
from datetime import datetime

from sqlalchemy import ForeignKey, Numeric
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

class Base(DeclarativeBase):
    pass

class Category(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)

    def __repr__(self) -> str:
        return f"Category(id={self.id!r}, name={self.name!r})"

class Transaction(Base):
    __tablename__ = "transactions"

    id: Mapped[int] = mapped_column(primary_key=True)
    amount: Mapped[Decimal] = mapped_column(Numeric(10, 2))
    date: Mapped[datetime]
    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id"))
    category: Mapped[Category] = relationship()
    description: Mapped[Optional[str]]

    def __repr__(self) -> str:
        return f"Transaction(id={self.id!r}, amount={self.amount!r}, date={self.date!r})"