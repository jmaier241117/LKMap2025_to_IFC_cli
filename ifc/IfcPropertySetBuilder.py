import ifcopenshell

from ifc import IfcUtils


class IfcPropertySet:
    def __init__(self, ifc_file, element, attributes):
        self.project_file = ifc_file
        self.element = element
        self.attributes = attributes
        self.properties = self._create_properties()
        self.property_set = self._create_property_set()

    def _create_properties(self) -> any:
        properties = ()
        for attribute in self.attributes:
            if self.attributes[attribute] is not None:
                prop = self.project_file.createIfcPropertySingleValue(attribute, None,
                                                                      self.project_file.createIfcLabel(
                                                                          self.attributes[attribute]))
            else:
                prop = self.project_file.createIfcPropertySingleValue(attribute, None,
                                                                      self.project_file.createIfcLabel(""))
            properties += (prop,)
        return properties

    def _create_property_set(self) -> any:
        return self.project_file.createIfcPropertySet(ifcopenshell.guid.new(), None, 'LKMap_Pset', None,
                                                      self.properties)

    def create_property_set_element_relationship(self):
        self.project_file.createIfcRelDefinesByProperties(ifcopenshell.guid.new(), None, 'RelProperties', None,
                                                        [self.element], self.property_set)
