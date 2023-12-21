import pyogrio


class TapPointProcessor:
    def __init__(self, dataset):
        self.dataset = dataset
        self.tap_point_geometries = None

    def execute_processor(self, object_type) -> any:
        self.tap_point_geometries = {}
        if object_type == 'lkpunkt':
            self._get_point_tap_points()
        elif object_type == 'lklinie':
            self._get_line_tap_points()
        elif object_type == 'lkflaeche':
            self._get_area_tap_points()
        return self._combine_tap_points(self.tap_point_geometries) if self.tap_point_geometries else None

    def _get_point_tap_points(self):
        point_tap_points_layer = pyogrio.read_dataframe(self.dataset, layer='abstichpunkt', where='lkpunktref not null')
        if not point_tap_points_layer.empty:
            for index, row in point_tap_points_layer.iterrows():
                if row.lkpunktref not in self.tap_point_geometries:
                    self.tap_point_geometries[row.lkpunktref] = []
                self.tap_point_geometries[row.lkpunktref].append(row.geometry.__geo_interface__['coordinates'])

    def _get_line_tap_points(self):
        line_tap_points_layer = pyogrio.read_dataframe(self.dataset, layer='abstichpunkt', where='lklinieref not null')
        if not line_tap_points_layer.empty:
            for index, row in line_tap_points_layer.iterrows():
                if row.lklinieref not in self.tap_point_geometries:
                    self.tap_point_geometries[row.lklinieref] = []
                self.tap_point_geometries[row.lklinieref].append(row.geometry.__geo_interface__['coordinates'])

    def _get_area_tap_points(self):
        area_tap_points_layer = pyogrio.read_dataframe(self.dataset, layer='abstichpunkt',
                                                       where='lkflaecheref not null')
        if not area_tap_points_layer.empty:
            for index, row in area_tap_points_layer.iterrows():
                if row.lkflaecheref in self.tap_point_geometries:
                    self.tap_point_geometries[row.lkflaecheref] = []
                self.tap_point_geometries[row.lkflaecheref].append(row.geometry.__geo_interface__['coordinates'])

    def _combine_tap_points(self, tap_points) -> any:
        tap_points_combined = {}
        for key in tap_points:
            tap_point_list = tap_points[key]
            tap_points_combined[key] = []
            index = 0
            while index < len(tap_point_list):
                x_and_y_match = tap_point_list[index][0:2]
                index += 1
                for tap_point in tap_point_list[index:]:
                    if x_and_y_match == tap_point[0:2]:
                        index -= 1
                        new_tap_point_tuple = (tap_point[0], tap_point[1], tap_point[2], tap_point_list[index][2])
                        tap_point_list.pop(index)
                        tap_point_list.remove(tap_point)
                        tap_points_combined[key].append(sorted(new_tap_point_tuple, reverse=True))
        return tap_points_combined
