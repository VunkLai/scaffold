# pylint: disable=unused-argument, redefined-outer-name
import shutil
from typing import Generator
from unittest.mock import ANY, MagicMock, call

import pytest
from pytest_mock import MockerFixture

from scaffold.builders import PythonBuilder
from scaffold.products import PythonProduct

PROJECT_NAME = "test-python-builder"


@pytest.fixture(scope="function")
def builder() -> Generator:
    try:
        builder = PythonBuilder()
        yield builder
    finally:
        shutil.rmtree(PROJECT_NAME, ignore_errors=True)  # just in case


@pytest.fixture(scope="function")
def product(mocker: MockerFixture) -> Generator:
    product = mocker.patch("scaffold.products.python_products.PythonProduct")
    product.attach_mock(mocker.patch.object(PythonProduct, "create"), "create")
    product.attach_mock(mocker.patch.object(PythonProduct, "install"), "install")
    product.attach_mock(mocker.patch.object(PythonProduct, "configure"), "configure")
    yield product


def test_python_builder(mocker: MockerFixture):
    reset = mocker.spy(PythonBuilder, "reset")

    python_builder = PythonBuilder()

    assert reset.called
    assert isinstance(python_builder.product, PythonProduct)


def test_python_initialize(product: MagicMock, builder: PythonBuilder):
    builder.initialize(PROJECT_NAME)

    assert len(product.method_calls) == 1
    assert product.method_calls[0] == call.create(PROJECT_NAME)


def test_python_install_dependencies(product: MagicMock, builder: PythonBuilder):
    builder.install_dependencies()

    assert len(product.method_calls) == 1
    assert product.method_calls[0] == call.install("ipython", dev=True)


def test_python_install_formatter(product: MagicMock, builder: PythonBuilder):
    builder.install_formatter()

    assert len(product.method_calls) == 3
    assert product.method_calls[0] == call.install("black", dev=True)
    assert product.method_calls[1] == call.install("isort", dev=True)
    assert product.method_calls[2] == call.configure("isort", ANY)


def test_python_install_linter(product: MagicMock, builder: PythonBuilder):
    builder.install_linter()

    assert len(product.method_calls) == 3
    assert product.method_calls[0] == call.install("pylint", dev=True)
    assert product.method_calls[1] == call.configure("pylint", ANY)
    assert product.method_calls[2] == call.install("mypy", dev=True)


def test_python_install_tester(product: MagicMock, builder: PythonBuilder):
    builder.install_tester()

    assert len(product.method_calls) == 1
    assert product.method_calls[0] == call.install("pytest", dev=True)
