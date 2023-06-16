from typing import Optional
from typing import List
from typing_extensions import Annotated
import typer

from lkmap_to_ifc_cli import __app_name__, __version__, config, ERRORS

app = typer.Typer()


def _version_callback(value: bool) -> None:
    if value:
        typer.echo(f"{__app_name__} v{__version__}")
        raise typer.Exit()


@app.callback()
def main(
        version: Optional[bool] = typer.Option(
            None,
            "--version",
            "-v",
            help="Show the application's version and exit.",
            callback=_version_callback,
            is_eager=True,
        )
) -> None:
    return


@app.command()
def convert(
        gpkg_path: Annotated[str, typer.Argument(help="The path to the Geopackge you would like to use")],
        clipsrc: Annotated[List[int], typer.Argument(help="The boundary for your IFC file")],
        ifc_file_name: Annotated[
            str, typer.Argument(help="The name to be used for the generated IFC file")] = "lkmap_to_ifc",

) -> None:
    conversion_init_error = config.init_conversion_config(gpkg_path, clipsrc)
    if conversion_init_error:
        typer.secho(f'An error occured during parsing of the required arguments',
                    fg=typer.colors.RED,
                    )
        raise typer.Exit(1)

    typer.Exit()
