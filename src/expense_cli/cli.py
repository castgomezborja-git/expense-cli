from decimal import Decimal, InvalidOperation
from datetime import datetime
from typing import Optional

import typer
from sqlalchemy import select

from expense_cli.db import get_session, init_db
from expense_cli.models import Category, Transaction

app = typer.Typer()


@app.callback()
def main():
    init_db()


@app.command()
def add(
    amount: str,
    category_name: str,
    description: Optional[str] = None,
):

    # Validación del amount: intenta convertir a Decimal, si falla, imprime error y return
    try:
        amount_decimal = Decimal(amount)
    except InvalidOperation:
        typer.echo(f"Error: '{amount}' no es una cantidad válida.")
        raise typer.Exit(code=1)
            
    session = get_session()

    # 1. Busca si la categoría ya existe
    statement = select(Category).where(Category.name == category_name)
    category = session.execute(statement).scalar_one_or_none()

    # 2. Si no existe, pregunta con typer.confirm() si se quiere crear
        #- si dice que no, cancela con typer.echo("Cancelado") y return
        #- si dice que sí, crea la Category, session.add(...), session.commit()
    if not category:
        if not typer.confirm(f"La categoría '{category_name}' no existe. ¿Quieres crearla?"):
            typer.echo("Cancelado")
            return
        category = Category(name=category_name)
        session.add(category)
        session.commit()

    # 3. Crea la Transaction con la categoría (nueva o existente), session.add(...), session.commit()

    gasto = Transaction(
            amount=amount_decimal,
            date=datetime.now(),
            category=category,
            description=description,
        )
    session.add(gasto)
    session.commit()
    
    # 4. Imprime confirmación con typer.echo(...)
    typer.echo("Gasto agregado exitosamente.")

if __name__ == "__main__":
    app()