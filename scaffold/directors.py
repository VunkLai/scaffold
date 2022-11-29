from typing import Union

from builders.python_builders import PythonBuilder
from builders.vscode_builders import VSCodeBuilder


class BuilderError(Exception):
    pass


class Director:
    _builder: Union[PythonBuilder, VSCodeBuilder]

    @property
    def builder(self) -> Union[PythonBuilder, VSCodeBuilder]:
        return self._builder

    @builder.setter
    def builder(self, builder: Union[PythonBuilder, VSCodeBuilder]) -> None:
        self._builder = builder


class Scaffold(Director):
    def create_python_project(self, project_name: str) -> None:
        if isinstance(self.builder, PythonBuilder):
            self.builder.initialize(project_name)
            self.builder.install_dependencies()
            self.builder.install_formatter()
            self.builder.install_linter()
            self.builder.install_tester()
            self.builder.product.commit("feat: initial project")
            self.builder.product.bump("0.1.0")

    def create_vscode_project(self) -> None:
        if isinstance(self.builder, VSCodeBuilder):
            self.builder.validate()
            self.builder.install_dependencies()
            self.builder.configure()
            self.builder.overwrite_shortcut()
