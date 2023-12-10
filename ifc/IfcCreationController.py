from itertools import islice

import ifcopenshell

from ifc import IfcUtils
from ifc.IfcElementBuilders import IfcDuctElementBuilder, IfcPipeElementBuilder, IfcSpecialStructureElementBuilder
from ifc.IfcProjectSetupBuilder import IfcProject, IfcSite
from ifc.IfcPropertySetBuilder import IfcPropertySet


class IfcCreationController:
    def __init__(self, reference_null_point):
        self.ifc_file = ifcopenshell.file(schema="IFC4X3")
        self.project = IfcProject(self.ifc_file, 'Project', reference_null_point)
        self.site = IfcSite(self.ifc_file, "Site", self._create_zero_placement())

    def ifc_base_element_initialization(self):
        self._relational_aggregates(self.project.element, self.site.element)

    def build_chamber_ifc_elements(self, dataset):
        chambers = ()
        for key in islice(dataset.keys(), 1, None):
            chamber_element = (
                IfcDuctElementBuilder(self.ifc_file).geometric_context(self.project.project_contexts['model_context'])
                .element_name(key)
                .coordinates(dataset[key]['geometry'])
                .position_uncertain(True)
                .radius(0.6)
                .build())
            property_set_builder = IfcPropertySet(self.ifc_file, chamber_element.distribution_flow_element,
                                                  dataset[key]['attributes'])
            property_set_builder.create_property_set_element_relationship()
            chambers += (chamber_element.distribution_flow_element,)
        self._spatial_relations_of_elements(chambers, self.site)

    def build_pipe_ifc_elements(self, dataset):
        pipes = ()
        for key in islice(dataset.keys(), 1, None):
            pipe_element = (
                IfcPipeElementBuilder(self.ifc_file).geometric_context(self.project.project_contexts['model_context'])
                .element_name(key)
                .coordinates(dataset[key]['geometry'])
                .position_uncertain(self._check_uncertainty(dataset[key]['attributes']['CHLKMap_Lagebestimmung']))
                .radius(0.3)
                .build())
            property_set_builder = IfcPropertySet(self.ifc_file, pipe_element.distribution_flow_element,
                                                  dataset[key]['attributes'])
            property_set_builder.create_property_set_element_relationship()
            pipes += (pipe_element.distribution_flow_element,)
        self._spatial_relations_of_elements(pipes, self.site)

    def build_special_structure_ifc_elements(self, dataset):
        specials = ()
        for key in islice(dataset.keys(), 1, None):
            special_element = (
                IfcSpecialStructureElementBuilder(self.ifc_file).geometric_context(
                    self.project.project_contexts['model_context'])
                .element_name(key)
                .coordinates(dataset[key]['geometry'])
                .position_uncertain(True)
                .thickness(2)
                .build())
            property_set_builder = IfcPropertySet(self.ifc_file, special_element.distribution_flow_element,
                                                  dataset[key]['attributes'])
            property_set_builder.create_property_set_element_relationship()
            specials += (special_element.distribution_flow_element,)
        self._spatial_relations_of_elements(specials, self.site)

    def _create_zero_placement(self):
        return self.ifc_file.createIfcLocalPlacement(None,
                                                     self.ifc_file.createIfcAxis2Placement3D(
                                                         self.ifc_file.createIfcCartesianPoint(
                                                             IfcUtils.zero_point_3D),
                                                         self.ifc_file.createIfcDirection(
                                                             IfcUtils.zero_point_3D_direction_1),
                                                         self.ifc_file.createIfcDirection(
                                                             IfcUtils.zero_point_3D_direction_2)))

    def _relational_aggregates(self, from_element, to_element):
        self.ifc_file.createIfcRelAggregates(ifcopenshell.guid.new(), None, None, None, from_element, [to_element])

    def _spatial_relations_of_elements(self, elements, spatial_endpoint):
        self.ifc_file.createIfcRelContainedInSpatialStructure(ifcopenshell.guid.new(), None, None, None, elements,
                                                              spatial_endpoint.element)

    def _check_uncertainty(self, uncertainty_value) -> bool:
        if uncertainty_value == "unbekannt":
            return True
        else:
            return False