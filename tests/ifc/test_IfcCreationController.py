import unittest
import ifcopenshell.util.element

from ifc.IfcCreationController import IfcCreationController

controller = IfcCreationController()

class TestIfcCreationControllerPoints(unittest.TestCase):
    def setUp(self):
        self.dataset = ({'lkobject_type': 'lkpunkt', 'ch211v63WS000004': {
            'attributes': {'CHLKMap_Objektart': 'Abwasser.Normschacht.Kontroll_Einsteigschacht',
                           'CHLKMap_Lagebestimmung': 'unbekannt', 'CHLKMap_Letzte_Aenderung': '2023-09-12',
                           'CHLKMap_Eigentuemer': 'Verband Schweizer Abwasser- und Gewässerschutzfachleute',
                           'CHLKMap_Hoehenbestimmung': None, 'CHLKMap_Status': 'in_Betrieb',
                           'CHLKMap_Dimension1': '600', 'CHLKMap_Dimension2': '800',
                           'CHLKMap_Dimension_Annahme': '600', 'CHLKMap_SymbolOri': '0.0'},
            'geometry': (2704394.757, 1231182.229), 'characteristics': {}}})
        controller.ifc_base_element_initialization()

    def test_build_chamber_ifc_elements(self):
        controller.build_chamber_ifc_elements(self.dataset)
        ducts = controller.file.by_type("IfcDistributionFlowElement")
        self.assertEquals(len(ducts), 1)


class TestIfcCreationControllerPipes(unittest.TestCase):
    def setUp(self):
        self.dataset = ({'lkobject_type': 'lklinie', 'ch211v63RE000002':
            {'attributes':
                 {'CHLKMap_Objektart': 'Abwasser.Haltung_Kanal',
                  'CHLKMap_Lagebestimmung': 'unbekannt',
                  'CHLKMap_Letzte_Aenderung': '2023-09-12',
                  'CHLKMap_Eigentuemer': 'Verband Schweizer Abwasser- und Gewässerschutzfachleute',
                  'CHLKMap_Hoehenbestimmung': None,
                  'CHLKMap_Status': 'in_Betrieb',
                  'CHLKMap_Breite': '300',
                  'CHLKMap_Breite_Annahme': None,
                  'CHLKMap_Profiltyp': 'Kreisprofil'},
             'geometry': ((2704377.024, 1231204.022), (2704394.757, 1231182.229)), 'characteristics': {}}}
        )
        controller.ifc_base_element_initialization()

    def test_build_pipe_ifc_elements(self):
        controller.build_pipe_ifc_elements(self.dataset)
        pipes = controller.file.by_type("IfcDistributionFlowElement")
        self.assertEquals(len(pipes), 2)


class TestIfcCreationControllerAreas(unittest.TestCase):
    def setUp(self):
        self.dataset = ({'lkobject_type': 'lkflaeche', 'ch211v63WS000002':
            {'attributes':
                 {'CHLKMap_Objektart': 'Abwasser.Normschacht.Kontroll_Einsteigschacht',
                  'CHLKMap_Lagebestimmung': 'unbekannt',
                  'CHLKMap_Letzte_Aenderung': '2023-09-12',
                  'CHLKMap_Eigentuemer': 'Verband Schweizer Abwasser- und Gewässerschutzfachleute',
                  'CHLKMap_Hoehenbestimmung': None,
                  'CHLKMap_Status': 'in_Betrieb'},
             'geometry': ((2704373.884, 1231209.472), (2704372.423, 1231199.535), (2704385.575, 1231200.12),
                          (2704383.529, 1231209.472), (2704373.884, 1231209.472)), 'characteristics': {}}}
        )
        controller.ifc_base_element_initialization()

    def test_build_special_structure_ifc_elements(self):
        controller.build_special_structure_ifc_elements(self.dataset)
        special_structures = controller.file.by_type("IfcDistributionFlowElement")
        self.assertEquals(len(special_structures), 3)
        controller.file.write("export/test_ifcCreationController.ifc")


if __name__ == '__main__':
    unittest.main()

