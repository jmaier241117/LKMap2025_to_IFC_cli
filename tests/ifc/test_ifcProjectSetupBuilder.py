import unittest
import ifcopenshell.util.element

from ifc import IfcUtils
from ifc.IfcProjectSetupBuilder import IfcProject, IfcSite


class TestIfcProjectSetupBuilder(unittest.TestCase):
    def setUp(self):
        self.ifc_file = ifcopenshell.file()
        self.zero_placement = self.ifc_file.createIfcLocalPlacement(None,
                                                                    self.ifc_file.createIfcAxis2Placement3D(
                                                                        self.ifc_file.createIfcCartesianPoint(
                                                                            IfcUtils.zero_point_3D),
                                                                        self.ifc_file.createIfcDirection(
                                                                            IfcUtils.zero_point_3D_direction_1),
                                                                        self.ifc_file.createIfcDirection(
                                                                            IfcUtils.zero_point_3D_direction_2)))
        IfcProject(self.ifc_file, 'Project', (20, 10, 3))

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
