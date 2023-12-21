import subprocess

import pyogrio


def convert_ili_2_gpkg(datafile) -> any:
    code = subprocess.run(
        ['java', '-jar', 'ili2gpkg-5.1.0.jar', '--import', '--dbfile',
         'GeoPackage.gpkg', datafile])
    code.check_returncode()
    return code


def cleanUp_db(geopackage):
    dataset_layer = pyogrio.read_dataframe(geopackage, layer='T_ILI2DB_DATASET')
    if not dataset_layer.empty:
        for index, row in dataset_layer.iterrows():
            print(row.datasetName)
            subprocess.run(['java', '-jar', 'ili2gpkg-5.1.0.jar', '--delete', '--dataset', row.datasetName, '--dbfile',
                            'GeoPackage.gpkg'])
