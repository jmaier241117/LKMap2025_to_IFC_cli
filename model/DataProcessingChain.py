import json
from itertools import islice

from model.TapPointProcessor import TapPointProcessor
from model.AttributeProcessor import AttributeProcessor
from model.CharacteristicsFilter import CharacteristicsProcessor
from model.CoordinateAdapter import CoordinateAdapter
from model.GeometryProcessor import LKObjectTypeProcessor, RangeConstraintProcessor
from model.GroupingToDictionaryProcessor import GroupingToDictionaryProcessor


class DataProcessingChain:
    def __init__(self, cli_arguments, clipsrc):
        self.geopackage = cli_arguments['gpkg']
        self.reference_null_point = cli_arguments['reference_null_point']
        self.clipsrc = clipsrc
        self.filtered_dictionaries = ()
        self.tapping_points_processor = TapPointProcessor(self.geopackage)
        self.coordinate_adapter = CoordinateAdapter(self.reference_null_point)

    def execute_filters(self) -> any:
        attribute_processor = AttributeProcessor(self.geopackage)
        attribute_dataset = attribute_processor.execute_processor()
        lkobjecttype_filter_results = LKObjectTypeProcessor(self.geopackage, None).execute_filter()
        if self.clipsrc:
            range_constraint_filter_results = RangeConstraintProcessor(lkobjecttype_filter_results,
                                                                       self.clipsrc).execute_filter()
            to_dictionary_processor = GroupingToDictionaryProcessor(range_constraint_filter_results,
                                                                    attribute_dataset)
        else:
            to_dictionary_processor = GroupingToDictionaryProcessor(lkobjecttype_filter_results,
                                                                    attribute_dataset)

        area_object_type = 'lkflaeche'
        area_dictionary = to_dictionary_processor.execute_processor(area_object_type)
        area_tapping_points = self.tapping_points_processor.execute_processor(area_object_type)
        area_dictionary = self.coordinate_adapter.execute_area_coordinate_adapter(area_dictionary, area_tapping_points)
        area_dictionary_characteristics = self._get_element_characteristics(area_dictionary, area_object_type)
        self.filtered_dictionaries += (area_dictionary_characteristics,)

        # lines
        line_object_type = 'lklinie'
        lines_dictionary = to_dictionary_processor.execute_processor(line_object_type)
        line_tapping_points = self.tapping_points_processor.execute_processor(line_object_type)
        lines_dictionary = self.coordinate_adapter.execute_line_coordinate_adapter(lines_dictionary,
                                                                                   line_tapping_points)
        lines_dictionary_characteristics = self._get_element_characteristics(lines_dictionary, line_object_type)
        self.filtered_dictionaries += (lines_dictionary_characteristics,)

        # points
        point_object_type = 'lkpunkt'
        points_dictionary = to_dictionary_processor.execute_processor(point_object_type)
        point_tapping_points = self.tapping_points_processor.execute_processor(point_object_type)
        points_dictionary = self.coordinate_adapter.execute_point_coordinate_adapter(points_dictionary,
                                                                                     point_tapping_points)
        points_dictionary_characteristics = self._get_element_characteristics(points_dictionary, point_object_type)
        self.filtered_dictionaries += (points_dictionary_characteristics,)

        return self.filtered_dictionaries

    def _get_element_characteristics(self, dictionary, object_type) -> any:
        for key in islice(dictionary.keys(), 1, None):
            characteristics_dictionary = CharacteristicsProcessor(self.geopackage,
                                                                  {'obj_id': key,
                                                                   'lkobject_type': object_type}).execute_filter()
            dictionary[key]['characteristics'] = characteristics_dictionary
        return dictionary
