import unittest
from statistics import mean

from model.CoordinateAdapter import CoordinateAdapter


class CoordinateAdapterTestCase(unittest.TestCase):

    def setUp(self):
        self.scale_attributes = (2691000.0, 1236000.0, 420.0)
        self.coordinate_adapter = CoordinateAdapter(self.scale_attributes)
        self.coordinate_adapter.lkobject_type = 'lkflaeche'
        self.area_element = {
            'areaId': {"geometry": [[[2691055.0, 1236166.0], [2691059.0, 1236164.0], [2691058.0, 1236163.0],
                                     [2691054.0, 1236165.0], [2691055.0, 1236166.0]]]}}
        self.area_element_nomatch = {'areaId': {
            "geometry": [[[2691045.0, 1236143.0], [2691044.5, 1236142.5], [2691037.0, 1236152.0]]]}}
        self.area_tap_points = {
            'areaId': [[2691055.0, 1236166.0, 418.0, 416.0], [2691059.0, 1236164.0, 418.0, 415.0],
                       [2691058.0, 1236163.0, 418.0, 414.0], [2691054.0, 1236165.0, 418.0, 416.0],
                       [2691055.0, 1236166.0, 417.0, 415.0]]
        }
        self.area_tap_points_incomplete = {
            'areaId': [[2691055.0, 1236166.0, 418.0, 416.0], [2691059.0, 1236164.0, 418.0, 415.0],
                       [2691058.0, 1236163.0, 418.0, 414.0]]
        }

    # Case 1: There are no Tapping points
    def test_execute_default_3d_coordinate_adapter_areas(self):
        self.coordinate_adapter.lkobject_type = 'lkflaeche'
        self.coordinate_adapter.coordinates_3d = []
        self.coordinate_adapter._execute_default_3d_coordinate_adapter(self.area_element['areaId']['geometry'][0])
        z_coord = self.scale_attributes[2] - 2.0
        expected_result = [[2691055.0, 1236166.0, z_coord], [2691059.0, 1236164.0, z_coord],
                           [2691058.0, 1236163.0, z_coord], [2691054.0, 1236165.0, z_coord],
                           [2691055.0, 1236166.0, z_coord]]
        self.assertEqual(expected_result, self.coordinate_adapter.coordinates_3d)
        self.assertEqual(2.0, self.coordinate_adapter.area_thickness)

    # Case 2: All Tapping points matching
    def test_area_coordinate_adapting(self):
        self.coordinate_adapter.coordinates_3d = []
        self.coordinate_adapter._execute_adapter(self.area_element['areaId']['geometry'][0],
                                                 self.area_tap_points['areaId'])
        expected_list_3d = []
        for coordinate in self.area_tap_points['areaId']:
            expected_list_3d.append([coordinate[0], coordinate[1], coordinate[3]])
        self.assertEqual(expected_list_3d, self.coordinate_adapter.coordinates_3d)
        self.assertEqual(2.6, self.coordinate_adapter.area_thickness)

    # Case 3: There are Tapping points not matching, take mean of all other z coordinates
    def test_area_coordinate_adapting_not_all_matching(self):
        self.coordinate_adapter.coordinates_3d = []
        self.coordinate_adapter._execute_adapter(self.area_element['areaId']['geometry'][0],
                                                 self.area_tap_points_incomplete['areaId'])
        expected_list_3d = []
        z_coords = []
        for coordinate in self.area_tap_points_incomplete['areaId']:
            z_coords.append(coordinate[3])
            expected_list_3d.append([coordinate[0], coordinate[1], coordinate[3]])
        expected_list_3d.append([2691054.0, 1236165.0, mean(z_coords)])
        expected_list_3d.append([2691055.0, 1236166.0, mean(z_coords)])
        self.assertEqual(expected_list_3d, self.coordinate_adapter.coordinates_3d)
        self.assertEqual(3.0, self.coordinate_adapter.area_thickness)

    # Case 4: There are Tapping points but none match
    def test_area_coordinate_adapting_no_matching(self):
        self.coordinate_adapter.coordinates_3d = []
        self.coordinate_adapter._execute_adapter(self.area_element_nomatch['areaId']['geometry'][0],
                                                 self.area_tap_points['areaId'])
        z_coord = self.scale_attributes[2] - 2.0
        expected_result = [[2691045.0, 1236143.0, z_coord], [2691044.5, 1236142.5, z_coord],
                           [2691037.0, 1236152.0, z_coord]]
        self.assertEqual(expected_result, self.coordinate_adapter.coordinates_3d)
        self.assertEqual(2.0, self.coordinate_adapter.area_thickness)

if __name__ == '__main__':
    unittest.main()
