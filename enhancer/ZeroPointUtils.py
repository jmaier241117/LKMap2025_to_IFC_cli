from itertools import islice


class ZeroPointScaler:
    def __init__(self, lkobject_type_dataset, clipsrc):
        self.dataset = lkobject_type_dataset
        self.scale_attributes = (clipsrc[0], clipsrc[1])

    def scale_point_objects(self) -> any:
        for key in islice(self.dataset.keys(), 1, None):
            coordinate_tuple = self.dataset[key]['geometry']
            self.dataset[key]['geometry'] = self._subtract_minimums_for_coords(coordinate_tuple)
        return self.dataset

    def scale_line_and_area_objects(self) -> any:

        for key in islice(self.dataset.keys(), 1, None):
            coordinates = self.dataset[key]['geometry']
            scaled_coordinates = ()
            for coordinate_tuple in coordinates:
                scaled_coordinates += (self._subtract_minimums_for_coords(coordinate_tuple),)
                self.dataset[key]['geometry'] = scaled_coordinates
        return self.dataset

    def _subtract_minimums_for_coords(self, coordinate_tuple) -> ():
        x_coord, y_coord = coordinate_tuple
        x_coord -= self.scale_attributes[0]
        y_coord -= self.scale_attributes[1]
        return round(x_coord, 4), round(y_coord, 4)
