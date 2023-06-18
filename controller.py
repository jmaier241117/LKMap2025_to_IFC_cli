from itertools import islice

from enhancer.ZeroPointUtils import ZeroPointScaler
from ifc.IfcFileBuilder import IfcFileUtils, IfcProject
from ifc.IfcElementBuilderImpls import IfcSimpleOriginPlacementElementBuilderImpl, IfcDistributionFlowElementBuilderImpl
from model.FilterChain import FilterChain


class Controller:
    def __init__(self, cli_arguments, cli_options):
        self.cli_arguments = cli_arguments
        self.cli_options = cli_options
        self.ifc_file_utils = IfcFileUtils(self.cli_options['ifc_file_name'])
        self.ifc_file = self.ifc_file_utils.file
        self.ifc_project_utils = IfcProject(self.ifc_file, "project")
        self.ifc_project = self.ifc_project_utils.ifc_project

    def run_conversion(self) -> int:
        self._ifc_initialization()
        filter_chain = FilterChain(self.cli_arguments['gpkg'], self.cli_arguments['clipsrc'])
        filtered_dictionaries_tuple = filter_chain.execute_filters()
        for filtered_dictionary in filtered_dictionaries_tuple:
            scaler = ZeroPointScaler(filtered_dictionary, self.cli_arguments['clipsrc'])
            if filtered_dictionary['lkobject_type'] == 'lkpunkt':
                scaled_dictionary = scaler.scale_point_objects()
                self._build_chamber_ifc_elements(scaled_dictionary, self.storey)
            if filtered_dictionary['lkobject_type'] == 'lklinie':
                scaled_dictionary = scaler.scale_line_and_area_objects()
                self._build_pipe_ifc_elements(scaled_dictionary, self.storey)
        self.ifc_file_utils.write_ifc_file()
        return 0

    def _ifc_initialization(self):
        site = (
            IfcSimpleOriginPlacementElementBuilderImpl(self.ifc_file, "site").assign_to_ifcFile().element_name(
                "Site").element_zero_placement().build())
        site.create_element_in_ifc_file()
        building = (
            IfcSimpleOriginPlacementElementBuilderImpl(self.ifc_file, "building").assign_to_ifcFile().element_name(
                "Building").element_zero_placement().build())

        building.create_element_in_ifc_file()
        self.storey = (
            IfcSimpleOriginPlacementElementBuilderImpl(self.ifc_file, "storey").assign_to_ifcFile().element_name(
                "Ground Floor").element_zero_placement().build())
        self.storey.create_element_in_ifc_file()
        self.ifc_file_utils.relational_aggregates(self.ifc_project, site.element)
        self.ifc_file_utils.relational_aggregates(site.element, building.element)
        self.ifc_file_utils.relational_aggregates(building.element, self.storey.element)

    def _build_chamber_ifc_elements(self, dataset, storey):
        chambers = ()
        for key in islice(dataset.keys(), 1, None):
            chamber_element = (
                IfcDistributionFlowElementBuilderImpl(self.ifc_file,
                                                      "duct").assign_to_ifcFile().element_name(
                    key).element_owner(dataset[key]['object_owner']).element_object_type(
                    dataset[key]['object_type']).project_sub_contexts(
                    self.ifc_project_utils.project_sub_contexts).coordinates(
                    dataset[key]['geometry']).radius(0.6).build()
            )
            chamber_element.create_element_in_ifc_file()
            chambers += (chamber_element.element,)
        self.ifc_file_utils.spatial_relations_of_elements(chambers, storey)

    def _build_pipe_ifc_elements(self, dataset, storey):
        pipes = ()
        for key in islice(dataset.keys(), 1, None):
            pipe_element = (
                IfcDistributionFlowElementBuilderImpl(self.ifc_file, "pipe").assign_to_ifcFile().element_name(
                    key).element_owner(dataset[key]['object_owner']).element_object_type(
                    dataset[key]['object_type']).project_sub_contexts(
                    self.ifc_project_utils.project_sub_contexts).coordinates(
                    dataset[key]['geometry']).radius(0.3).build())
            pipe_element.create_element_in_ifc_file()
            pipes += (pipe_element.element,)
        self.ifc_file_utils.spatial_relations_of_elements(pipes, storey)

    def _build_special_structure_ifc_elements(self, dataset, storey):
        specials = ()
        for key in islice(dataset.keys(), 1, None):
            special_element = (
                IfcDistributionFlowElementBuilderImpl(self.ifc_file,
                                                      "other_structure").assign_to_ifcFile().element_name(
                    key).element_owner(dataset[key]['object_owner']).element_object_type(
                    dataset[key]['object_type']).project_sub_contexts(
                    self.ifc_project_utils.project_sub_contexts).coordinates(
                    dataset[key]['geometry']).build())
            special_element.create_element_in_ifc_file()
            specials += (special_element.element,)
        self.ifc_file_utils.spatial_relations_of_elements(specials, storey)
