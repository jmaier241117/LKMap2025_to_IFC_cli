import unittest
from unittest.mock import MagicMock
from model.FilterChain import FilterChain
from model.GeometryFilter import LKObjectTypeFilter, RangeConstraintFilter, GroupingToDictionaryFilter
from model.CharacteristicsFilter import CharacteristicsFilter


class FilterChainTestCase(unittest.TestCase):
    def test_execute_filters(self):
        # Mock the necessary filter classes and their execute_filter methods
        LKObjectTypeFilter.execute_filter = MagicMock(return_value={
            'area_objects': {'a': 1, 'b': 2},
            'line_objects': {'c': 3, 'd': 4},
            'point_objects': {'e': 5, 'f': 6}
        })

        RangeConstraintFilter.execute_filter = MagicMock(return_value={
            'lkflaeche': {'a': 1},
            'lklinie': {'c': 3},
            'lkpunkt': {'e': 5}
        })

        GroupingToDictionaryFilter.execute_filter = MagicMock(return_value={
            'lkobject_type': 'lklinie',
            'b': {'object_type': 'lkflaeche', 'object_owner': 'Rothenfluh', 'geometry': [(1, 2), (3, 4)]},
            'd': {'object_type': 'lklinie', 'object_owner': 'Rothenfluh', 'geometry': [(5, 6), (7, 8)]}
        })

        CharacteristicsFilter.execute_filter = MagicMock(return_value={
            'Funktion': 'Sammelkanal',
            'Nutzungsart': 'Regenabwasser'
        })

        geopackage = 'data.gpkg'
        filter_attributes = {
            'clipsrc': [0, 0, 10, 10],
            'lkobject_types': ['lkflaeche', 'lklinie']
        }
        filter_chain = FilterChain(geopackage, filter_attributes)

        result = filter_chain.execute_filters()

        expected_result = [
            {
                'b': {
                    'object_type': 'lkflaeche',
                    'object_owner': 'Rothenfluh',
                    'geometry': [(1, 2), (3, 4)],
                    'characteristics': {
                        'Funktion': 'Sammelkanal',
                        'Nutzungsart': 'Regenabwasser'
                    }
                }
            },
            {
                'd': {
                    'object_type': 'lklinie',
                    'object_owner': 'Rothenfluh',
                    'geometry': [(5, 6), (7, 8)],
                    'characteristics': {
                        'Funktion': 'Sammelkanal',
                        'Nutzungsart': 'Regenabwasser'
                    }
                }

            },
            {'lkobject_type': 'lklinie'}
        ]
        # self.assertEqual(result, expected_result)


if __name__ == '__main__':
    unittest.main()
