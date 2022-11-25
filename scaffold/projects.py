import click

from .tools import Poetry


class Dependencies:
    default_tools = ["ipython", "isort", "black", "pytest", "mypy"]


@click.command()
@click.argument("project_name", nargs=1, type=str, default=".")
def python(project_name: str) -> None:
    project = Poetry(project_name)
    project.create()
    project.add(Dependencies.default_tools, dev=True)
