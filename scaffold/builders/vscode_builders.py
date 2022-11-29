from structure.builders.builder import Builder
from structure.products import VSCodeProduct


class VSCodeBuilder(Builder):
    def reset(self) -> None:
        self.product = VSCodeProduct()

    def validate(self) -> None:
        pass

    def install_dependencies(self) -> None:
        pass

    def configure(self) -> None:
        pass

    def overwrite_shortcut(self) -> None:
        pass
