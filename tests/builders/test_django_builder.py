# pylint: disable=unused-argument, redefined-outer-name
import shutil
from typing import Generator
from unittest.mock import ANY, MagicMock, call

import pytest
from pytest_mock import MockerFixture

from scaffold.builders import DjangoBuilder, PythonBuilder
from scaffold.products import PythonProduct

PROJECT_NAME = "test-django-builder"


@pytest.fixture(scope="function")
def builder() -> Generator:
    try:
        builder = DjangoBuilder()
        yield builder
    finally:
        shutil.rmtree(PROJECT_NAME, ignore_errors=True)  # just in case


@pytest.fixture(scope="function")
def product(mocker: MockerFixture) -> Generator:
    product = mocker.patch("scaffold.products.python_products.PythonProduct")
    product.attach_mock(mocker.patch.object(PythonProduct, "create"), "create")
    product.attach_mock(mocker.patch.object(PythonProduct, "install"), "install")
    product.attach_mock(mocker.patch.object(PythonProduct, "configure"), "configure")
    product.attach_mock(mocker.patch.object(PythonProduct, "run"), "run")
    product.attach_mock(mocker.patch.object(PythonProduct, "commit"), "commit")
    product.attach_mock(mocker.patch.object(PythonProduct, "bump"), "bump")
    yield product


def test_django_builder(mocker: MockerFixture):
    reset = mocker.spy(DjangoBuilder, "reset")

    django_builder = DjangoBuilder()

    assert reset.called
    assert isinstance(django_builder.product, PythonProduct)
    assert django_builder.DJANGO_PROJECT_NAME == "server"


def test_django_initialize(
    mocker: MockerFixture, product: MagicMock, builder: DjangoBuilder
):
    rmdir = mocker.patch("shutil.rmtree")
    builder.initialize(PROJECT_NAME)

    assert len(product.method_calls) == 1
    assert product.method_calls[0] == call.create(PROJECT_NAME)

    assert rmdir.call_count == 2
    clean_name = PROJECT_NAME.replace("-", "_")
    assert rmdir.mock_calls[0] == call(f"{PROJECT_NAME}/{clean_name}")
    assert rmdir.mock_calls[1] == call(f"{PROJECT_NAME}/tests")


def test_django_install_dependencies(
    mocker, product: MagicMock, builder: DjangoBuilder
):
    spy = mocker.spy(PythonBuilder, "install_dependencies")

    builder.install_dependencies()

    assert len(product.method_calls) == 5
    assert spy.call_count == 1
    assert product.method_calls[1] == call.install("django")
    assert product.method_calls[2] == call.install("djangorestframework")
    assert product.method_calls[3] == call.install("django-cors-headers")
    assert product.method_calls[4] == call.run(
        "django-admin", "startproject", builder.DJANGO_PROJECT_NAME
    )


def test_django_install_formatter(mocker, product: MagicMock, builder: DjangoBuilder):
    spy = mocker.spy(PythonBuilder, "install_formatter")

    builder.install_formatter()

    assert len(product.method_calls) == 4
    assert spy.call_count == 1
    assert product.method_calls[3] == call.configure("isort", ANY)


def test_django_install_linter(mocker, product: MagicMock, builder: DjangoBuilder):
    spy = mocker.spy(PythonBuilder, "install_linter")

    builder.install_linter()

    assert len(product.method_calls) == 4
    assert not spy.called
    assert product.method_calls[0] == call.install("pylint=2.14.5", dev=True)
    assert product.method_calls[1] == call.install("pylint-django", dev=True)
    assert product.method_calls[2] == call.configure("pylint", ANY)
    assert product.method_calls[3] == call.install("mypy", dev=True)


def test_django_install_tester(mocker, product: MagicMock, builder: DjangoBuilder):
    spy = mocker.spy(PythonBuilder, "install_tester")

    builder.install_tester()

    assert len(product.method_calls) == 3
    assert spy.call_count == 1
    assert product.method_calls[1] == call.install("pytest-django", dev=True)
    assert product.method_calls[2] == call.configure("pytest", ANY)


def test_django_release(mocker, product: MagicMock, builder: DjangoBuilder):
    spy = mocker.spy(PythonBuilder, "release")

    builder.release()

    assert len(product.method_calls) == 2
    assert spy.call_count == 1
