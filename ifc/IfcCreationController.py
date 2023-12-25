from itertools import islice

import ifcopenshell

from ifc import IfcUtils
from ifc.IfcElementBuilders import IfcDuctElementBuilder, IfcPipeElementBuilder, IfcSpecialStructureElementBuilder
from ifc.IfcProjectSetupBuilder import IfcProject, IfcSite
from ifc.IfcPropertySetBuilder import IfcPropertySet
from ifc.IfcUtils import Uncertainty, initialize_styles


class IfcCreationController:
    def __init__(self, reference_null_point, show_height_uncertainty):
        self.ifc_file = ifcopenshell.file(schema="IFC4X3")
        self.project = IfcProject(self.ifc_file, 'Project', reference_null_point)
        self.site = IfcSite(self.ifc_file, "Site", self._create_zero_placement())
        self.show_height_uncertainty = show_height_uncertainty

    def ifc_base_initialization(self):
        self._relational_aggregates(self.project.element, self.site.element)
        initialize_styles(self.ifc_file)

    def build_chamber_ifc_elements(self, dataset):
        chambers = ()
        for key in islice(dataset.keys(), 1, None):
            if dataset[key]['attributes']['CHLKMap_Dimension1']:
                radius = dataset[key]['attributes']['CHLKMap_Dimension1']
                default_dimension_value = False
            else:
                radius = dataset[key]['attributes']['CHLKMap_Dimension_Annahme']
                default_dimension_value = True
            chamber_element = (
                IfcDuctElementBuilder(self.ifc_file).geometric_context(self.project.project_contexts['model_context'])
                .element_name(dataset[key]['attributes']['T_Ili_Tid'])
                .coordinates(dataset[key]['geometry'])
                .radius(radius)
                .position_uncertain(self._check_uncertainty(dataset[key]['attributes']['CHLKMap_Lagebestimmung']),
                                    default_dimension_value)
                .build())
            property_set_builder = IfcPropertySet(self.ifc_file, chamber_element.distribution_flow_element,
                                                  dataset[key]['attributes'])
            property_set_builder.create_property_set_element_relationship()
            chambers += (chamber_element.distribution_flow_element,)
        self._spatial_relations_of_elements(chambers, self.site)

    def build_pipe_ifc_elements(self, dataset):
        pipes = ()
        for key in dataset.keys():
            if dataset[key]['attributes']['CHLKMap_Breite']:
                radius = dataset[key]['attributes']['CHLKMap_Breite']
                default_dimension_value = False
            else:
                radius = dataset[key]['attributes']['CHLKMap_Breite_Annahme']
                default_dimension_value = True
            pipe_element = (
                IfcPipeElementBuilder(self.ifc_file).geometric_context(self.project.project_contexts['model_context'])
                .element_name(dataset[key]['attributes']['T_Ili_Tid'])
                .coordinates(dataset[key]['geometry'])
                .radius(radius)
                .position_uncertain(self._check_uncertainty(dataset[key]['attributes']['CHLKMap_Lagebestimmung']),
                                    default_dimension_value)
                .height_position_uncertain(
                    self._check_uncertainty(dataset[key]['attributes']['CHLKMap_Hoehenbestimmung'])
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
                IfcSpecialStructureElementBuilder(self.ifc_file).geometric_context(
                    self.project.project_contexts['model_context'])
                .element_name(dataset[key]['attributes']['T_Ili_Tid'])
                .coordinates(dataset[key]['geometry'])
                .position_uncertain(self._check_uncertainty(dataset[key]['attributes']['CHLKMap_Lagebestimmung']))
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

    def _check_uncertainty(self, uncertainty_value) -> any:
        if uncertainty_value == Uncertainty.PRECISE.value:
            return Uncertainty.PRECISE
        elif uncertainty_value == Uncertainty.IMPRECISE.value:
            return Uncertainty.IMPRECISE
        else:
            return Uncertainty.UNKNOWN
