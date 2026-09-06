# expense-cli

CLI de gestión de gastos personales construida en Python. Primer proyecto de un
portfolio backend orientado a demostrar fundamentos sólidos del lenguaje,
persistencia con ORM, testing en todas las capas y buenas prácticas de
desarrollo (Git, empaquetado, Conventional Commits).

## Características

- **Registro de gastos** con cantidad, categoría, fecha y descripción opcional
- **Categorías extensibles**: se crean sobre la marcha, con confirmación interactiva
- **Listado filtrable** por categoría y rango de fechas, en tabla formateada
- **Reportes exportables** en consola, CSV o PDF, seleccionables en tiempo de ejecución

## Stack técnico

| Componente | Herramienta |
|---|---|
| Lenguaje | Python 3.12+ |
| Gestor de dependencias | [`uv`](https://github.com/astral-sh/uv) |
| CLI | [`Typer`](https://typer.tiangolo.com/) |
| ORM / Base de datos | `SQLAlchemy` 2.0 + SQLite |
| Tablas en consola | `rich` |
| Exportación PDF | `fpdf2` |
| Testing | `pytest` |

## Decisiones de diseño destacadas

- **`Decimal` en vez de `float`** para las cantidades monetarias, evitando errores
  de precisión de la coma flotante binaria.
- **Src-layout** (`src/expense_cli/`) para forzar que los tests validen el
  paquete tal como se instalaría realmente, no un import "de casualidad".
- **Relación muchos-a-uno** entre `Transaction` y `Category`: cada gasto
  pertenece a una única categoría.
- **Base de datos en memoria para tests** (`sqlite:///:memory:`), aislada por
  completo de los datos reales de desarrollo.

## Instalación

```bash
git clone https://github.com/castgomezborja-git/expense-cli.git
cd expense-cli
uv sync
```

## Uso

```bash
# Añadir un gasto
uv run python -m expense_cli.cli add 12.50 Comida --description "Cena rápida"

# Listar todos los gastos (más recientes primero)
uv run python -m expense_cli.cli list

# Filtrar por categoría o rango de fechas
uv run python -m expense_cli.cli list --category-name Comida
uv run python -m expense_cli.cli list --date-init 2026-09-01 --date-end 2026-09-30

# Generar un reporte (consola, CSV o PDF)
uv run python -m expense_cli.cli report --format csv
uv run python -m expense_cli.cli report --format pdf
uv run python -m expense_cli.cli report   # pregunta el formato interactivamente
```

## Tests

```bash
uv run pytest -v
```

Cobertura actual: modelos de dominio, comandos de la CLI (simulando entrada de
usuario con `CliRunner`) y funciones de exportación (CSV y PDF), todo sobre
bases de datos en memoria aisladas.

## Estado del proyecto

Primer proyecto de un portfolio de 5 proyectos progresivos en Python backend.
Pendiente de ampliación: comandos `delete` y `edit`.

## Estructura

```
expense-cli/
├── src/expense_cli/
│   ├── cli.py           # comandos Typer: add, list, report
│   ├── models.py        # entidades: Category, Transaction
│   ├── db.py            # engine y sesión de SQLAlchemy
│   └── reports.py       # filtrado y exportación (consola/CSV/PDF)
├── tests/
│   ├── conftest.py
│   ├── test_models.py
│   ├── test_cli.py
│   └── test_reports.py
└── pyproject.toml
```