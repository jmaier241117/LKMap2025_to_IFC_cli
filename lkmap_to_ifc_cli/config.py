import configparser
import os
from pathlib import Path
from typing import List

import typer

from lkmap_to_ifc_cli import (
    CONFIG_ERROR, SUCCESS
)


def init_conversion_config(gpkg_path: str, clipsrc: List[int]) -> int:
    try:
        os.path.isfile(gpkg_path)
    except OSError:
        return CONFIG_ERROR
    if clipsrc:
        typer.secho(
            f'Creating database failed wit"',
            fg=typer.colors.RED,
        )
        return CONFIG_ERROR
    return SUCCESS
