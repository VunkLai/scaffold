import shutil

import click
import requests
import yaml
from git import Repo

from .tools import Poetry, PyProject


class Dependencies:
    default_tools = [
        "ipython",
        "isort",
        "black",
        "pytest",
        "mypy",
        "Commitizen",
        "pre-commit",
    ]

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
                    "too-few-public-methods",
                ],
            },
            "basic": {"good-names": ["_"]},
        },
    )
    pyproject.save()

    url = "https://raw.githubusercontent.com/github/gitignore/main/Python.gitignore"
    response = requests.get(url, timeout=10)
    with open(f"{project_name}/.gitignore", "w", encoding="utf-8") as fw:
        fw.write("# Github gitignore template\n")
        fw.write(f"# {url}\n")
        fw.write(response.text)

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
        project.run(["django-admin", "startproject", django_project_name])

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

        repo.git.add(all=True)
        repo.git.commit("-m", "feat: initial django project")

    # project.run(["cz", "init"])
    pyproject = PyProject(project_name)
    pyproject.add(
        "commitizen",
        {
            "name": "cz_conventional_commits",
            "version": "0.0.1",
            "tag_format": "$version",
        },
    )
    pyproject.save()

    commitize_hook = {
        "hooks": [{"id": "commitizen"}],
        "repo": "https://github.com/commitizen-tools/commitizen",
        "rev": "v2.37.0",
    }
    pre_commit_config = {"repos": [commitize_hook]}
    with open(f"{project_name}/.pre-commit-config.yaml", "w", encoding="utf-8") as fw:
        yaml.dump(pre_commit_config, fw)

    repo.git.add(all=True)
    repo.git.commit("-m", "build: import commitizen and pre-commit")

    project.run(["pre-commit", "install"])
    project.run(["cz", "bump", "-ch", "--yes", "0.1.0"])
