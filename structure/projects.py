from typing import Optional


class Builder:
    def __init__(self):
        self.product = Project()

    def initialize(self, project_name: str) -> None:
        self.product.init(project_name)

    def install_formatter(self) -> None:
        pass

    def install_linter(self) -> None:
        print("install linter")

    def install_tester(self) -> None:
        print("install tester")


class VSCodeBuilder(Builder):
    pass


class NormalProjectBuilder(Builder):
    def install_formatter(self) -> None:
        self.product.install("black", dev=True)
        self.product.install("isort", dev=True, config={"profile", "black"})


class DjangoProjectBuilder(Builder):
    def install_formatter(self) -> None:
        self.product.install("black", dev=True)
        self.product.install(
            "isort",
            dev=True,
            config={
                "profile": "black",
                "known_django": "django,rest_framework",
                "sections": "FUTURE,STDLIB,DJANGO,THIRDPARTY,FIRSTPARTY,LOCALFOLDER",
            },
        )


class Poetry:
    def new(self, project_name: str) -> None:
        print(f"poetry new {project_name}")

    def add(self, key, dev):
        if dev:
            print(f"poetry add --group dev {key}")
        else:
            print(f"poetry add {key}")


class Git:
    def init(self, project_name: str) -> None:
        print("git init", project_name)

    def commit(self, message: str):
        print("git add .")
        print(f"git commit -m {message}")


class Configuration:
    def add(self, key, value):
        print("pyproject.toml", key, value)


class Project:
    # product, python env, includes git, pyproject.toml,

    def __init__(self) -> None:
        self.poetry = Poetry()
        self.git = Git()
        self.configuration = Configuration()

    def init(self, name):
        self.poetry.new(name)
        self.git.init(name)

    def install(self, key, dev=False, config=None):
        self.poetry.add(key, dev)
        if config:
            self.configuration.add(key, config)

    def commit(self, message):
        self.git.commit(message)


class Scaffold:
    # director: scaffold
    _builder: Optional[Builder]

    def __init__(self) -> None:
        self._builder = None

    @property
    def builder(self):
        return self._builder

    @builder.setter
    def builder(self, builder: Builder) -> None:
        self._builder = builder

    def create_python_project(self, project_name) -> None:
        self.builder.initialize(project_name)
        self.builder.install_formatter()
        self.builder.product.commit("feat: initial project")

    def create_vscode(self) -> None:
        pass


if __name__ == "__main__":
    project = Scaffold()
    project.builder = NormalProjectBuilder()
    project.create_python_project(project_name="python")

    project = Scaffold()
    project.builder = DjangoProjectBuilder()
    project.create_python_project(project_name="django")

    project = Scaffold()
    project.builder = VSCodeBuilder()
    project.create_vscode()
