from itertools import islice

import ifcopenshell

from ifc import IfcUtils
from ifc.IfcElementBuilders import IfcDuctElementBuilder, IfcPipeElementBuilder, IfcSpecialStructureElementBuilder
from ifc.IfcProjectSetupBuilder import IfcProject, IfcSite
from ifc.IfcPropertySetBuilder import IfcPropertySet
from ifc.IfcUtils import Uncertainty, initialize_styles, initialize_zero_points, initialize_directions, \
    initialize_contexts


class IfcCreationController:
    def __init__(self, reference_null_point, show_height_uncertainty, show_position_uncertainty):
        self.ifc_file = ifcopenshell.file(schema="IFC4X3")
        self.project = None
        self.site = None
        self.show_height_uncertainty = show_height_uncertainty
        self.show_position_uncertainty = show_position_uncertainty
        self.reference_null_point = reference_null_point

    def ifc_base_initialization(self):
        initialize_zero_points(self.ifc_file)
        initialize_directions(self.ifc_file)
        initialize_contexts(self.ifc_file)
        initialize_styles(self.ifc_file)
        self.project = IfcProject(self.ifc_file, 'Project', self.reference_null_point)
        self.site = IfcSite(self.ifc_file, "Site", self._create_zero_placement())
        self._relational_aggregates(self.project.element, self.site.element)

    def build_chamber_ifc_elements(self, dataset):
        chambers = ()
        for key in islice(dataset.keys(), 1, None):
            if dataset[key]['attributes']['Dimension1']:
                radius = dataset[key]['attributes']['Dimension1']
                default_dimension_value = False
            else:
                radius = dataset[key]['attributes']['Dimension_Annahme']
                default_dimension_value = True
            chamber_element = (
                IfcDuctElementBuilder(self.ifc_file)
                .element_name(dataset[key]['attributes']['T_Ili_Tid'])
                .coordinates(dataset[key]['geometry'])
                .radius(radius)
                .position_uncertain(self._check_uncertainty(dataset[key]['attributes']['Lagebestimmung'])
                                    if self.show_position_uncertainty else Uncertainty.PRECISE,
                                    default_dimension_value)
                .height_position_uncertain(
                    self._check_uncertainty(dataset[key]['attributes']['Hoehenbestimmung'])
                    if self.show_height_uncertainty else Uncertainty.PRECISE)
                .build())
            property_set_builder = IfcPropertySet(self.ifc_file, chamber_element.distribution_flow_element,
                                                  dataset[key]['attributes'])
            property_set_builder.create_property_set_element_relationship()
            chambers += (chamber_element.distribution_flow_element,)
        self._spatial_relations_of_elements(chambers, self.site)

    def build_pipe_ifc_elements(self, dataset):
        pipes = ()
        for key in dataset.keys():
            if dataset[key]['attributes']['Breite']:
                radius = dataset[key]['attributes']['Breite']
                default_dimension_value = False
            else:
                radius = dataset[key]['attributes']['Breite_Annahme']
                default_dimension_value = True
            pipe_element = (
                IfcPipeElementBuilder(self.ifc_file)
                .element_name(dataset[key]['attributes']['T_Ili_Tid'])
                .coordinates(dataset[key]['geometry'])
                .radius(radius)
                .position_uncertain(self._check_uncertainty(dataset[key]['attributes']['Lagebestimmung'])
                                    if self.show_position_uncertainty else Uncertainty.PRECISE,
                                    default_dimension_value)
                .height_position_uncertain(
                    self._check_uncertainty(dataset[key]['attributes']['Hoehenbestimmung'])
                    if self.show_height_uncertainty else Uncertainty.PRECISE)
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
                IfcSpecialStructureElementBuilder(self.ifc_file)
                .element_name(dataset[key]['attributes']['T_Ili_Tid'])
                .coordinates(dataset[key]['geometry'])
                .position_uncertain(self._check_uncertainty(dataset[key]['attributes']['Lagebestimmung'])
                                    if self.show_position_uncertainty else Uncertainty.PRECISE)
                .height_position_uncertain(
                    self._check_uncertainty(dataset[key]['attributes']['Hoehenbestimmung'])
                    if self.show_height_uncertainty else Uncertainty.PRECISE)
                .thickness(dataset[key]['thickness'])
                .build())
            property_set_builder = IfcPropertySet(self.ifc_file, special_element.distribution_flow_element,
                                                  dataset[key]['attributes'])
            property_set_builder.create_property_set_element_relationship()
            specials += (special_element.distribution_flow_element,)
        self._spatial_relations_of_elements(specials, self.site)

    def _create_zero_placement(self):
        return self.ifc_file.createIfcLocalPlacement(None, IfcUtils.axis_2_placement_3d)

    def _relational_aggregates(self, from_element, to_element):
        self.ifc_file.createIfcRelAggregates(ifcopenshell.guid.new(), None, None, None, from_element, [to_element])

    def _spatial_relations_of_elements(self, elements, spatial_endpoint):
        self.ifc_file.createIfcRelContainedInSpatialStructure(ifcopenshell.guid.new(), None, None, None, elements,
                                                              spatial_endpoint.element)

    def _check_uncertainty(self, uncertainty_value) -> any:
        if uncertainty_value == Uncertainty.PRECISE.value:
            return Uncertainty.PRECISE
        elif uncertainty_value == Uncertainty.IMPRECISE.value:
            return Uncertainty.IMPRECISE
        else:
            return Uncertainty.UNKNOWN
