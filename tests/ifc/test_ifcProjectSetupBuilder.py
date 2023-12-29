import unittest
import ifcopenshell.util.element

from ifc import IfcUtils
from ifc.IfcProjectSetupBuilder import IfcProject, IfcSite
from ifc.IfcUtils import initialize_zero_points, initialize_directions, initialize_contexts


class TestIfcProjectSetupBuilder(unittest.TestCase):
    def setUp(self):
        self.ifc_file = ifcopenshell.file()
        initialize_zero_points(self.ifc_file)
        initialize_directions(self.ifc_file)
        initialize_contexts(self.ifc_file)
        self.project = IfcProject(self.ifc_file, 'Project', (20, 10, 3))

    def test_ifc_si_unit_and_assignment(self):
        self.assertEqual(4, len(self.ifc_file.by_type("IfcSIUnit")))
        self.assertEqual(1, len(self.ifc_file.by_type("IfcUnitAssignment")))

    def test_projected_crs_and_map_conversion(self):
        self.assertEqual(1, len(self.ifc_file.by_type("IfcProjectedCRS")))
        self.assertEqual(1, len(self.ifc_file.by_type("IfcMapConversion")))

    def test_ifc_project(self):
        self.assertEqual(1, len(self.ifc_file.by_type("IfcProject")))

    def test_ifc_site(self):
        IfcSite(self.ifc_file, "Site", self.ifc_file.createIfcLocalPlacement(None, IfcUtils.axis_2_placement_3d))
        self.assertEqual(1, len(self.ifc_file.by_type("IfcSite")))


if __name__ == '__main__':
    unittest.main()
