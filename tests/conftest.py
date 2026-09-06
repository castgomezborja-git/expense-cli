import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from expense_cli.models import Base

from expense_cli import cli
from typer.testing import CliRunner

@pytest.fixture
def session():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)

    with Session(engine) as db_session:
        yield db_session


@pytest.fixture
def cli_runner(monkeypatch):
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    test_session = Session(engine)

    monkeypatch.setattr(cli, "get_session", lambda: test_session)

    return CliRunner()