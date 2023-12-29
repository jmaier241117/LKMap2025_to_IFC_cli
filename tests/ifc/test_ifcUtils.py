import unittest

import ifcopenshell

from ifc.IfcUtils import initialize_styles, initialize_zero_points, initialize_directions


class TestIfcUtils(unittest.TestCase):
    def setUp(self):
        self.ifc_file = ifcopenshell.file(schema="IFC4X3")

    def test_initialize_styles(self):
        initialize_styles(self.ifc_file)
        styles = self.ifc_file.by_type("IfcSurfaceStyle")
        colors = self.ifc_file.by_type("IfcColourRgb")
        self.assertEqual(4, len(styles))
        self.assertEqual(4, len(colors))

    def test_initialize_zero_points(self):
        initialize_zero_points(self.ifc_file)
        self.assertEqual(2, len(self.ifc_file.by_type("IfcCartesianPoint")))

    def test_initalize_directions(self):
        initialize_directions(self.ifc_file)
        self.assertEqual(3, len(self.ifc_file.by_type("IfcDirection")))


if __name__ == '__main__':
    unittest.main()