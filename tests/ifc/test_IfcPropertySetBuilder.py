import unittest
import ifcopenshell.util.element

from ifc.IfcPropertySetBuilder import IfcPropertySet


class TestIfcPropertySetBuilder(unittest.TestCase):
    def setUp(self):
        self.file = ifcopenshell.file()
        self.element = self.file.createIfcDistributionFlowElement(ifcopenshell.guid.new(), None, 'Duct')
        self.attributes = {'Objektart': 'Abwasser.Normschacht.Kontroll_Einsteigschacht',
                           'Lagebestimmung': 'unbekannt',
                           'Letzte_Aenderung': '2023-09-12',
                           'Eigentuemer': 'Verband Schweizer Abwasser- und Gewässerschutzfachleute',
                           'Hoehenbestimmung': None,
                           'Dimension1': 800,
                           'Dimension2': 800,
                           'Dimension_Annahme': 600.0,
                           'Status': 'in_Betrieb'}

    def test_build_chamber_ifc_elements(self):
        IfcPropertySet(self.file, self.element, self.attributes)
        self.assertEqual(len(self.file.by_type("IfcPropertySingleValue")), 9)
        self.assertEqual(len(self.file.by_type("IfcPropertySet")), 1)


if __name__ == '__main__':
    unittest.main()
