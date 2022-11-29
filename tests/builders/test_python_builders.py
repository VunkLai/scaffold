# pylint: disable=unused-argument, redefined-outer-name

from typing import Generator
from unittest import mock

import pytest
from pytest_mock import MockerFixture

from scaffold.builders import PythonBuilder
from scaffold.products import PythonProduct

PROJECT_NAME = "test-python-builder"

IS_DEV = {"dev": True}


@pytest.fixture(scope="function")
def builder() -> Generator:
    builder = PythonBuilder()
    yield builder


def test_python_builder(mocker: MockerFixture):
    reset = mocker.spy(PythonBuilder, "reset")

    python_builder = PythonBuilder()

    assert reset.called
    assert isinstance(python_builder.product, PythonProduct)


def test_python_initialize(mocker: MockerFixture, builder):
    product_create = mocker.patch.object(PythonProduct, "create")

    builder.initialize(PROJECT_NAME)

    assert product_create.call_count == 1
    assert product_create.call_args == mock.call(PROJECT_NAME)


def test_python_install_dependencies(mocker: MockerFixture, builder: PythonBuilder):
    product_install = mocker.patch.object(PythonProduct, "install")

    builder.install_dependencies()

    assert product_install.call_count == 1
    assert product_install.call_args == mock.call("ipython", dev=True)


def test_python_install_formatter(mocker: MockerFixture, builder: PythonBuilder):
    product_install = mocker.patch.object(PythonProduct, "install")
    product_configure = mocker.patch.object(PythonProduct, "configure")

    builder.install_formatter()

    assert product_install.call_count == 2
    assert product_install.call_args_list == [
        mocker.call("black", dev=True),
        mocker.call("isort", dev=True),
    ]

    assert product_configure.call_count == 1
    assert "isort" in product_configure.call_args.args


def test_python_install_linter(mocker: MockerFixture, builder: PythonBuilder):
    product_install = mocker.patch.object(PythonProduct, "install")
    product_configure = mocker.patch.object(PythonProduct, "configure")

    builder.install_linter()

    assert product_install.call_count == 2
    assert product_install.call_args_list == [
        mocker.call("pylint", dev=True),
        mocker.call("mypy", dev=True),
    ]

    assert product_configure.call_count == 1
    assert "pylint" in product_configure.call_args.args
