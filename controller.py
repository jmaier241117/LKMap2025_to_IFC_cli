from itertools import islice

from enhancer.IntelligentDefaults import ColorDefaults
from enhancer.ZeroPointUtils import ZeroPointScaler
from ifc.IfcCreationController import IfcCreationController
from ifc.IfcUtils import write_ifc_file
from model.DataProcessingChain import DataProcessingChain


class Controller:
    def __init__(self, cli_arguments, cli_options):
        self.cli_arguments = cli_arguments
        self.cli_options = cli_options
        self.ifc_controller = IfcCreationController()
        self.ifc_file = self.ifc_controller.file


    def run_conversion(self):
        filter_chain = DataProcessingChain(self.cli_arguments['gpkg'], self.cli_arguments['clipsrc'])
        filtered_dictionaries_tuple = filter_chain.execute_filters()
        self.ifc_controller.ifc_base_element_initialization()
        for filtered_dictionary in filtered_dictionaries_tuple:
            scaler = ZeroPointScaler(filtered_dictionary, self.cli_arguments['clipsrc'])
            if filtered_dictionary['lkobject_type'] == 'lkpunkt':
               # scaled_dictionary = scaler.scale_point_objects()
                self.ifc_controller.build_chamber_ifc_elements(filtered_dictionary)
            if filtered_dictionary['lkobject_type'] == 'lklinie':
               # scaled_dictionary = scaler.scale_line_objects()
               # colored_elements = ColorDefaults(filtered_dictionary).assign_color_to_objects()
                self.ifc_controller.build_pipe_ifc_elements(filtered_dictionary)
            if filtered_dictionary['lkobject_type'] == 'lkflaeche':
             #   scaled_dictionary = scaler.scale_area_objects()
             self.ifc_controller.build_special_structure_ifc_elements(filtered_dictionary)
        write_ifc_file(self.ifc_file, self.cli_options['ifc_file_path'])



