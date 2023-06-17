import unittest
import geopandas
from shapely import box, linestrings, points

from model.GeometryFilter import LKObjectTypeFilter, RangeConstraintFilter, GroupingToDictionaryFilter


class TestLKObjectTypeFilter(unittest.TestCase):
    def test_execute_filter(self):
        dataset = "Rothenfluh.gpkg"
        filter_obj = LKObjectTypeFilter(dataset, None)
        result = filter_obj.execute_filter()

        self.assertIsInstance(result, dict)

        # Check if the values of the keys are of the expected type (GeoDataFrame)
        self.assertIsInstance(result['area_objects'], geopandas.GeoDataFrame)
        self.assertIsInstance(result['line_objects'], geopandas.GeoDataFrame)
        self.assertIsInstance(result['point_objects'], geopandas.GeoDataFrame)


class TestRangeConstraintFilter(unittest.TestCase):
    def setUp(self):
        dataset = {
            'area_objects': geopandas.GeoDataFrame(geometry=[box(1, 1, 2, 2), box(3, 3, 4, 4), box(4.2, 4.2, 5, 5)]),
            'line_objects': geopandas.GeoDataFrame(
                geometry=linestrings([[[0, 1], [4, 5]], [[2, 3], [5, 6]], [[1, 1], [3, 1]]]).tolist()),
            'point_objects': geopandas.GeoDataFrame(geometry=points([[0, 1], [4, 5], [2, 3]]).tolist()),
        }
        filter_attribute = [2, 2, 4, 4]
        self.filter_obj = RangeConstraintFilter(dataset, filter_attribute)

    def test_execute_filter(self):
        result = self.filter_obj.execute_filter()

        self.assertIsInstance(result, dict)

        # Check if the necessary keys are present in the result
        self.assertIn('range_area_objects', result)
        self.assertIn('range_line_objects', result)
        self.assertIn('range_point_objects', result)

        # Check if the values of the keys are of the expected type (GeoDataFrame)
        self.assertIsInstance(result['range_area_objects'], geopandas.GeoDataFrame)
        self.assertIsInstance(result['range_line_objects'], geopandas.GeoDataFrame)
        self.assertIsInstance(result['range_point_objects'], geopandas.GeoDataFrame)


class TestGroupingToDictionaryFilter(unittest.TestCase):
    def setUp(self):
        first_filter_result = LKObjectTypeFilter("Rothenfluh.gpkg", None).execute_filter()
        self.dataset = RangeConstraintFilter(first_filter_result,
                                             (2635955.3, 1256666.5, 2635997.8, 1256709.9)).execute_filter()
        filter_attribute = 'range_line_objects'
        self.filter_obj = GroupingToDictionaryFilter(self.dataset, filter_attribute)

    def test_execute_filter(self):
        result = self.filter_obj.execute_filter()
        self.assertIsInstance(result, dict)

        # Check if the values associated with obj_id keys are dictionaries
        for obj_id in self.dataset['range_line_objects']:
            self.assertIn(obj_id, result)
            self.assertIsInstance(result['ch14fhv800471660'], dict)

            # Check if the expected keys exist in each inner dictionary
            self.assertIn('object_type', result['ch14fhv800471660'])
            self.assertIn('object_owner', result['ch14fhv800471660'])
            self.assertIn('geometry', result['ch14fhv800471660'])


if __name__ == '__main__':
    unittest.main()
