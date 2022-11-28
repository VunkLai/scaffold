import shutil

import click
from git import Repo

from .tools import Poetry, PyProject


class Dependencies:
    default_tools = ["ipython", "isort", "black", "pytest", "mypy"]

    django = ["django", "djangorestframework", "django-cors-headers"]
    django_tools = ["pylint=2.14.5", "pylint-django", "pytest-django"]


@click.command()
@click.argument("project_name", nargs=1, type=str, default=".")
@click.option("-d", "--django", is_flag=True)
def python(project_name: str, django: bool) -> None:
    project = Poetry(project_name)
    project.new()
    project.add(Dependencies.default_tools, dev=True)

    pyproject = PyProject(project_name)
    pyproject.add("isort", {"profile": "black"})
    pyproject.add(
        "pylint",
        {
            "messages_control": {
                "max-line-length": 120,
                "disable": [
                    "missing-module-docstring",
                    "missing-class-docstring",
                    "missing-function-docstring",
                    "fixme",
                ],
            },
            "basic": {"good-names": ["_"]},
        },
    )
    pyproject.save()

    repo = Repo.init(project_name)
    repo.git.add(all=True)
    repo.git.commit("-m", "feat: initial commit")
    repo.git.branch("-m", "main")

    if django:
        project.add(Dependencies.django)
        # fixme: pylint 2.15 causes django.core.exceptions.Improperlyconfigured to be raised
        # https://github.com/PyCQA/pylint-django/issues/370
        project.remove("pylint")
        project.add(Dependencies.django_tools, dev=True)

        # clean default project
        clean_name = project_name.replace("-", "_")
        shutil.rmtree(f"{project_name}/{clean_name}")
        shutil.rmtree(f"{project_name}/tests")

        # create django project
        django_project_name = "server"
        project.invoke(f"django-admin startproject {django_project_name}")

        pyproject = PyProject(project_name)
        pyproject.add(
            "isort",
            {
                "profile": "black",
                "known_django": "django,rest_framework",
                "sections": "FUTURE,STDLIB,DJANGO,THIRDPARTY,FIRSTPARTY,LOCALFOLDER",
            },
        )
        pyproject.add(
            "pylint",
            {
                "main": {
                    "ignore": "db.sqlite3",
                    "ignore-patterns": ["migrations/"],
                    "load-plugins": ["pylint_django"],
                    "django-settings-module": f"{django_project_name}.settings",
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
        pyproject.add(
            "pytest",
            {
                "ini_options": {
                    "DJANGO_SETTINGS_MODULE": f"{django_project_name}.settings",
                    "python_files": ["tests.py", "test_*.py"],
                }
            },
        )
        pyproject.save()
