import shutil

from scaffold.builders.builder import Builder
from scaffold.products import PythonProduct


class PythonBuilder(Builder):
    def reset(self) -> None:
        self.product = PythonProduct()

    def initialize(self, project_name: str) -> None:
        self.product.create(project_name)

    def install_dependencies(self) -> None:
        self.product.install("ipython", dev=True)

    def install_formatter(self) -> None:
        self.product.install("black", dev=True)
        self.product.install("isort", dev=True)
        self.product.configure("isort", {"profile": "black"})

    def install_linter(self) -> None:
        self.product.install("pylint", dev=True)
        self.product.configure(
            "pylint",
            {
                "messages_control": {
                    "max-line-length": 120,
                    "disable": [
                        "missing-module-docstring",
                        "missing-class-docstring",
                        "missing-function-docstring",
                        "fixme",
                        "too-few-public-methods",
                    ],
                },
                "basic": {"good-names": ["_"]},
            },
        )
        self.product.install("mypy", dev=True)

    def install_tester(self) -> None:
        self.product.install("pytest", dev=True)

    def release(self, message: str = "", version: str = "") -> None:
        self.product.commit(message or "feat: initial project")
        self.product.bump(version or "0.1.0")


class DjangoBuilder(PythonBuilder):
    DJANGO_PROJECT_NAME: str = "server"

    def initialize(self, project_name: str) -> None:
        self.product.create(project_name)
        # django does not use default layout
        clean_name = project_name.replace("-", "_")
        shutil.rmtree(f"{project_name}/{clean_name}")
        shutil.rmtree(f"{project_name}/tests")

    def install_dependencies(self) -> None:
        super().install_dependencies()
        self.product.install("django")
        self.product.install("djangorestframework")
        self.product.install("django-cors-headers")
        # create django project
        self.product.run("django-admin", "startproject", self.DJANGO_PROJECT_NAME)

    def install_formatter(self) -> None:
        super().install_formatter()
        self.product.configure(
            "isort",
            {
                "profile": "black",
                "known_django": "django,rest_framework",
                "sections": "FUTURE,STDLIB,DJANGO,THIRDPARTY,FIRSTPARTY,LOCALFOLDER",
            },
        )

    def install_linter(self) -> None:
        # fixme: pylint 2.15 causes django.core.exceptions.Improperlyconfigured to be raised
        # https://github.com/PyCQA/pylint-django/issues/370
        self.product.install("pylint=2.14.5", dev=True)
        self.product.install("pylint-django", dev=True)
        self.product.configure(
            "pylint",
            {
                "main": {
                    "ignore": "db.sqlite3",
                    "ignore-patterns": ["migrations/"],
                    "load-plugins": ["pylint_django"],
                    "django-settings-module": f"{self.DJANGO_PROJECT_NAME}.settings",
                },
                "messages_control": {
                    "max-line-length": 120,
                    "disable": [
                        "missing-module-docstring",
                        "missing-class-docstring",
                        "missing-function-docstring",
                        "fixme",
                    ],
                },
                "basic": {
                    "good-names": ["_"],
                },
            },
        )
        self.product.install("mypy", dev=True)

    def install_tester(self) -> None:
        super().install_tester()
        self.product.install("pytest-django", dev=True)
        self.product.configure(
            "pytest",
            {
                "ini_options": {
                    "DJANGO_SETTINGS_MODULE": f"{self.DJANGO_PROJECT_NAME}.settings",
                    "python_files": ["tests.py", "test_*.py"],
                }
            },
        )

    def release(self, message: str = "", version: str = "") -> None:
        super().release()
