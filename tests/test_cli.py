from expense_cli import cli

def test_add_command_cancelled(cli_runner):
    result = cli_runner.invoke(
        cli.app, ["add", "10.50", "Factura", "--description", "Luz"], input="n\n"
    )
    assert result.exit_code == 0
    assert "Cancelado" in result.stdout


def test_add_command_confirmed(cli_runner):
    result = cli_runner.invoke(
        cli.app, ["add", "23.50", "Factura", "--description", "Luz"], input="y\n"
    )
    assert result.exit_code == 0
    assert "Gasto agregado exitosamente." in result.stdout


def test_list_transaction_command(cli_runner):
    # First, add a transaction
    cli_runner.invoke(
        cli.app, ["add", "15.00", "Transporte", "--description", "Taxi"], input="y\n"
    )

    # Now, list transactions
    result = cli_runner.invoke(cli.app, ["list"])

    assert result.exit_code == 0
    assert "Transporte" in result.stdout

def test_list_transaction_by_category_command(cli_runner):
    # First, add a transaction
    cli_runner.invoke(
        cli.app, ["add", "15.00", "Transporte", "--description", "Taxi"], input="y\n"
    )

    # Now, list transactions
    result = cli_runner.invoke(cli.app, ["list", "--category-name", "Transporte"])

    assert result.exit_code == 0
    assert "Transporte" in result.stdout

def test_list_transaction_by_dates_command(cli_runner):
    # First, add a transaction
    cli_runner.invoke(
        cli.app, ["add", "15.00", "Transporte", "--description", "Taxi"], input="y\n"
    )

    # Now, list transactions
    result = cli_runner.invoke(cli.app, ["list", "--date-init", "2026-09-01", "--date-end", "2026-09-30"])

    assert result.exit_code == 0
    assert "Transporte" in result.stdout