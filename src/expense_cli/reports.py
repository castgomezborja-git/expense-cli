# src/expense_cli/reports.py

from datetime import datetime
from typing import Optional

from sqlalchemy import select, desc
from sqlalchemy.orm import Session

from expense_cli.models import Category, Transaction

from rich.console import Console
from rich.table import Table

import csv

def get_filtered_transactions(
    session: Session,
    category_name: Optional[str] = None,
    date_init: Optional[str] = None,
    date_end: Optional[str] = None,
) -> list[Transaction]:
    statement = select(Transaction).order_by(desc(Transaction.date))

    if category_name:
        statement = statement.join(Transaction.category).where(Category.name == category_name)

    if date_init and date_end:
        statement = statement.where(
            Transaction.date >= datetime.strptime(date_init, "%Y-%m-%d"),
            Transaction.date <= datetime.strptime(date_end, "%Y-%m-%d"),
        )
    elif date_init:
        statement = statement.where(Transaction.date >= datetime.strptime(date_init, "%Y-%m-%d"))
    elif date_end:
        statement = statement.where(Transaction.date <= datetime.strptime(date_end, "%Y-%m-%d"))

    return list(session.execute(statement).scalars().all())

def render_console_report(transactions: list[Transaction]) -> None:
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

def export_csv(transactions: list[Transaction], filepath: str) -> None:
    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Fecha", "Cantidad", "Categoría", "Descripción"])

        for transaction in transactions:
            writer.writerow([
                transaction.date.strftime("%Y-%m-%d %H:%M"),
                f"{transaction.amount:.2f}",
                transaction.category.name,
                transaction.description or "",
            ])