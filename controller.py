from ifc.IfcCreationController import IfcCreationController
from ifc.IfcUtils import write_ifc_file
from model.DataProcessingChain import DataProcessingChain


class Controller:
    def __init__(self, cli_arguments, cli_options):
        self.cli_arguments = cli_arguments
        self.cli_options = cli_options
        self.ifc_creation_controller = IfcCreationController(cli_arguments['reference_null_point'])
        self.ifc_file = self.ifc_creation_controller.ifc_file

    def run_conversion(self):
        filter_chain = DataProcessingChain(self.cli_arguments, self.cli_options['clipsrc'])
        filtered_dictionaries_tuple = filter_chain.execute_filters()
        print(filtered_dictionaries_tuple)
        self.ifc_creation_controller.ifc_base_initialization()
        for filtered_dictionary in filtered_dictionaries_tuple:
            if filtered_dictionary['lkobject_type'] == 'lkpunkt':
                self.ifc_creation_controller.build_chamber_ifc_elements(filtered_dictionary)
            if filtered_dictionary['lkobject_type'] == 'lklinie':
                # colored_elements = ColorDefaults(filtered_dictionary).assign_color_to_objects()
                self.ifc_creation_controller.build_pipe_ifc_elements(filtered_dictionary)
            if filtered_dictionary['lkobject_type'] == 'lkflaeche':
                self.ifc_creation_controller.build_special_structure_ifc_elements(filtered_dictionary)
        write_ifc_file(self.ifc_file, self.cli_options['ifc_file_path'])


