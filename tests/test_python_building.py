# pylint: disable=unused-argument, redefined-outer-name

from pathlib import Path

import pytest
import toml  # type: ignore
from click.testing import CliRunner
from git import Git

from scaffold.main import scaffold

PROJECT_NAME = "fake-project-name"


@pytest.fixture()
def folder_for_test(scope="function"):
    try:
        yield PROJECT_NAME
    finally:
        shutil.rmtree(PROJECT_NAME, ignore_errors=True)


def test_default_python_project(folder_for_test) -> None:
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
        poetry = data["tool"]["poetry"]
        assert PROJECT_NAME == poetry["name"]

        dependencies = poetry["dependencies"]
        assert "python" in dependencies

        dev_dependencies = poetry["group"]["dev"]["dependencies"]
        assert "ipython" in dev_dependencies
        assert "isort" in dev_dependencies
        assert "black" in dev_dependencies
        assert "pytest" in dev_dependencies
        assert "mypy" in dev_dependencies

        assert "isort" in data["tool"]
        assert data["tool"]["isort"] == {"profile": "black"}

        assert "pylint" in data["tool"]

    git_folder = project / ".git"
    assert git_folder.exists()

    git = Git(PROJECT_NAME)
    assert "* main" in git.branch()
    assert "feat: initial commit" in git.log()


def test_django_project(folder_for_test) -> None:
    runner = CliRunner()
    result = runner.invoke(scaffold, ["python", "--django", folder_for_test])
    assert result.exit_code == 0

    project = Path(PROJECT_NAME)
    assert project.exists()

    pyproject = project / "pyproject.toml"
    assert pyproject.exists()

    with pyproject.open("r") as fr:
        data = toml.load(fr)

        assert "poetry" in data["tool"]
        poetry = data["tool"]["poetry"]
        assert PROJECT_NAME == poetry["name"]

        dependencies = poetry["dependencies"]
        assert "python" in dependencies
        assert "Django" in dependencies
        assert "djangorestframework" in dependencies
        assert "django-cors-headers" in dependencies

        dev_dependencies = poetry["group"]["dev"]["dependencies"]
        assert "ipython" in dev_dependencies
        assert "isort" in dev_dependencies
        assert "black" in dev_dependencies
        assert "pytest" in dev_dependencies
        assert "mypy" in dev_dependencies
        assert "pytest-django" in dev_dependencies
        assert "pylint-django" in dev_dependencies
        assert "pylint" in dev_dependencies
        assert dev_dependencies["pylint"] == "2.14.5"

        assert "isort" in data["tool"]
        assert data["tool"]["isort"]["profile"] == "black"
        assert "known_django" in data["tool"]["isort"]
        assert "sections" in data["tool"]["isort"]

        assert "pylint" in data["tool"]
        assert "main" in data["tool"]["pylint"]

        assert "pytest" in data["tool"]
        assert "ini_options" in data["tool"]["pytest"]
        assert "DJANGO_SETTINGS_MODULE" in data["tool"]["pytest"]["ini_options"]
        assert "python_files" in data["tool"]["pytest"]["ini_options"]

    git_folder = project / ".git"
    assert git_folder.exists()

    git = Git(PROJECT_NAME)
    assert "* main" in git.branch()
    assert "feat: initial commit" in git.log()

    django_folder = project / "server"
    assert django_folder.exists()

    manage = django_folder / "manage.py"
    assert manage.exists()
