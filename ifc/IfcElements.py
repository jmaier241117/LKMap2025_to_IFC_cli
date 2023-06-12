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


class IfcDistributionFlowElementPipe(AbstractIfcElement):
    def __init__(self):
        super().__init__()
        self.shape_rep = None
        self.project_sub_contexts = None
        self.coordinates = None
        self.radius = None

    def create_element_in_ifc_file(self) -> any:
        self.element = self.project_file.createIfcDistributionFlowElement(ifcopenshell.guid.new(), None,
                                                                          self.element_name,
                                                                          None, None, None,
                                                                          self.shape_rep)


class IfcDistributionFlowElementDuct(AbstractIfcElement):
    def __init__(self):
        super().__init__()
        self.shape_rep = None
        self.project_sub_contexts = None
        self.coordinates = None
        self.radius = None

    def create_element_in_ifc_file(self) -> any:
        self.element = self.project_file.createIfcDistributionFlowElement(ifcopenshell.guid.new(), None,
                                                                          self.element_name,
                                                                          None, None, None,
                                                                          self.shape_rep)


class IfcDistributionFlowElementOtherStructure(AbstractIfcElement):
    def __init__(self):
        super().__init__()
        self.shape_rep = None
        self.project_sub_contexts = None
        self.coordinates = None

    def create_element_in_ifc_file(self) -> any:
        self.element = self.project_file.createIfcDistributionFlowElement(ifcopenshell.guid.new(), None,
                                                                          self.element_name,
                                                                          None, None, None,
                                                                          self.shape_rep)
