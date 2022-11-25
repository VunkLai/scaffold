import click
from git import Repo

from .tools import Poetry, PyProject


class Dependencies:
    default_tools = ["ipython", "isort", "black", "pytest", "mypy"]


@click.command()
@click.argument("project_name", nargs=1, type=str, default=".")
def python(project_name: str) -> None:
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
