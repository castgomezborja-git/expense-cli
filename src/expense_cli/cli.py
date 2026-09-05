from decimal import Decimal, InvalidOperation
from datetime import datetime
from typing import Optional

import typer
from sqlalchemy import select, desc

from expense_cli.db import get_session, init_db
from expense_cli.models import Category, Transaction

from rich.console import Console
from rich.table import Table

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

@app.command(name="list")
def list_transactions(
    category_name: Optional[str] = None,
    date_init: Optional[str] = None,
    date_end: Optional[str] = None,
):
    session = get_session()

    # 1. Construye la query para obtener los gastos, ordenados por fecha descendente
    statement = select(Transaction).order_by(desc(Transaction.date))

    # 2. Si category_name no es None, filtra por esa categoría
    if category_name:
        statement = statement.join(Transaction.category).where(Category.name == category_name)

    # 3. Si date_init y date_end no son None, filtra por ese rango de fechas
    if date_init and date_end:
        statement = statement.where(
            Transaction.date >= datetime.strptime(date_init, "%Y-%m-%d"),
            Transaction.date <= datetime.strptime(date_end, "%Y-%m-%d")
        )
    elif date_init:
        statement = statement.where(Transaction.date >= datetime.strptime(date_init, "%Y-%m-%d"))
    elif date_end:
        statement = statement.where(Transaction.date <= datetime.strptime(date_end, "%Y-%m-%d"))

    transactions = session.execute(statement).scalars().all()

    # 4. Imprime los gastos en una tabla usando rich.Table
    table = Table(title="Gastos")

    table.add_column("Cantidad", style="red")
    table.add_column("Fecha", style="cyan")
    table.add_column("Categoría", style="yellow")
    table.add_column("Descripción", style="green")

    for transaction in transactions:
        table.add_row(
            f"{transaction.amount:.2f}",
            transaction.date.strftime("%Y-%m-%d %H:%M"),
            transaction.category.name,
            transaction.description or "-",
        )

    console = Console()
    console.print(table)

if __name__ == "__main__":
    app()