from itertools import islice

import ifcopenshell

from ifc.IfcDuctElementBuilder import IfcDuctElementBuilder
from ifc.IfcPipeElementBuilder import IfcPipeElementBuilder
from ifc.IfcProjectSetupBuilder import IfcProject, IfcSite
from ifc.IfcPropertySetBuilder import IfcPropertySet
from ifc.IfcSpecialStructureElementBuilder import IfcSpecialStructureElementBuilder
from ifc.IfcUtils import create_zero_placement, relational_aggregates, spatial_relations_of_elements


class IfcCreationController:
    def __init__(self):
        self.file = ifcopenshell.file()
        self.project = IfcProject(self.file, 'Project')
        self.site = IfcSite(self.file, "Site", create_zero_placement(self.file))

    def ifc_base_element_initialization(self):
        relational_aggregates(self.file, self.project.element, self.site.element)

    def build_chamber_ifc_elements(self, dataset):
        chambers = ()
        for key in islice(dataset.keys(), 1, None):
            chamber_element = (
                IfcDuctElementBuilder(self.file, "duct",
                                      self.project.project_contexts).assign_to_ifcFile().element_name(
                    key).coordinates(
                    dataset[key]['geometry']).radius(0.6).build()
            )
            chamber_element.create_element_in_ifc_file()
            property_set_builder = IfcPropertySet(self.file, chamber_element.element, dataset[key]['attributes'])
            property_set_builder.create_property_set_element_relationship()
            chambers += (chamber_element.element,)
        spatial_relations_of_elements(self.file, chambers, self.site)

    def build_pipe_ifc_elements(self, dataset):
        pipes = ()
        for key in islice(dataset.keys(), 1, None):
            pipe_element = (
                IfcPipeElementBuilder(self.file, "pipe", self.project.project_contexts).assign_to_ifcFile().element_name(
                    key).coordinates(
                    dataset[key]['geometry']).radius(0.3).build())
            pipe_element.create_element_in_ifc_file()
            property_set_builder = IfcPropertySet(self.file, pipe_element.element, dataset[key]['attributes'])
            property_set_builder.create_property_set_element_relationship()
            pipes += (pipe_element.element,)
        spatial_relations_of_elements(self.file, pipes, self.site)

    def build_special_structure_ifc_elements(self, dataset):
        specials = ()
        for key in islice(dataset.keys(), 1, None):
            special_element = (
                IfcSpecialStructureElementBuilder(self.file,
                                                  "other_structure", self.project.project_contexts).assign_to_ifcFile().element_name(
                    key).coordinates(
                    dataset[key]['geometry']).build())
            special_element.create_element_in_ifc_file()
            property_set_builder = IfcPropertySet(self.file, special_element.element, dataset[key]['attributes'])
            property_set_builder.create_property_set_element_relationship()
            specials += (special_element.element,)
        spatial_relations_of_elements(self.file, specials, self.site)
