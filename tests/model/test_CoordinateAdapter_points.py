import unittest

from model.CoordinateAdapter import CoordinateAdapter


class CoordinateAdapterTestCase(unittest.TestCase):

    def setUp(self):
        self.scale_attributes = (2691000.0, 1236000.0, 420.0)
        self.coordinate_adapter = CoordinateAdapter(self.scale_attributes)
        self.coordinate_adapter.lkobject_type = 'lkpunkt'
        self.point_element = {'pointId': {"geometry": [2691035.0, 1236152.0]}}
        self.point_element_nomatch = {'pointId': {"geometry": [2691036.0, 1236153.0]}}
        self.point_tap_points = {'pointId': [[2691035.0, 1236152.0, 418.0, 416.0]]}

    # Case 1: There are no Tapping points
    def test_execute_default_3d_coordinate_adapter_points(self):
        self.coordinate_adapter.coordinates_3d = []
        self.coordinate_adapter._execute_default_3d_coordinate_adapter(self.point_element['pointId']['geometry'])
        expected_result = [[2691035.0, 1236152.0, self.scale_attributes[2]],
                           [2691035.0, 1236152.0, self.scale_attributes[2] - 2.0]]
        self.assertEqual(expected_result, self.coordinate_adapter.coordinates_3d)

    # Case 2: There are Tapping points matching
    def test_execute_points_adapter(self):
        self.coordinate_adapter.coordinates_3d = []
        self.coordinate_adapter._execute_points_adapter(self.point_element['pointId']['geometry'],
                                                        self.point_tap_points['pointId'][0])
        expected_list_3d = [[2691035.0, 1236152.0, self.point_tap_points['pointId'][0][2]],
                            [2691035.0, 1236152.0, self.point_tap_points['pointId'][0][3]]]
        self.assertEqual(expected_list_3d, self.coordinate_adapter.coordinates_3d)

    # Case 3: There are Tappoints not matching, back to default
    def test_execute_points_adapter_no_match(self):
        self.coordinate_adapter.coordinates_3d = []
        self.coordinate_adapter._execute_points_adapter(self.point_element_nomatch['pointId']['geometry'],
                                                        self.point_tap_points['pointId'][0])
        expected_list_3d = [[2691036.0, 1236153.0, self.scale_attributes[2]],
                            [2691036.0, 1236153.0, self.scale_attributes[2] - 2.0]]
        self.assertEqual(expected_list_3d, self.coordinate_adapter.coordinates_3d)


if __name__ == '__main__':
    unittest.main()
