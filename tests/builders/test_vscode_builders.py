from scaffold.builders import VSCodeBuilder
from scaffold.products import VSCodeProduct


def test_vscode_builder(mocker):
    reset = mocker.spy(VSCodeBuilder, "reset")

    builder = VSCodeBuilder()
    assert reset.called
    assert isinstance(builder.product, VSCodeProduct)


def test_vscode_produce():
    builder = VSCodeBuilder()

    assert callable(builder.validate)
    assert callable(builder.install_dependencies)
    assert callable(builder.configure)
    assert callable(builder.overwrite_shortcut)
