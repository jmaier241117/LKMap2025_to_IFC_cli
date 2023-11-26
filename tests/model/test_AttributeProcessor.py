import unittest
from unittest.mock import patch

from model.AttributeProcessor import AttributeProcessor


class CharacteristicsFilterTestCase(unittest.TestCase):
    @patch('model.AttributeProcessor.sqlite3.connect')
    def test_execute_processor_lkobject_types(self, mock_connect):
        # Mock the database connection and cursor
        mock_cursor = mock_connect.return_value.cursor.return_value

        # Create an instance of the CharacteristicsFilter class
        dataset = 'data.gpkg'
        filter_attribute = {}
        attribute_processor = AttributeProcessor(dataset, filter_attribute)

        # Set up the mock query results
        mock_cursor.fetchone.return_value = ('465',)
        mock_cursor.fetchall.return_value = [('3', 'Abwasser.Spezialbauwerk.Pumpwerk'),
                                             ('4', 'Abwasser.Spezialbauwerk.weitere')]

        # Call the execute_filter method
        result = attribute_processor._get_object_types('lkflaeche')

        # Assert the expected results
        expected_result = {'3': 'Abwasser.Spezialbauwerk.Pumpwerk',
                           '4': 'Abwasser.Spezialbauwerk.weitere'}
        self.assertEqual(result, expected_result)

        # Assert the database connection and queries
        mock_connect.assert_called_once_with('data.gpkg')
        mock_cursor.fetchall.assert_called_once()
        mock_cursor.execute.assert_called_with("SELECT T_Id, iliCode FROM lkflaeche_objektart")


if __name__ == '__main__':
    unittest.main()
