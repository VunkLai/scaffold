# pylint: disable=unused-argument, redefined-outer-name
import shutil
from pathlib import Path

import pytest
from click.testing import CliRunner

from scaffold.main import scaffold

PROJECT_NAME = "fake-project-name"


@pytest.fixture()
def cli(scope="function"):
    runner = CliRunner()
    try:
        yield runner
    finally:
        shutil.rmtree(PROJECT_NAME, ignore_errors=True)


def test_cli_entrypoint(cli):
    result = cli.invoke(scaffold)
    assert result.exit_code == 0
    assert result.output.startswith("Usage: scaffold")


def test_python_project_creation(cli):
    result = cli.invoke(scaffold, ["python", PROJECT_NAME])
    assert result.exit_code == 0

    project = Path(PROJECT_NAME)
    assert project.exists()


def test_django_project_creation(cli):
    result = cli.invoke(scaffold, ["python", "--django", PROJECT_NAME])
    assert result.exit_code == 0

    project = Path(PROJECT_NAME)
    assert project.exists()
