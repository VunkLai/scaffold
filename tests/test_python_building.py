# pylint: disable=unused-argument, redefined-outer-name

import shutil
from pathlib import Path

import pytest
import toml
from click.testing import CliRunner

from scaffold.main import scaffold

PROJECT_NAME = "fake-project-name"


@pytest.fixture()
def folder_for_test(scope="function"):
    shutil.rmtree(PROJECT_NAME, ignore_errors=True)
    yield PROJECT_NAME


def dependencies_check(poetry):
    assert PROJECT_NAME == poetry["name"]

    dependencies = poetry["dependencies"]
    assert "python" in dependencies

    dev_dependencies = poetry["group"]["dev"]["dependencies"]
    assert "ipython" in dev_dependencies
    assert "isort" in dev_dependencies
    assert "black" in dev_dependencies
    assert "pytest" in dev_dependencies
    assert "mypy" in dev_dependencies


def test_default_python_project(folder_for_test):
    runner = CliRunner()
    result = runner.invoke(scaffold, ["python", folder_for_test])
    assert result.exit_code == 0

    project = Path(PROJECT_NAME)
    assert project.exists()

    pyproject = project / "pyproject.toml"
    assert pyproject.exists()

    with pyproject.open("r") as fr:
        data = toml.load(fr)

        assert "poetry" in data["tool"]
        dependencies_check(data["tool"]["poetry"])

        assert "isort" in data["tool"]
        assert data["tool"]["isort"] == {"profile": "black"}

        assert "pylint" in data["tool"]
