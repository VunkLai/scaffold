from scaffold.products.product import Product
from scaffold.products.tools import Commitizen, Git, Poetry, TomlConfiguration


class PythonProduct(Product):
    def __init__(self):
        self.git = Git()
        self.configuration = TomlConfiguration()
        self.poetry = Poetry()
        self.commitizen = Commitizen()

    def create(self, project_name: str):
        self.poetry.new(project_name)
        self.configuration.initialize(project_name)
        self.git.init(project_name, gitignore=True)
        self.commitizen.initialize(pre_commit=True)

    def install(self, package_name: str, dev: bool = False) -> None:
        self.poetry.add(package_name, dev)

    def configure(self, key: str, value: dict) -> None:
        self.configuration[key] = value

    def commit(self, message: str) -> None:
        self.configuration.save()
        self.git.add()
        self.git.commit(message)

    def bump(self, version: str) -> None:
        self.git.add()
        self.run("cz", "bump", "-ch", "--yes", version)

    def run(self, *options: str) -> None:
        self.poetry.run(*options)
