import os
from typing import Optional, Tuple
import typer
from typing_extensions import Annotated
from controller import Controller

__app_name__ = "lkmap_to_ifc_cli"
__version__ = "0.0.1"

(
    SUCCESS,
    CONFIG_ERROR,
    GPKG_ERROR,
    IFC_ERROR,

) = range(4)

ERRORS = {
    CONFIG_ERROR: "config error",
    GPKG_ERROR: "geopackage error",
    IFC_ERROR: "IFC error"
}

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
def convert_gpkg_to_ifc(
        gpkg_path: Annotated[str, typer.Argument(help="The path to the Geopackge you would like to use")],
        clipsrc: Annotated[
            Tuple[float, float, float, float], typer.Argument(
                help="The range for objects, format: [xmin, ymin, xmax, ymax]")],
        ifc_file_path: Annotated[
            str, typer.Argument(help="The name to be used for the generated IFC file, format: <name>.ifc")],

) -> None:
    conversion_init_error = _init_conversion_config(gpkg_path, ifc_file_path)
    if conversion_init_error:
        typer.secho(
            f'An error occured during parsing of the required arguments, please check that your arguments are valid',
            fg=typer.colors.RED,
        )
        raise typer.Exit(1)
    controller = Controller({'gpkg': gpkg_path, 'clipsrc': clipsrc}, {'ifc_file_path': ifc_file_path})
    controller.run_conversion()
    typer.secho(f"The conversion has successfully completed, you can find your IFC file here \"{ifc_file_path}\"",
                fg=typer.colors.GREEN)
    typer.Exit()


def _init_conversion_config(gpkg_path: str, ifc_file: str) -> int:
    try:
        if not os.path.isfile(gpkg_path):
            typer.secho(f"ERROR: The GeoPackge {gpkg_path} cannot be found", fg=typer.colors.RED)
            return GPKG_ERROR
        if os.path.isfile(ifc_file):
            typer.secho(f"ERROR: An ifc file with the given name already exists", fg=typer.colors.RED)
            return IFC_ERROR
    except OSError:
        return CONFIG_ERROR
    return SUCCESS


if __name__ == "__main__":
    app()
