# pylint: disable=redefined-outer-name
import pytest

from scaffold.builders import VSCodeBuilder
from scaffold.products import VSCodeProduct


@pytest.fixture(scope="function")
def builder():
    yield VSCodeBuilder()


def test_vscode_builder(mocker):
    reset = mocker.spy(VSCodeBuilder, "reset")

    builder = VSCodeBuilder()
    assert reset.called
    assert isinstance(builder.product, VSCodeProduct)


def test_vscode_produce(builder):

    assert callable(builder.validate)
    assert callable(builder.install_dependencies)
    assert callable(builder.configure)
    assert callable(builder.overwrite_shortcut)


def test_vscode_validate(mocker, builder):
    spy = mocker.spy(builder, "validate")

    builder.validate()

    assert spy.called


def test_vscode_install_dependencies(mocker, builder):
    spy = mocker.spy(builder, "install_dependencies")

    builder.install_dependencies()

    assert spy.called


def test_vscode_configure(mocker, builder):
    spy = mocker.spy(builder, "configure")

    builder.configure()

    assert spy.called


def test_vscode_overwrite_shortcut(mocker, builder):
    spy = mocker.spy(builder, "overwrite_shortcut")

    builder.overwrite_shortcut()

    assert spy.called
