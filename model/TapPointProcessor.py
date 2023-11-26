import sqlite3
from sqlite3 import Error

import geopandas


class TapPointProcessor:
    def __init__(self, dataset):
        self.dataset = dataset
        self.gpkg_connection = _create_connection(dataset)

    def execute_processor(self) -> any:
        tap_points = self._get_tap_points()
        tap_point_geometries = self._get_tap_point_geometries()
        for key in tap_points:
            tap_points[key]['geometry'] = tap_point_geometries[key]['geometry']
        return tap_points

    def _get_tap_points(self) -> any:
        with open('tapPoint.sql', 'r') as sql_file:
            sql_script = sql_file.read()
        cur = self.gpkg_connection.cursor()
        cur.execute(sql_script)
        rows = cur.fetchall()
        tap_points = {}
        for row in rows:
            tap_points[row[0]] = {'id': row[1], 'type': row[2]}
        return tap_points

    def _get_tap_point_geometries(self) -> any:
        tap_points = geopandas.read_file(self.dataset, layer='abstichpunkt')
        tap_point_geometries = {}
        for index, row in tap_points.iterrows():
            tap_point_geometries[row.T_Ili_Tid] = {}
            tap_point_geometries[row.T_Ili_Tid]['geometry'] = row.geometry.__geo_interface__['coordinates']
        return tap_point_geometries
def _create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)
    return conn
