import unittest
from unittest.mock import MagicMock

from controller import Controller
from model.FilterChain import FilterChain


class TestController(unittest.TestCase):
    def setUp(self):
        self.cli_arguments = {'gpkg': 'geopackage.gpkg', 'clipsrc': (2.0, 5.2, 4.0, 3.5)}
        self.cli_options = {'ifc_file_name': 'test.ifc'}
        self.controller = Controller(self.cli_arguments, self.cli_options)

    def test_run_conversion(self):
        FilterChain.execute_filters = MagicMock(return_value=
                                                ({'lkobject_type': 'lkflaeche',
                                                  'd': {'object_type': 4, 'object_owner': 'Bob',
                                                        'geometry': (
                                                            ((2.0, 1.0), (2.0, 2.0), (1.0, 2.0), (1.0, 1.0),
                                                             (2.0, 1.0)),),
                                                        'characteristics': {'Funktion': 'Sammelkanal',
                                                                            'Nutzungsart': 'Regenabwasser'}},
                                                  'e': {'object_type': 4, 'object_owner': 'Ali',
                                                        'geometry': (
                                                            ((4.0, 3.0), (4.0, 4.0), (3.0, 4.0), (3.0, 3.0),
                                                             (4.0, 3.0)),),
                                                        'characteristics': {'Funktion': 'Sammelkanal',
                                                                            'Nutzungsart': 'Regenabwasser'}}},
                                                 {'lkobject_type': 'lklinie',
                                                  'b': {'object_type': 4, 'object_owner': 'Bob',
                                                        'geometry': ((0.0, 1.0), (4.0, 5.0)),
                                                        'characteristics': {'Funktion': 'Sammelkanal',
                                                                            'Nutzungsart': 'Regenabwasser'}},
                                                  'c': {'object_type': 4, 'object_owner': 'Ali',
                                                        'geometry': ((2.0, 3.0), (5.0, 6.0)),
                                                        'characteristics': {'Funktion': 'Sammelkanal',
                                                                            'Nutzungsart': 'Regenabwasser'}}},
                                                 {'lkobject_type': 'lkpunkt',
                                                  'a': {'object_type': 4, 'object_owner': 'Bob', 'geometry': (2.0, 3.0),
                                                        'characteristics': {'Funktion': 'Sammelkanal',
                                                                            'Nutzungsart': 'Regenabwasser'}}}))
        self.controller.run_conversion()

