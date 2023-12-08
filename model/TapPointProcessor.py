import sqlite3
from sqlite3 import Error

import geopandas


class TapPointProcessor:
    def __init__(self, dataset, type):
        self.dataset = dataset
        self.gpkg_connection = _create_connection(dataset)
        self.type = type

    def execute_processor(self) -> any:
        tap_points = self._get_tap_points()
        tap_point_geometries = self._get_tap_point_geometries()
        for key in tap_points:
            for tap_point_id in tap_point_geometries:
                if tap_point_id in tap_points[key]:
                    tap_points[key][tap_point_id]['geometry'] = tap_point_geometries[tap_point_id]['geometry']
        return self._combine_tap_points(tap_points)

    def _get_tap_points(self) -> any:
        with open("tappingPoints_" + self.type + ".sql", 'r') as sql_file:
            sql_script = sql_file.read()
        cur = self.gpkg_connection.cursor()
        cur.execute(sql_script)
        rows = cur.fetchall()
        tap_points = {}
        for row in rows:
            if row[1] in tap_points:
                tap_points[row[1]][row[0]] = {}
                tap_points[row[1]][row[0]]['type'] = row[2]
            else:
                tap_points[row[1]] = {row[0]: {}}
                tap_points[row[1]][row[0]]['type'] = row[2]
        return tap_points

    def _get_tap_point_geometries(self) -> any:
        tap_points = geopandas.read_file(self.dataset, layer='abstichpunkt')
        tap_point_geometries = {}
        for index, row in tap_points.iterrows():
            tap_point_geometries[row.T_Ili_Tid] = {}
            tap_point_geometries[row.T_Ili_Tid]['geometry'] = row.geometry.__geo_interface__['coordinates']
        return tap_point_geometries

    def _combine_tap_points(self, tap_points) -> any:
        tap_points_combined = {}
        for key in tap_points:
            tap_point_list = []
            for tap_point_id in tap_points[key]:
                tap_point_list.append(list(tap_points[key][tap_point_id]['geometry']))
            tap_points_combined[key] = []
            index = 0
            while index < len(tap_point_list):
                x_and_y_match = tap_point_list[index][0:2]
                index += 1
                for tap_point in tap_point_list[index:]:
                    if x_and_y_match == tap_point[0:2]:
                        index -= 1
                        new_tap_point = tap_point_list[index]
                        new_tap_point.append(tap_point[2])
                        tap_point_list.pop(index)
                        tap_point_list.remove(tap_point)
                        tap_points_combined[key].append(sorted(new_tap_point, reverse=True))
        return tap_points_combined


def _create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)
    return conn
