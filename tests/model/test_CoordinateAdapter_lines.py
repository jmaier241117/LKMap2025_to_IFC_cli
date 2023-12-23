import unittest
from statistics import mean

from model.CoordinateAdapter import CoordinateAdapter


class CoordinateAdapterTestCase(unittest.TestCase):

    def setUp(self):
        self.scale_attributes = (2691000.0, 1236000.0, 420.0)
        self.coordinate_adapter = CoordinateAdapter(self.scale_attributes)
        self.coordinate_adapter.lkobject_type = 'lklinie'
        self.line_element = {
            'lineId': {
                "geometry": [[2691044.0, 1236142.0], [2691043.0, 1236141.0], [2691036.0, 1236151.0]]}}
        self.line_element_nomatch = {'lineId': {
            "geometry": [[2691045.0, 1236143.0], [2691044.5, 1236142.5], [2691037.0, 1236152.0]]}}
        self.line_tap_points = {
            'lineId': [[2691044.0, 1236142.0, 418.0, 416.0], [2691043.0, 1236141.0, 418.0, 415.0],
                       [2691036.0, 1236151.0, 418.0, 414.0]]
        }
        self.line_tap_points_incomplete = {
            'lineId': [[2691044.0, 1236142.0, 418.0, 416.0], [2691043.0, 1236141.0, 418.0, 415.0]]
        }

    # Case 1: There are no Tapping points
    def test_execute_default_3d_coordinate_adapter_lines(self):
        self.coordinate_adapter.coordinates_3d = []
        self.coordinate_adapter._execute_default_3d_coordinate_adapter(self.line_element['lineId']['geometry'])
        z_coord = self.scale_attributes[2] - 2.0
        expected_result = [[2691044.0, 1236142.0, z_coord], [2691043.0, 1236141.0, z_coord],
                           [2691036.0, 1236151.0, z_coord]]
        self.assertEqual(expected_result, self.coordinate_adapter.coordinates_3d)

    # Case 2: All Tapping points matching
    def test_line_coordinate_adapting(self):
        self.coordinate_adapter.coordinates_3d = []
        self.coordinate_adapter._execute_adapter(self.line_element['lineId']['geometry'],
                                                 self.line_tap_points['lineId'])
        expected_list_3d = []
        for coordinate in self.line_tap_points['lineId']:
            z_line_coordinate = coordinate[2] - ((coordinate[2] - coordinate[3]) / 2)
            expected_list_3d.append([coordinate[0], coordinate[1], z_line_coordinate])
        self.assertEqual(expected_list_3d, self.coordinate_adapter.coordinates_3d)

    # Case 3: There are Tapping points not matching, take mean of all other z coordinates
    def test_line_coordinate_adapting_not_all_matching(self):
        self.coordinate_adapter.coordinates_3d = []
        self.coordinate_adapter._execute_adapter(self.line_element['lineId']['geometry'],
                                                 self.line_tap_points_incomplete['lineId'])
        expected_list_3d = []
        z_coords = []
        for coordinate in self.line_tap_points_incomplete['lineId']:
            z_line_coordinate = coordinate[2] - ((coordinate[2] - coordinate[3]) / 2)
            z_coords.append(z_line_coordinate)
            expected_list_3d.append([coordinate[0], coordinate[1], z_line_coordinate])
        expected_list_3d.append([2691036.0, 1236151.0, mean(z_coords)])
        self.assertEqual(expected_list_3d, self.coordinate_adapter.coordinates_3d)

    # Case 4: There are Tapping points but none match
    def test_line_coordinate_adapting_no_matching(self):
        self.coordinate_adapter.coordinates_3d = []
        self.coordinate_adapter._execute_adapter(self.line_element_nomatch['lineId']['geometry'],
                                                 self.line_tap_points['lineId'])
        z_coord = self.scale_attributes[2] - 2.0
        expected_result = [[2691045.0, 1236143.0, z_coord], [2691044.5, 1236142.5, z_coord],
                           [2691037.0, 1236152.0, z_coord]]
        self.assertEqual(expected_result, self.coordinate_adapter.coordinates_3d)


if __name__ == '__main__':
    unittest.main()
