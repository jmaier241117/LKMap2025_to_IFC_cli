import unittest
import ifcopenshell.util.element

from ifc.IfcProjectSetupBuilder import IfcProject, IfcSite
from ifc.IfcUtils import initialize_zero_points, initialize_directions


class TestIfcProjectSetupBuilder(unittest.TestCase):
    def setUp(self):
        self.ifc_file = ifcopenshell.file()
        initialize_zero_points(self.ifc_file)
        initialize_directions(self.ifc_file)
        self.project = IfcProject(self.ifc_file, 'Project', (20, 10, 3))
        self.zero_placement = self.ifc_file.createIfcLocalPlacement(None, self.project.project_zero_points['3D'])

    def test_geometric_representation_context(self):
        self.assertEquals(2, len(self.ifc_file.by_type("IfcGeometricRepresentationContext")))

    def test_ifc_si_unit_and_assignment(self):
        self.assertEquals(4, len(self.ifc_file.by_type("IfcSIUnit")))
        self.assertEquals(1, len(self.ifc_file.by_type("IfcUnitAssignment")))

    def test_projected_crs_and_map_conversion(self):
        self.assertEquals(1, len(self.ifc_file.by_type("IfcProjectedCRS")))
        self.assertEquals(1, len(self.ifc_file.by_type("IfcMapConversion")))

    def test_ifc_project(self):
        self.assertEquals(1, len(self.ifc_file.by_type("IfcProject")))

    def test_ifc_site(self):
        IfcSite(self.ifc_file, "Site", self.zero_placement)
        self.assertEquals(1, len(self.ifc_file.by_type("IfcSite")))


if __name__ == '__main__':
    unittest.main()
