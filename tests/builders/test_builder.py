from scaffold.builders import VSCodeBuilder
from scaffold.builders.builder import Builder
from scaffold.products import VSCodeProduct
from scaffold.products.product import Product


def test_builder(mocker):
    reset = mocker.spy(Builder, "reset")

    builder = Builder()
    assert reset.called
    assert isinstance(builder.product, Product)


def test_vscode_builder(mocker):
    reset = mocker.spy(VSCodeBuilder, "reset")

    builder = VSCodeBuilder()
    assert reset.called
    assert isinstance(builder.product, VSCodeProduct)

    assert callable(builder.validate)
    assert callable(builder.install_dependencies)
    assert callable(builder.configure)
    assert callable(builder.overwrite_shortcut)
