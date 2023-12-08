import json
from itertools import islice

from model.AttributeProcessor import AttributeProcessor
from model.CharacteristicsFilter import CharacteristicsProcessor
from model.GeometryProcessor import LKObjectTypeProcessor, RangeConstraintProcessor
from model.GroupingToDictionaryProcessor import GroupingToDictionaryProcessor


class DataProcessingChain:
    def __init__(self, geopackage, clipsrc):
        self.geopackage = geopackage
        self.clipsrc = clipsrc
        self.filtered_dictionaries = ()

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
        # areas
        area_dictionary = to_dictionary_processor.execute_processor('lkflaeche')
        area_dictionary_characteristics = self._get_element_characteristics(area_dictionary, 'lkflaeche')
        formatted_json1 = json.dumps(area_dictionary_characteristics, indent=4)
        print(formatted_json1)
        self.filtered_dictionaries += (area_dictionary_characteristics,)

        # lines
        lines_dictionary = to_dictionary_processor.execute_processor('lklinie')
        lines_dictionary_characteristics = self._get_element_characteristics(lines_dictionary, 'lklinie')
        formatted_json2 = json.dumps(lines_dictionary_characteristics, indent=4)
        print(formatted_json2)
        self.filtered_dictionaries += (lines_dictionary_characteristics,)

        # points
        points_dictionary = to_dictionary_processor.execute_processor('lkpunkt')
        points_dictionary_characteristics = self._get_element_characteristics(points_dictionary, 'lkpunkt')
        formatted_json3 = json.dumps(points_dictionary_characteristics, indent=4)
        print(formatted_json3)
        self.filtered_dictionaries += (points_dictionary_characteristics,)

        return self.filtered_dictionaries

    def _get_element_characteristics(self, dictionary, object_type) -> any:
        for key in islice(dictionary.keys(), 1, None):
            characteristics_dictionary = CharacteristicsProcessor(self.geopackage,
                                                                  {'obj_id': key,
                                                                   'lkobject_type': object_type}).execute_filter()
            dictionary[key]['characteristics'] = characteristics_dictionary
        return dictionary
