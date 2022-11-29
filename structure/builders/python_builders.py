from structure.builders.builder import Builder
from structure.products import PythonProduct


class PythonBuilder(Builder):
    def reset(self) -> None:
        self.product = PythonProduct()

    def initialize(self, project_name: str) -> None:
        self.product.create(project_name)

    def install_dependencies(self) -> None:
        pass

    def install_formatter(self) -> None:
        self.product.install("black", dev=True)
        self.product.install("isort", dev=True)
        self.product.configure("isort", {"profile": "black"})

    def install_linter(self) -> None:
        self.product.install("pylint", "pytest")

    def install_tester(self) -> None:
        self.product.install("pytest")


class DjangoBuilder(PythonBuilder):
    def install_dependencies(self) -> None:
        pass

    def install_formatter(self) -> None:
        super().install_formatter()
        self.product.configure(
            "isort", {"profile": "black", "known_django": "django,rest_framework"}
        )

    def install_linter(self) -> None:
        self.product.install("pylint=2.14.5", "pylint-django")

    def install_tester(self) -> None:
        super().install_tester()
        self.product.install("pytest-django")
