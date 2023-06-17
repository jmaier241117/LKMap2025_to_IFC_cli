import unittest
import sqlite3
from unittest.mock import patch
from model.CharacteristicsFilter import CharacteristicsFilter


class CharacteristicsFilterTestCase(unittest.TestCase):
    @patch('model.CharacteristicsFilter.sqlite3.connect')
    def test_execute_filter(self, mock_connect):
        # Mock the database connection and cursor
        mock_cursor = mock_connect.return_value.cursor.return_value

        # Set up the mock query results
        mock_cursor.fetchone.return_value = ('465',)
        mock_cursor.fetchall.return_value = [('Funktion', 'Sammelkanal'),
                                             ('Nutzungsart', 'Regenabwasser')]

        # Create an instance of the CharacteristicsFilter class
        dataset = 'data.gpkg'
        filter_attribute = {'obj_id': 'ch14fhv800471660', 'lkobject_type': 'area'}
        characteristics_filter = CharacteristicsFilter(dataset, filter_attribute)

        # Call the execute_filter method
        result = characteristics_filter.execute_filter()

        # Assert the expected results
        expected_result = (('Funktion', 'Sammelkanal'),
                           ('Nutzungsart', 'Regenabwasser'))
        self.assertEqual(result, expected_result)

        # Assert the database connection and queries
        mock_connect.assert_called_once_with('data.gpkg')
        mock_cursor.fetchall.assert_called_once()
        mock_cursor.execute.assert_called_with(
            "SELECT bezeichnung, wert FROM eigenschaften WHERE area_eigenschaft = (SELECT T_Id FROM area WHERE "
            "T_Ili_Tid = 'ch14fhv800471660')")


if __name__ == '__main__':
    unittest.main()
