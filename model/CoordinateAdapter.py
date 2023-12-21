from statistics import mean


class CoordinateAdapter:
    def __init__(self, reference_null_point):
        self.scale_attributes = (reference_null_point[0], reference_null_point[1], reference_null_point[2])

    def execute_processor(self, lkobject_type, elements, tapping_points) -> any:
        adapted_elements = None
        if lkobject_type == 'lklinie':
            adapted_elements = self._execute_line_coordinate_adapter(elements, tapping_points)
        elif lkobject_type == 'lkpunkt':
            adapted_elements = self._execute_point_coordinate_adapter(elements, tapping_points)
        elif lkobject_type == 'lkflaeche':
            adapted_elements = self._execute_area_coordinate_adapter(elements, tapping_points)
        return adapted_elements

    def _execute_point_coordinate_adapter(self, elements, tapping_points) -> any:
        for key in elements.keys():
            coordinate_2d = list(elements[key]['geometry'])
            list_3d = []
            if key in tapping_points:
                tap_point = tapping_points[key][0]
                if tap_point[0:2] == coordinate_2d:
                    list_3d.append([tap_point[0], tap_point[1], tap_point[2]])
                    list_3d.append([tap_point[0], tap_point[1], tap_point[3]])
                else:
                    print("this should never happen")
            else:
                list_3d.append([coordinate_2d[0], coordinate_2d[1], self.scale_attributes[2]])
                list_3d.append([coordinate_2d[0], coordinate_2d[1], (self.scale_attributes[2] - 2)])
            elements[key]['geometry'] = self._scale_objects(list_3d)
        return elements

    def _execute_line_coordinate_adapter(self, elements, tapping_points) -> any:
        for key in elements.keys():
            coordinate_list_2d = list(elements[key]['geometry'])
            coordinate_list_2d = [list(coord_tuple) for coord_tuple in coordinate_list_2d]
            list_3d = []
            if key in tapping_points:
                tp_list = tapping_points[key]
                for index in tp_list:
                    x_and_y = index[0:2]
                    if any(x_and_y == coordinate_2d for coordinate_2d in coordinate_list_2d):
                        z_line_coordinate = index[2] - ((index[2] - index[3]) / 2)
                        list_3d.append([index[0], index[1], z_line_coordinate])
                        coordinate_list_2d.remove(x_and_y)
            if coordinate_list_2d:
                for index in coordinate_list_2d:
                    index.append(self.scale_attributes[2] - 1.5)
                    list_3d.append(index)
            elements[key]['geometry'] = self._scale_objects(list_3d)
        return elements

    def _execute_area_coordinate_adapter(self, elements, tapping_points) -> any:
        for key in elements.keys():
            coordinate_list_2d = list(elements[key]['geometry'][0])
            coordinate_list_2d = [list(coord_tuple) for coord_tuple in coordinate_list_2d]
            list_3d = []
            thickness = 0.0
            if key in tapping_points:
                tp_list = tapping_points[key]
                thickness_list = []
                for index in tp_list:
                    x_and_y = index[0:2]
                    if any(x_and_y == coordinate_2d for coordinate_2d in coordinate_list_2d):
                        thickness_list.append(index[2] - index[3])
                        list_3d.append([index[0], index[1], index[3]])
                        coordinate_list_2d.remove(x_and_y)
                thickness = mean(thickness_list)
            if coordinate_list_2d:
                for index in coordinate_list_2d:
                    index.append(self.scale_attributes[2] - 2)
                    list_3d.append(index)
            elements[key]['geometry'] = self._scale_objects(list_3d)
            elements[key]['thickness'] = thickness if thickness != 0.0 else 1.0
        return elements

    def _scale_objects(self, coordinates) -> any:
        scaled_coordinates = ()
        for coordinate_tuple in coordinates:
            x_coord, y_coord, z_coord = coordinate_tuple
            x_coord -= self.scale_attributes[0]
            y_coord -= self.scale_attributes[1]
            z_coord -= self.scale_attributes[2]
            scaled_coordinates += ((round(x_coord, 4), round(y_coord, 4), round(z_coord, 4)),)
        return scaled_coordinates
