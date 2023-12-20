import sqlite3
import subprocess
from sqlite3 import Error

gpkg_connection = None


def create_connection(db_file):
    global gpkg_connection
    try:
        gpkg_connection = sqlite3.connect(db_file)
    except Error as e:
        print(e)
    return gpkg_connection


def convert_ili_2_gpkg(datafile) -> any:
    code = subprocess.run(
        ['java', '-jar', 'ili2gpkg-5.1.0.jar', '--import', '--dbfile',
         'GeoPackage.gpkg', datafile])
    code.check_returncode()
    return code


def cleanUp_db():
    sql_script = ("select datasetName from T_ILI2DB_DATASET")
    cur = gpkg_connection.cursor()
    cur.execute(sql_script)
    rows = cur.fetchall()
    for row in rows:
        subprocess.run(['java', '-jar', 'ili2gpkg-5.1.0.jar', '--delete', '--dataset', row[0], '--dbfile',
                        'GeoPackage.gpkg'])
        print(row[0])

