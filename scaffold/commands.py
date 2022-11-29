import click

from scaffold.builders import DjangoBuilder, PythonBuilder, VSCodeBuilder
from scaffold.directors import Scaffold


@click.command()
@click.argument("project_name", nargs=1, type=str, default=".")
@click.option("--django", is_flag=True, default=False)
def python(project_name: str, django: bool) -> None:
    scaffold = Scaffold()
    scaffold.builder = PythonBuilder()
    if django:
        scaffold.builder = DjangoBuilder()
    scaffold.create_python_project(project_name)


@click.command()
def vscode() -> None:
    scaffold = Scaffold()
    scaffold.builder = VSCodeBuilder()
    scaffold.create_vscode_project()


@click.group()
def entrypoint():
    click.echo("hello world")


entrypoint.add_command(python)
entrypoint.add_command(vscode)
