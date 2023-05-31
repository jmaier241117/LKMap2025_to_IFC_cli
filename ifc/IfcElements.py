from abc import ABC, abstractmethod

import ifcopenshell.guid


class AbstractIfcElement(ABC):

    def __init__(self):
        self.project_file = None
        self.element_name = None
        self.element_placement = None
        self.element = None

    @abstractmethod
    def create_element_in_ifc_file(self):
        pass


class IfcSite(AbstractIfcElement):

    def create_element_in_ifc_file(self) -> any:
        self.element = self.project_file.createIfcSite(ifcopenshell.guid.new(), None, self.element_name, None,
                                                       None, self.element_placement)


class IfcBuilding(AbstractIfcElement):

    def create_element_in_ifc_file(self) -> any:
        self.element = self.project_file.createIfcBuilding(ifcopenshell.guid.new(), None, self.element_name, None,
                                                           None, self.element_placement)


class IfcBuildingStorey(AbstractIfcElement):

    def create_element_in_ifc_file(self) -> any:
        self.element = self.project_file.createIfcBuildingStorey(ifcopenshell.guid.new(), None, self.element_name, None,
                                                                 None, self.element_placement)


class IfcBuildingElementProxyPipe(AbstractIfcElement):
    def __init__(self):
        super().__init__()
        self.shape_rep = None
        self.project_sub_contexts = None
        self.coordinates = None
        self.length = None
        self.radius = None

    def create_element_in_ifc_file(self) -> any:
        self.element = self.project_file.createIfcBuildingElementProxy(ifcopenshell.guid.new(), None, self.element_name,
                                                                       None, None, None,
                                                                       self.shape_rep, None,
                                                                       "ELEMENT")


class IfcBuildingElementProxyDuct(AbstractIfcElement):
    def __init__(self):
        super().__init__()
        self.shape_rep = None
        self.project_sub_contexts = None
        self.coordinates = None
        self.radius = None

    def create_element_in_ifc_file(self) -> any:
        self.element = self.project_file.createIfcBuildingElementProxy(ifcopenshell.guid.new(), None, self.element_name,
                                                                       None, None, None,
                                                                       self.shape_rep
                                                                       , None,
                                                                       "ELEMENT")


class IfcDistributionChamberElement:
    def __init__(self, project_file, element_name, project_subcontexts, coord_x, coord_y, element_type):
        self.project_file = project_file
        self.element_name = element_name
        self.project_subcontexts = project_subcontexts
        self.coord_x = coord_x
        self.coord_y = coord_y
        self.element_type = element_type
