from decimal import Decimal
from datetime import datetime

from expense_cli.models import Category, Transaction


def test_create_category(session):
    comida = Category(name="Comida")
    session.add(comida)
    session.commit()

    assert comida.id is not None
    assert comida.name == "Comida"


def test_transaction_linked_to_category(session):
    comida = Category(name="Comida")
    session.add(comida)
    session.commit()

    gasto = Transaction(
        amount=Decimal("12.50"),
        date=datetime.now(),
        category=comida,
        description="Cena rápida",
    )
    session.add(gasto)
    session.commit()

    assert gasto.category_id == comida.id
    assert gasto.category.name == "Comida"