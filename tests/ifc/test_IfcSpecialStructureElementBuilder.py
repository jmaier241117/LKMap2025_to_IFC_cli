import unittest

import ifcopenshell

from ifc.IfcElementBuilders import IfcSpecialStructureElementBuilder
from ifc.IfcUtils import initialize_zero_points, initialize_directions, initialize_contexts, initialize_styles, \
    Uncertainty


class TestIfcPipeElementBuilder(unittest.TestCase):
    def setUp(self):
        self.ifc_file = ifcopenshell.file(schema="IFC4X3")
        initialize_zero_points(self.ifc_file)
        initialize_directions(self.ifc_file)
        initialize_contexts(self.ifc_file)
        initialize_styles(self.ifc_file)
        self.builder = (IfcSpecialStructureElementBuilder(self.ifc_file).element_name('special structure').coordinates(
            [[2.446, -32.828, -2.45], [1.746, -31.939, -2.55], [-0.834, -29.077, -2.65], [2.446, -32.828, -2.45]])
                        .thickness(1.0))

    def test_special_structure_creation_no_uncertainties(self):
        self.builder.position_uncertain(Uncertainty.PRECISE).height_position_uncertain(
            Uncertainty.PRECISE).build()
        self.assertEqual(1, len(self.ifc_file.by_type("IfcDistributionElement")))
        # one default styled item
        self.assertEqual(1, len(self.ifc_file.by_type("IfcStyledItem")))

    def test_special_structure_creation_with_height_uncertainties(self):
        self.builder.position_uncertain(Uncertainty.PRECISE).height_position_uncertain(Uncertainty.UNKNOWN).build()
        self.assertEqual(1, len(self.ifc_file.by_type("IfcDistributionElement")))
        # one height uncertainty styled item
        self.assertEqual(2, len(self.ifc_file.by_type("IfcStyledItem")))

    def test_special_structure_creation_with_position_uncertainties(self):
        self.builder.position_uncertain(Uncertainty.UNKNOWN).height_position_uncertain(Uncertainty.PRECISE).build()
        self.assertEqual(1, len(self.ifc_file.by_type("IfcDistributionElement")))
        # one uncertainty styled item + the default style
        self.assertEqual(2, len(self.ifc_file.by_type("IfcStyledItem")))

    def test_special_structure_creation_with_position_and_height_uncertainties(self):
        self.builder.position_uncertain(Uncertainty.UNKNOWN).height_position_uncertain(Uncertainty.UNKNOWN).build()
        self.assertEqual(1, len(self.ifc_file.by_type("IfcDistributionElement")))
        # one height uncertainty styled item + one position uncertainty style + the default style
        self.assertEqual(3, len(self.ifc_file.by_type("IfcStyledItem")))


if __name__ == '__main__':
    unittest.main()
