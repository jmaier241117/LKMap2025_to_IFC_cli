from itertools import islice

from model import AttributeProcessor
from model.CharacteristicsFilter import CharacteristicsProcessor
from model.GeometryProcessor import LKObjectTypeProcessor, RangeConstraintProcessor
from model.GroupingToDictionaryProcessor import GroupingToDictionaryProcessor


class DataProcessingChain:
    def __init__(self, geopackage):
        self.geopackage = geopackage
        #self.clipsrc = clipsrc
        self.lkobject_types = ('lkflaeche', 'lklinie', 'lkpunkt')
        self.filtered_dictionaries = ()

    def execute_filters(self) -> any:
        lkobjecttype_filter_results = LKObjectTypeProcessor(self.geopackage, None).execute_filter()
        #range_constraint_filter_results = RangeConstraintProcessor(lkobjecttype_filter_results,
                                                        #           self.clipsrc).execute_filter()
        attribute_dataset = AttributeProcessor(self.geopackage).execute_processor()
        to_dictionary_processor = GroupingToDictionaryProcessor(lkobjecttype_filter_results,
                                                                         attribute_dataset)
        # areas
        area_dictionary = to_dictionary_processor.execute_lkflaeche_processor()
        for key in islice(area_dictionary.keys(), 1, None):
            characteristics_dictionary = CharacteristicsProcessor(self.geopackage,
                                                                  {'obj_id': key,
                                                                   'lkobject_type': 'lkflaeche'}).execute_filter()
            area_dictionary[key]['characteristics'] = characteristics_dictionary
        self.filtered_dictionaries += (area_dictionary,)

        # lines
        lines_dictionary = to_dictionary_processor.execute_lklinie_processor()
        for key in islice(lines_dictionary.keys(), 1, None):
            characteristics_dictionary = CharacteristicsProcessor(self.geopackage,
                                                                  {'obj_id': key,
                                                                   'lkobject_type': 'lklinie'}).execute_filter()
            lines_dictionary[key]['characteristics'] = characteristics_dictionary
        self.filtered_dictionaries += (lines_dictionary,)

        # points
        points_dictionary = to_dictionary_processor.execute_lkpunkt_processor()
        for key in islice(points_dictionary.keys(), 1, None):
            characteristics_dictionary = CharacteristicsProcessor(self.geopackage,
                                                                  {'obj_id': key,
                                                                   'lkobject_type': 'lkpunkt'}).execute_filter()
            points_dictionary[key]['characteristics'] = characteristics_dictionary
        self.filtered_dictionaries += (points_dictionary,)

        return self.filtered_dictionaries
