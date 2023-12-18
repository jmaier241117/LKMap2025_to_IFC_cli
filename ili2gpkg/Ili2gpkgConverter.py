import subprocess


class Ili2gpkgConverter:
    def __init__(self, datafile):
        self.datafile = datafile

    def convert_ili_2_gpkg(self):
        subprocess.call(
            ['java', '-jar', 'ili2gpkg-5.1.0.jar', '--import', '--doSchemaImport', '--dbfile', 'GeoPackage.gpkg',
             '--createBasketCol', '--strokeArcs', '--createTidCol', '--importTid', self.datafile])
