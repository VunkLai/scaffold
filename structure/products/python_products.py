from structure.products.product import Product


class Git:
    def init(self) -> None:
        pass

    def commit(self, message: str) -> None:
        pass


class Configuration:
    def create_or_update(self, key: str, value: dict) -> None:
        pass


class Poetry:
    def new(self, project_name: str) -> None:
        pass

    def add(self, key, dev: bool = False) -> None:
        pass


class PythonProduct(Product):
    def __init__(self):
        self.git = Git()
        self.configuration = Configuration()
        self.poetry = Poetry()

    def create(self, project_name: str):
        self.git.init()
        self.poetry.new(project_name)

    def install(self, package_name: str, dev: bool = False) -> None:
        self.poetry.add(package_name, dev)

    def configure(self, key: str, value: dict) -> None:
        self.configuration.create_or_update(key, value)

    def commit(self, message: str) -> None:
        self.git.commit(message)
