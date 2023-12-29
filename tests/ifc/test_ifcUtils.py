import unittest

import ifcopenshell

from ifc.IfcUtils import initialize_styles


class TestIfcUtils(unittest.TestCase):
    def setUp(self):
        self.ifc_file = ifcopenshell.file(schema="IFC4X3")

    def test_initialize_styles(self):
        initialize_styles(self.ifc_file)
        styles = self.ifc_file.by_type("IfcSurfaceStyle")
        colors = self.ifc_file.by_type("IfcColourRgb")
        self.assertEquals(4, len(styles))
        self.assertEquals(4, len(colors))



if __name__ == '__main__':
    unittest.main()