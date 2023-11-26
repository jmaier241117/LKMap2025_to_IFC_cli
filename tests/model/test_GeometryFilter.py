import unittest
import geopandas
from shapely import box, linestrings, points

from model.GeometryProcessor import LKObjectTypeProcessor, RangeConstraintProcessor, GroupingToDictionaryFilter


class TestLKObjectTypeFilter(unittest.TestCase):
    def test_execute_filter(self):
        dataset = "Rothenfluh.gpkg"
        filter_obj = LKObjectTypeProcessor(dataset, None)
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
                geometry=linestrings(
                    [[[0, 1], [4, 5]], [[2, 3], [5, 6]], [[1, 1], [4, 1]]]).tolist()),
            'point_objects': geopandas.GeoDataFrame(geometry=points([[0, 1], [4, 5], [2, 3]]).tolist()),
        }
        self.expected_element_count = {
            'lkflaeche': 2,
            'lklinie': 2,
            'lkpunkt': 1
        }
        filter_attribute = [2, 2, 4, 4]
        self.filter_obj = RangeConstraintProcessor(dataset, filter_attribute)

    def test_execute_filter(self):
        result = self.filter_obj.execute_filter()
        print(result)
        self.assertIsInstance(result, dict)

        # Check if the necessary keys are present in the result
        self.assertIn('lkflaeche', result)
        self.assertIn('lklinie', result)
        self.assertIn('lkpunkt', result)

        # Check if the values of the keys are of the expected type (GeoDataFrame)
        self.assertIsInstance(result['lkflaeche'], geopandas.GeoDataFrame)
        self.assertIsInstance(result['lklinie'], geopandas.GeoDataFrame)
        self.assertIsInstance(result['lkpunkt'], geopandas.GeoDataFrame)

        self.assertEquals(len(result['lkflaeche']), self.expected_element_count['lkflaeche'])
        self.assertEquals(len(result['lklinie']), self.expected_element_count['lklinie'])
        self.assertEquals(len(result['lkpunkt']), self.expected_element_count['lkpunkt'])


class TestGroupingToDictionaryFilter(unittest.TestCase):
    def setUp(self):
        first_filter_result = LKObjectTypeProcessor("Rothenfluh.gpkg", None).execute_filter()
        self.dataset = RangeConstraintProcessor(first_filter_result,
                                                (2635955.3, 1256666.5, 2635997.8, 1256709.9)).execute_filter()
        self.filter_attributes = {
            'lkflaeche': 'ch14fhv800986760',
            'lklinie': 'ch14fhv800471660',
            'lkpunkt': 'ch14fhv8c8eb0343'
        }
        self.expected_element_count = {
            'lkflaeche': 5,
            'lklinie': 45,
            'lkpunkt': 18
        }

    def test_execute_filter(self):
        element_count = {
            'lkflaeche': 0,
            'lklinie': 0,
            'lkpunkt': 0
        }
        for key, value in self.filter_attributes.items():
            filter_obj = GroupingToDictionaryFilter(self.dataset, key)
            result = filter_obj.execute_filter()
            print(result)
            self.assertIsInstance(result, dict)
            self.assertEquals(result['lkobject_type'], key)
            self.assertIsInstance(result[value], dict)
            self.assertIn('object_type', result[value])
            self.assertIn('object_owner', result[value])
            self.assertIn('geometry', result[value])
            element_count[key] = len(result)
        # Plus one for the dictionary header defining the lkobject_type
        self.assertEquals(self.expected_element_count['lkflaeche'] + 1, element_count['lkflaeche'])
        self.assertEquals(self.expected_element_count['lklinie'] + 1, element_count['lklinie'])
        self.assertEquals(self.expected_element_count['lkpunkt'] + 1, element_count['lkpunkt'])


if __name__ == '__main__':
    unittest.main()
