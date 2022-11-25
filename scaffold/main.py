import click

from .projects import python


@click.group()
def scaffold():
    pass


scaffold.add_command(python)
