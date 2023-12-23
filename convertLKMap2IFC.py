import os

import click

from ifc.IfcCreationController import IfcCreationController
from ifc.IfcUtils import write_ifc_file
from model.DataProcessingChain import DataProcessingChain
from setup import POLYGON, POINT, XTF_ERROR, IFC_ERROR, CONFIG_ERROR, SUCCESS


@click.command()
@click.argument('importfile', type=click.Path())
@click.option('--nullpoint', required=True, type=POINT,
              help='The Reference Null Point used for creating the elements, example: \'POINT(2691039.8 1236160.3 420.0)\'')
@click.option('--exportpath', default=None, type=click.Path(),
              help='The path to where you would like your IFC file to be generated')
@click.option('--clipsrc', default=None, type=POLYGON,
              help='The range for which elements should be included, example: \'POLYGON((69.0 41.0, 69.0 41.4, 69.4 41.4, 69.4 41.0, 69.0 41.0))\'')
def convert(importfile, nullpoint, exportpath, clipsrc):
    """
     IMPORTFILE is the path to the INTERLIS transferfile (.xtf) you would like to use!

     NULLPOINT is the reference null point for all elements, format LV95: x , y, z

     EXPORTFILE is , format: <name>.ifc
    """
    print(nullpoint)
    if check_conversion_config(importfile, exportpath) == 0:
        run_conversion({'xtf': importfile, 'reference_null_point': nullpoint},
                       {'clipsrc': clipsrc, 'ifc_file_path': exportpath})
    click.secho(f"The conversion has successfully completed, you can find your IFC file here \"{exportpath}\"",
                fg='green')


def check_conversion_config(importfile, exportpath) -> int:
    try:
        if not os.path.isfile(importfile):
            click.secho(f"ERROR: The file {importfile} cannot be found", fg='red')
            return XTF_ERROR
        if not exportpath:
            click.secho(f"WARNING: No export path was given, the file will be created in the current working directory",
                        fg='magenta')
            click.confirm('Do you want to continue?', abort=True)
        if exportpath and os.path.isfile(exportpath):
            click.secho(f"ERROR: An ifc file with the given name already exists", fg='red')
            return IFC_ERROR
    except OSError:
        return CONFIG_ERROR
    return SUCCESS


def run_conversion(cli_arguments, cli_options):
    data_processing_chain = DataProcessingChain(cli_arguments, cli_options['clipsrc'])
    processed_dictionaries = data_processing_chain.execute_processing_chain()
    print(processed_dictionaries)
    ifc_creation_controller = IfcCreationController(cli_arguments['reference_null_point'])
    ifc_creation_controller.ifc_base_initialization()
    ifc_creation_controller.build_chamber_ifc_elements(processed_dictionaries['lkpunkt'])
    ifc_creation_controller.build_pipe_ifc_elements(processed_dictionaries['lklinie'])
    ifc_creation_controller.build_special_structure_ifc_elements(processed_dictionaries['lkflaeche'])
    write_ifc_file(ifc_creation_controller.ifc_file, cli_options['ifc_file_path'])


if __name__ == '__main__':
    convert()
