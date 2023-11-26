import unittest
from unittest.mock import MagicMock

import geopandas
import pandas
from shapely import box, linestrings, points

from model.DataProcessingChain import DataProcessingChain
from model.GeometryProcessor import LKObjectTypeProcessor, RangeConstraintProcessor, GroupingToDictionaryFilter
from model.CharacteristicsFilter import CharacteristicsProcessor


class FilterChainTestCase(unittest.TestCase):

    def setUp(self):
        self.geopackage = "geopackage"
        self.clipsrc = "clipsrc"
        self.filter_chain = DataProcessingChain(self.geopackage, self.clipsrc)

    def test_execute_filters(self):
        # Mock the necessary filter classes and their execute_filter methods

        LKObjectTypeProcessor.execute_filter = MagicMock(
            return_value={
                'lkflaeche': geopandas.GeoDataFrame(geometry=[box(1, 1, 2, 2), box(3, 3, 4, 4), box(4.2, 4.2, 5, 5)]),
                'lklinie': geopandas.GeoDataFrame(
                    geometry=linestrings([[[0, 1], [4, 5]], [[2, 3], [5, 6]], [[1, 1], [3, 1]]]).tolist()),
                'lkpunkt': geopandas.GeoDataFrame(geometry=points([[0, 1], [4, 5], [2, 3]]).tolist()),
            })
        RangeConstraintProcessor.execute_filter = MagicMock(return_value={
            'lkflaeche': geopandas.GeoDataFrame(pandas.DataFrame({'obj_id': ['d', 'e'],
                                                                  'objektart': [4, 4],
                                                                  'eigentuemer': ['Bob', 'Ali']}),
                                                geometry=[box(1, 1, 2, 2), box(3, 3, 4, 4)]),
            'lklinie': geopandas.GeoDataFrame(pandas.DataFrame({'obj_id': ['b', 'c'],
                                                                'objektart': [4, 4],
                                                                'eigentuemer': ['Bob', 'Ali']}),
                                              geometry=linestrings([[[0, 1], [4, 5]], [[2, 3], [5, 6]]]).tolist()),
            'lkpunkt': geopandas.GeoDataFrame(pandas.DataFrame({'obj_id': ['a'],
                                                                'objektart': [4],
                                                                'eigentuemer': ['Bob']}),
                                              geometry=points([[2, 3]]).tolist()),
        })
        area_grouping_filter_mock = GroupingToDictionaryFilter('dummy_dataset', 'lkflaeche')
        line_grouping_filter_mock = GroupingToDictionaryFilter('dummy_dataset', 'lklinie')
        point_grouping_filter_mock = GroupingToDictionaryFilter('dummy_dataset', 'lkpunkt')
        point_grouping_filter_mock.execute_filter = MagicMock(return_value={'lkobject_type': 'lkpunkt',
                                                                            'a': {'object_type': 4,
                                                                                  'object_owner': 'Bob',
                                                                                  'geometry': (
                                                                                      2, 3)}})
        line_grouping_filter_mock.execute_filter = MagicMock(return_value={'lkobject_type': 'lklinie',
                                                                           'b': {'object_type': 52,
                                                                                 'object_owner': 'Bob',
                                                                                 'geometry': (
                                                                                     (0, 1), (4, 5))
                                                                                 },
                                                                           'c': {'object_type': 4,
                                                                                 'object_owner': 'Ali',
                                                                                 'geometry': (
                                                                                     (2, 3), (5, 6))
                                                                                 }})
        area_grouping_filter_mock.execute_filter = MagicMock(return_value={'lkobject_type': 'lkflaeche',
                                                                           'd': {'object_type': 4,
                                                                                 'object_owner': 'Bob',
                                                                                 'geometry': (
                                                                                     (2, 1), (2, 2),
                                                                                     (1, 2),
                                                                                     (1, 1), (2, 1))},
                                                                           'e': {'object_type': 4,
                                                                                 'object_owner': 'Ali',
                                                                                 'geometry': (
                                                                                     (4, 3), (4, 4),
                                                                                     (3, 4),
                                                                                     (3, 3), (4, 3))}})
        CharacteristicsProcessor.execute_filter = MagicMock(return_value={
            'Funktion': 'Sammelkanal',
            'Nutzungsart': 'Regenabwasser'
        })
        geopackage = 'data.gpkg'
        filter_chain = DataProcessingChain(geopackage, [2, 2, 4, 4])
        result = filter_chain.execute_filters()
        expected_result = ({'lkobject_type': 'lkflaeche',
                            'd': {'object_type': 4, 'object_owner': 'Bob',
                                  'geometry': (((2.0, 1.0), (2.0, 2.0), (1.0, 2.0), (1.0, 1.0), (2.0, 1.0)),),
                                  'characteristics': {'Funktion': 'Sammelkanal', 'Nutzungsart': 'Regenabwasser'}},
                            'e': {'object_type': 4, 'object_owner': 'Ali',
                                  'geometry': (((4.0, 3.0), (4.0, 4.0), (3.0, 4.0), (3.0, 3.0), (4.0, 3.0)),),
                                  'characteristics': {'Funktion': 'Sammelkanal', 'Nutzungsart': 'Regenabwasser'}}},
                           {'lkobject_type': 'lklinie',
                            'b': {'object_type': 4, 'object_owner': 'Bob', 'geometry': ((0.0, 1.0), (4.0, 5.0)),
                                  'characteristics': {'Funktion': 'Sammelkanal', 'Nutzungsart': 'Regenabwasser'}},
                            'c': {'object_type': 4, 'object_owner': 'Ali', 'geometry': ((2.0, 3.0), (5.0, 6.0)),
                                  'characteristics': {'Funktion': 'Sammelkanal', 'Nutzungsart': 'Regenabwasser'}}},
                           {'lkobject_type': 'lkpunkt',
                            'a': {'object_type': 4, 'object_owner': 'Bob', 'geometry': (2.0, 3.0),
                                  'characteristics': {'Funktion': 'Sammelkanal', 'Nutzungsart': 'Regenabwasser'}}})
        self.assertEqual(result, expected_result)


if __name__ == '__main__':
    unittest.main()
