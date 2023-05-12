import typer as typer

from controller import __app_name__
from controller import cli


def main(name: str):
    typer.echo("Hello World")
    typer.echo(f"Hello {name}!")
    cli.app(prog_name=__app_name__)


if __name__ == "__main__":
    typer.run(main)
