import os

import click

from ifc.IfcCreationController import IfcCreationController
from ifc.IfcUtils import write_ifc_file
from model.DataProcessingChain import DataProcessingChain
from setup import POLYGON, POINT, XTF_ERROR, CONFIG_ERROR, SUCCESS


@click.argument('import_file', type=click.Path())
@click.argument('null_point',  type=POINT)
@click.option('--export_path', default=None, type=click.Path(),
              help='The path to where you would like your IFC file to be generated')
@click.option('--clip_src', default=None, type=POLYGON,
              help='The range for which elements should be included, example: \'POLYGON((69.0 41.0, 69.0 41.4, 69.4 41.4, 69.4 41.0, 69.0 41.0))\'')
@click.option('--show_height_uncertainty', default=True,
              help='Flag if height uncertainties should be shown, default = True')
@click.option('--show_position_uncertainty', default=True,
              help='Flag if position uncertainties should be shown, default = True')
@click.command()
def convertLKMap2IFC(import_file, null_point, export_path, clip_src, show_height_uncertainty,
                     show_position_uncertainty):
    """
     IMPORTFILE is the path to the INTERLIS transferfile (.xtf) you would like to use!

     NULLPOINT is the reference null point for all elements, format LV95: x , y, z

     EXPORTFILE is , format: <name>.ifc
    """
    try:
        if not os.path.isfile(import_file):
            raise click.ClickException(f'The file {import_file} cannot be found')
        if not export_path:
            click.secho(f"WARNING: No export path was given," +
                        " the file will be created in the current working directorys export folder!",
                        fg='magenta')
            click.confirm('Do you want to continue?', abort=True)
            export_path = 'export/' + (import_file.split(".")[0]) + '.ifc'
        if os.path.isfile(export_path):
            click.secho(f'WARNING: An ifc file with the given name already exists at {export_path}', fg='magenta')
            click.confirm('Do you want to overwrite it?', abort=True)
    except OSError:
        return CONFIG_ERROR
    run_conversion({'xtf': import_file, 'reference_null_point': null_point},
                   {'clipsrc': clip_src, 'ifc_file_path': export_path,
                    'show_height_uncertainty': show_height_uncertainty,
                    'show_position_uncertainty': show_position_uncertainty})
    click.secho(f"The conversion has successfully completed, you can find your IFC file here \"{export_path}\"",
                fg='green')


def run_conversion(cli_arguments, cli_options):
    data_processing_chain = DataProcessingChain(cli_arguments, cli_options['clipsrc'])
    processed_dictionaries = data_processing_chain.execute_processing_chain()
    ifc_creation_controller = IfcCreationController(cli_arguments['reference_null_point'],
                                                    cli_options['show_height_uncertainty'],
                                                    cli_options['show_position_uncertainty'])
    ifc_creation_controller.ifc_base_initialization()
    ifc_creation_controller.build_chamber_ifc_elements(processed_dictionaries['lkpunkt'])
    ifc_creation_controller.build_pipe_ifc_elements(processed_dictionaries['lklinie'])
    ifc_creation_controller.build_special_structure_ifc_elements(processed_dictionaries['lkflaeche'])
    write_ifc_file(ifc_creation_controller.ifc_file, cli_options['ifc_file_path'])


if __name__ == '__main__':
    convertLKMap2IFC()
