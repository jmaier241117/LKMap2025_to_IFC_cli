import unittest

import ifcopenshell

from ifc.IfcElementBuilders import IfcDuctElementBuilder
from ifc.IfcUtils import initialize_zero_points, initialize_directions, initialize_contexts, initialize_styles, \
    Uncertainty


class TestIfcPipeElementBuilder(unittest.TestCase):
    def setUp(self):
        self.ifc_file = ifcopenshell.file(schema="IFC4X3")
        initialize_zero_points(self.ifc_file)
        initialize_directions(self.ifc_file)
        initialize_contexts(self.ifc_file)
        initialize_styles(self.ifc_file)
        self.builder = IfcDuctElementBuilder(self.ifc_file).element_name('duct').coordinates(
            [[2.446, -32.828, 0.0], [2.446, -32.828, -2.0]]).radius(600.0)

    def test_duct_creation_no_uncertainties(self):
        self.builder.position_uncertain(Uncertainty.PRECISE).height_position_uncertain(
            Uncertainty.PRECISE).build()
        self.assertEqual(1, len(self.ifc_file.by_type("IfcDistributionElement")))
        # one default styled item
        self.assertEqual(1, len(self.ifc_file.by_type("IfcStyledItem")))

    def test_duct_creation_with_height_uncertainties(self):
        self.builder.position_uncertain(Uncertainty.PRECISE).height_position_uncertain(Uncertainty.UNKNOWN).build()
        self.assertEqual(1, len(self.ifc_file.by_type("IfcDistributionElement")))
        # one height uncertainty styled item
        self.assertEqual(2, len(self.ifc_file.by_type("IfcStyledItem")))

    def test_duct_creation_with_position_uncertainties(self):
        self.builder.position_uncertain(Uncertainty.UNKNOWN).height_position_uncertain(Uncertainty.PRECISE).build()
        self.assertEqual(1, len(self.ifc_file.by_type("IfcDistributionElement")))
        # one uncertainty styled item + the default style
        self.assertEqual(2, len(self.ifc_file.by_type("IfcStyledItem")))

    def test_duct_creation_with_position_and_height_uncertainties(self):
        self.builder.position_uncertain(Uncertainty.UNKNOWN).height_position_uncertain(Uncertainty.UNKNOWN).build()
        self.assertEqual(1, len(self.ifc_file.by_type("IfcDistributionElement")))
        # one height uncertainty styled item + one position uncertainty style + the default style
        self.assertEqual(3, len(self.ifc_file.by_type("IfcStyledItem")))


if __name__ == '__main__':
    unittest.main()
