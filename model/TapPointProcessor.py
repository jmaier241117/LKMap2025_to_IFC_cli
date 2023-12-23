from itertools import islice

import pyogrio


class TapPointProcessor:
    def __init__(self, dataset):
        self.dataset = dataset
        self.tap_point_geometries = None

    def execute_processor(self, object_type) -> any:
        if object_type == 'lkpunkt':
            self._get_point_tap_points()
        elif object_type == 'lklinie':
            self._get_line_tap_points()
        elif object_type == 'lkflaeche':
            self._get_area_tap_points()
        return self._combine_tap_points() if self.tap_point_geometries else None

    def _get_point_tap_points(self):
        point_tap_points_layer = pyogrio.read_dataframe(self.dataset, layer='abstichpunkt', where='lkpunktref not null')
        if not point_tap_points_layer.empty:
            self.tap_point_geometries = {}
            for index, row in point_tap_points_layer.iterrows():
                if row.lkpunktref not in self.tap_point_geometries:
                    self.tap_point_geometries[row.lkpunktref] = []
                self.tap_point_geometries[row.lkpunktref].append(row.geometry.__geo_interface__['coordinates'])

    def _get_line_tap_points(self):
        line_tap_points_layer = pyogrio.read_dataframe(self.dataset, layer='abstichpunkt', where='lklinieref not null')
        if not line_tap_points_layer.empty:
            self.tap_point_geometries = {}
            for index, row in line_tap_points_layer.iterrows():
                if row.lklinieref not in self.tap_point_geometries:
                    self.tap_point_geometries[row.lklinieref] = []
                self.tap_point_geometries[row.lklinieref].append(row.geometry.__geo_interface__['coordinates'])

    def _get_area_tap_points(self):
        area_tap_points_layer = pyogrio.read_dataframe(self.dataset, layer='abstichpunkt',
                                                       where='lkflaecheref not null')
        if not area_tap_points_layer.empty:
            self.tap_point_geometries = {}
            for index, row in area_tap_points_layer.iterrows():
                if row.lkflaecheref in self.tap_point_geometries:
                    self.tap_point_geometries[row.lkflaecheref] = []
                self.tap_point_geometries[row.lkflaecheref].append(row.geometry.__geo_interface__['coordinates'])

    def _combine_tap_points(self) -> any:
        tap_points_combined = {}
        for key in self.tap_point_geometries:
            tap_point_list = self.tap_point_geometries[key]
            tap_points_combined[key] = []
            for tap_point_to_match in tap_point_list:
                x_and_y_match = tap_point_to_match[0:2]
                tap_point_list = list(filter(lambda tp: tp != tap_point_to_match, tap_point_list))
                for tap_point in tap_point_list:
                    if x_and_y_match == tap_point[0:2]:
                        new_tap_point_tuple = (tap_point[0], tap_point[1], tap_point[2], tap_point_to_match[2])
                        tap_point_list = list(filter(lambda tp: tp != tap_point, tap_point_list))
                        tap_points_combined[key].append(sorted(new_tap_point_tuple, reverse=True))
                    if not tap_point_list:
                        break
        return tap_points_combined
