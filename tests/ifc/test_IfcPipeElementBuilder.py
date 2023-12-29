import unittest

import ifcopenshell

from ifc.IfcElementBuilders import IfcPipeElementBuilder
from ifc.IfcUtils import initialize_zero_points, initialize_directions, initialize_contexts, initialize_styles, \
    Uncertainty


class TestIfcPipeElementBuilder(unittest.TestCase):
    def setUp(self):
        self.ifc_file = ifcopenshell.file(schema="IFC4X3")
        initialize_zero_points(self.ifc_file)
        initialize_directions(self.ifc_file)
        initialize_contexts(self.ifc_file)
        initialize_styles(self.ifc_file)
        self.builder = IfcPipeElementBuilder(self.ifc_file).element_name('pipe').coordinates(
            [[2.446, -32.828, -2.45], [1.746, -31.939, -2.55], [-0.834, -29.077, -2.65]]).radius(250.0)

    def test_line_creation_no_uncertainties(self):
        self.builder.position_uncertain(Uncertainty.PRECISE).height_position_uncertain(Uncertainty.PRECISE).build()
        self.assertEqual(1, len(self.ifc_file.by_type("IfcDistributionFlowElement")))
        # one default styled item
        self.assertEqual(1, len(self.ifc_file.by_type("IfcStyledItem")))

    def test_line_creation_with_height_uncertainties(self):
        self.builder.position_uncertain(Uncertainty.PRECISE).height_position_uncertain(Uncertainty.UNKNOWN).build()
        self.assertEqual(1, len(self.ifc_file.by_type("IfcDistributionFlowElement")))
        # Two pipe segments equals two height uncertainty styled items + the default style
        self.assertEqual(3, len(self.ifc_file.by_type("IfcStyledItem")))

    def test_line_creation_with_position_uncertainties(self):
        self.builder.position_uncertain(Uncertainty.UNKNOWN).height_position_uncertain(Uncertainty.PRECISE).build()
        self.assertEqual(1, len(self.ifc_file.by_type("IfcDistributionFlowElement")))
        # one uncertainty styled item + the default style
        self.assertEqual(2, len(self.ifc_file.by_type("IfcStyledItem")))

    def test_line_creation_with_position_and_height_uncertainties(self):
        self.builder.position_uncertain(Uncertainty.UNKNOWN).height_position_uncertain(Uncertainty.UNKNOWN).build()
        self.assertEqual(1, len(self.ifc_file.by_type("IfcDistributionFlowElement")))
        # Two pipe segments, two height uncertainty styled items + one position uncertainty style + the default style
        self.assertEqual(4, len(self.ifc_file.by_type("IfcStyledItem")))


if __name__ == '__main__':
    unittest.main()
