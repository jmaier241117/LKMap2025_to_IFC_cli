from statistics import mean


class CoordinateAdapter:
    def __init__(self, reference_null_point):
        self.scale_attributes = (reference_null_point[0], reference_null_point[1], reference_null_point[2])
        self.lkobject_type = None
        self.coordinates_3d = None
        self.area_thickness = None

    def execute_processor(self, lkobject_type, elements, tapping_points) -> any:
        self.lkobject_type = lkobject_type
        for key in elements.keys():
            self.coordinates_3d = []
            if key in tapping_points:
                if lkobject_type == 'lkpunkt':
                    self._execute_points_adapter(elements[key]['geometry'], tapping_points[key][0])
                elif lkobject_type == 'lklinie':
                    self._execute_adapter(elements[key]['geometry'], tapping_points[key])
                elif lkobject_type == 'lkflaeche':
                    self._execute_adapter(elements[key]['geometry'][0], tapping_points[key])
            else:
                if lkobject_type == 'lklinie':
                    self._execute_default_3d_coordinate_adapter(elements[key]['geometry'])
                elif lkobject_type == 'lkpunkt':
                    self._execute_default_3d_coordinate_adapter(elements[key]['geometry'])
                elif lkobject_type == 'lkflaeche':
                    self._execute_default_3d_coordinate_adapter(elements[key]['geometry'][0])
            elements[key]['geometry'] = self._scale_objects(self.coordinates_3d)
            if lkobject_type == 'lkflaeche':
                elements[key]['thickness'] = self.area_thickness
        return elements

    def _execute_default_3d_coordinate_adapter(self, element_geometry):
        coordinate_2d = list(element_geometry)
        if self.lkobject_type == 'lkpunkt':
            self.coordinates_3d = [[coordinate_2d[0], coordinate_2d[1], self.scale_attributes[2]],
                                   [coordinate_2d[0], coordinate_2d[1], (self.scale_attributes[2] - 0.6)]]
        else:
            for coordinate in coordinate_2d:
                self.coordinates_3d.append([coordinate[0], coordinate[1], self.scale_attributes[2]])
            self.area_thickness = 1.0

    def _execute_points_adapter(self, element_geometry, element_tapping_point):
        coordinate_2d = list(element_geometry)
        tap_point = element_tapping_point
        if tap_point[0:2] == coordinate_2d:
            self.coordinates_3d.append([tap_point[0], tap_point[1], tap_point[2]])
            self.coordinates_3d.append([tap_point[0], tap_point[1], tap_point[3]])
        else:
            self._execute_default_3d_coordinate_adapter(element_geometry)

    def _execute_adapter(self, element_geometry, element_tapping_points):
        coordinate_list_2d = list(element_geometry)
        coordinate_list_2d = [list(coord_tuple) for coord_tuple in coordinate_list_2d]
        thickness_list = []
        z_coordinates = []
        for tap_point in element_tapping_points:
            x_and_y = tap_point[0:2]
            if any(x_and_y == coordinate_2d for coordinate_2d in coordinate_list_2d):
                if self.lkobject_type == 'lklinie':
                    z_line_coordinate = tap_point[2] - ((tap_point[2] - tap_point[3]) / 2)
                    self.coordinates_3d.append([tap_point[0], tap_point[1], z_line_coordinate])
                    z_coordinates.append(z_line_coordinate)
                elif self.lkobject_type == 'lkflaeche':
                    thickness_list.append(tap_point[2] - tap_point[3])
                    self.coordinates_3d.append([tap_point[0], tap_point[1], tap_point[3]])
                    z_coordinates.append(tap_point[3])
                coordinate_list_2d.remove(x_and_y)
        if coordinate_list_2d:
            for coordinate in coordinate_list_2d:
                z_line_coordinate = mean(z_coordinates) if z_coordinates else self.scale_attributes[2]
                self.coordinates_3d.append([coordinate[0], coordinate[1], z_line_coordinate])
        self.area_thickness = mean(thickness_list) if thickness_list else 1.0

    def _scale_objects(self, coordinates) -> any:
        scaled_coordinates = ()
        for coordinate_tuple in coordinates:
            x_coord, y_coord, z_coord = coordinate_tuple
            x_coord -= self.scale_attributes[0]
            y_coord -= self.scale_attributes[1]
            z_coord -= self.scale_attributes[2]
            scaled_coordinates += ((round(x_coord, 4), round(y_coord, 4), round(z_coord, 4)),)
        return scaled_coordinates
