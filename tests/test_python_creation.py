# pylint: disable=unused-argument, redefined-outer-name

import shutil
from pathlib import Path

import pytest
import tomli
from click.testing import CliRunner
from git import Git

from scaffold.main import scaffold

PROJECT_NAME = "fake-python-project"


def setup_module():
    runner = CliRunner()
    runner.invoke(scaffold, ["python", PROJECT_NAME])


def teardown_module():
    shutil.rmtree(PROJECT_NAME, ignore_errors=True)


@pytest.fixture(scope="function")
def folder():
    yield Path(PROJECT_NAME)


@pytest.fixture(scope="function")
def config():
    configuration = Path(PROJECT_NAME, "pyproject.toml")
    with open(configuration, "rb") as fr:
        data = tomli.load(fr)
        yield data["tool"]


def test_python_configuration(folder) -> None:
    configuration = folder / "pyproject.toml"
    assert configuration.exists(), "pyproject.toml not found"


def test_poetry_config(config) -> None:
    assert "poetry" in config, "invalid pyproject.toml, poetry not found"
    assert config["poetry"]["name"] == PROJECT_NAME, "invalid project name"


def test_dependencies(config) -> None:
    assert "dependencies" in config["poetry"], "dependencies not found"

    dependencies = config["poetry"]["dependencies"]
    assert "python" in dependencies, "python does not install"


def test_dev_dependencies(config) -> None:
    assert (
        "dependencies" in config["poetry"]["group"]["dev"]
    ), "dev-dependencies not found"

    dev_dependencies = config["poetry"]["group"]["dev"]["dependencies"]
    assert "ipython" in dev_dependencies, "ipython does not install"
    assert "isort" in dev_dependencies, "isort does not install"
    assert "black" in dev_dependencies, "black does not install"
    assert "pytest" in dev_dependencies, "pytest does not install"
    assert "mypy" in dev_dependencies, "mypy does not install"


def test_isort_config(config) -> None:
    assert "isort" in config, "isort not found"

    isort = config["isort"]
    assert isort["profile"] == "black", "isort profile should be black"


def test_pylint_config(config) -> None:
    assert "pylint" in config, "pylint not found"

    pylint = config["pylint"]
    assert "messages_control" in pylint, "messages_control not found"

    messages_control = pylint["messages_control"]
    assert messages_control["max-line-length"] == 120, "max-line-length should be 120"
    assert (
        "missing-module-docstring" in messages_control["disable"]
    ), "missing-module-docstring should be disabled"
    assert (
        "missing-class-docstring" in messages_control["disable"]
    ), "missing-class-docstring should be disabled"
    assert (
        "missing-function-docstring" in messages_control["disable"]
    ), "missing-function-docstring not found"
    assert "fixme" in messages_control["disable"], "fixme should be disabled"
    assert (
        "too-few-public-methods" in messages_control["disable"]
    ), "too-few-public-methods should be disabled"


def test_commitizen_config(config, folder) -> None:
    assert "commitizen" in config, "commitizen does not install"

    commitizen = config["commitizen"]
    assert (
        commitizen["name"] == "cz_conventional_commits"
    ), "commitizen commit-rule should be `cz_conventional_commits`"
    assert (
        commitizen["version"] == "0.0.1"
    ), "commitizen initial-version should be 0.0.1"
    assert (
        commitizen["tag_format"] == "$version"
    ), "commitizen tag-format should be `$version`"


def test_python_version_control(folder) -> None:
    gitignore = folder / ".gitignore"
    assert gitignore.exists(), ".gitignore not found"

    git_folder = folder / ".git"
    assert git_folder.exists(), ".git not found"
    assert git_folder.is_dir(), ".git should be folder"

    pre_commit = git_folder / "hooks" / "pre-commit"
    assert pre_commit.exists(), "pre-commit does not install"

    git = Git(PROJECT_NAME)
    assert "* main" in git.branch(), "default branch should be main"
    assert (
        "feat: initial commit" in git.log()
    ), "scaffold should create the initial commit"
