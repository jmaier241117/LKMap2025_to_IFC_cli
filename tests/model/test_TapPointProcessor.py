import unittest

from model.TapPointProcessor import TapPointProcessor


class TapPointProcessorTestCase(unittest.TestCase):

    def setUp(self):
        self.tap_point_processor = TapPointProcessor("mock")

    def test_no_tappoints(self):
        self.tap_point_processor.tap_point_geometries = None
        result = self.tap_point_processor.execute_processor('mock')
        self.assertIsNone(result)

    def test_only_kotez_available(self):
        self.tap_point_processor.tap_point_geometries = {
            'pointId': [(2691043.022, 1236156.274, 3.0)]
        }
        result = self.tap_point_processor._combine_tap_points()
        expected_result = {
            'pointId': []
        }
        self.assertEqual(expected_result, result)

    def test_duplicate_tapping_points(self):
        self.tap_point_processor.tap_point_geometries = {
            'pointId': [(2691043.022, 1236156.274, 3.0), (2691043.022, 1236156.274, 4.0),
                        (2691043.022, 1236156.274, 3.0), (2691043.022, 1236156.274, 4.0)]
        }
        result = self.tap_point_processor._combine_tap_points()
        expected_result = {
            'pointId': [[2691043.022, 1236156.274, 4.0, 3.0]]
        }
        self.assertEqual(expected_result, result)

    def test_combine_point_kotez_and_koteref(self):
        self.tap_point_processor.tap_point_geometries = {
            'pointId': [(2691043.022, 1236156.274, 3.0), (2691043.022, 1236156.274, 4.0)]
        }
        result = self.tap_point_processor._combine_tap_points()
        expected_result = {
            'pointId': [[2691043.022, 1236156.274, 4.0, 3.0]]
        }
        self.assertEqual(expected_result, result)

    def test_combine_line_kotez_and_koteref(self):
        self.tap_point_processor.tap_point_geometries = {
            'lineId': [(2691043.022, 1236156.274, 3.0), (2691043.022, 1236156.274, 4.0),
                       (2691031.557, 1236139.135, 2.0), (2691031.557, 1236139.135, 1.0)]
        }
        result = self.tap_point_processor._combine_tap_points()
        expected_result = {
            'lineId': [[2691043.022, 1236156.274, 4.0, 3.0], [2691031.557, 1236139.135, 2.0, 1.0]]
        }
        self.assertEqual(expected_result, result)

    def test_combine_multiple_lines_kotez_and_koteref(self):
        self.tap_point_processor.tap_point_geometries = {
            'lineId1': [(2691043.022, 1236156.274, 3.0), (2691043.022, 1236156.274, 4.0),
                        (2691031.557, 1236139.135, 2.0), (2691031.557, 1236139.135, 1.0)],
            'lineId2': [(2691043.022, 1236156.274, 3.0), (2691043.022, 1236156.274, 4.0),
                        (2691031.557, 1236139.135, 2.0), (2691031.557, 1236139.135, 1.0)]
        }
        result = self.tap_point_processor._combine_tap_points()
        expected_result = {
            'lineId1': [[2691043.022, 1236156.274, 4.0, 3.0], [2691031.557, 1236139.135, 2.0, 1.0]],
            'lineId2': [[2691043.022, 1236156.274, 4.0, 3.0], [2691031.557, 1236139.135, 2.0, 1.0]]
        }
        self.assertEqual(expected_result, result)


if __name__ == '__main__':
    unittest.main()
