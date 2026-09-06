from expense_cli import reports

from datetime import datetime

def test_export_csv(tmp_path):
    filepath = tmp_path / "test_report.csv"

    # Creamos un par de categorías y transacciones de prueba
    category1 = reports.Category(name="Comida")
    category2 = reports.Category(name="Transporte")

    transaction1 = reports.Transaction(
        amount=10.50,
        date=datetime.strptime("2026-09-15 12:00:00", "%Y-%m-%d %H:%M:%S"),
        category=category1,
        description="Almuerzo",
    )
    transaction2 = reports.Transaction(
        amount=20.00,
        date=datetime.strptime("2026-09-16 14:00:00", "%Y-%m-%d %H:%M:%S"),
        category=category2,
        description="Taxi",
    )

    transactions = [transaction1, transaction2]

    # Exportamos a CSV
    reports.export_csv(transactions, str(filepath))

    # Verificamos que el archivo CSV se haya creado y tenga contenido
    assert filepath.exists()
    assert filepath.read_text(encoding="utf-8").startswith("Fecha,Cantidad,Categoría,Descripción")


def test_export_pdf(tmp_path):
    filepath = tmp_path / "test_report.pdf"

    category = reports.Category(name="Ocio")
    transaction = reports.Transaction(
        amount=15.00,
        date=datetime.strptime("2026-09-15 12:00:00", "%Y-%m-%d %H:%M:%S"),
        category=category,
        description="Cine",
    )

    reports.export_pdf([transaction], str(filepath))

    assert filepath.exists()
    assert filepath.stat().st_size > 0