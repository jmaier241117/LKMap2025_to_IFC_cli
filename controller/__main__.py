import typer as typer

from lkmap_to_ifc_cli import cli, __app_name__


def main(name: str):
    typer.echo("Hello World")
    typer.echo(f"Hello {name}!")
    cli.app(prog_name=__app_name__)


if __name__ == "__main__":
    typer.run(main)
