import unittest
import ifcopenshell.util.element

from ifc.IfcPropertySetBuilder import IfcPropertySet


class TestIfcPropertySetBuilder(unittest.TestCase):
    def setUp(self):
        self.file = ifcopenshell.file()
        self.element = self.file.createIfcDistributionFlowElement(ifcopenshell.guid.new(), None, 'Pipe')
        self.attributes = {'CHLKMap_Objektart': 'Abwasser.Normschacht.Kontroll_Einsteigschacht',
                           'CHLKMap_Lagebestimmung': 'unbekannt',
                           'CHLKMap_Letzte_Aenderung': '2023-09-12',
                           'CHLKMap_Eigentuemer': 'Verband Schweizer Abwasser- und Gewässerschutzfachleute',
                           'CHLKMap_Hoehenbestimmung': None,
                           'CHLKMap_Status': 'in_Betrieb'}

    def test_build_chamber_ifc_elements(self):
        IfcPropertySet(self.file, self.element, self.attributes)
        self.assertEquals(len(self.file.by_type("IfcPropertySingleValue")), 6)
        self.assertEquals(len(self.file.by_type("IfcPropertySet")), 1)


if __name__ == '__main__':
    unittest.main()
