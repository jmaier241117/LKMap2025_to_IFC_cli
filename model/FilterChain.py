from itertools import islice

from model.CharacteristicsFilter import CharacteristicsFilter
from model.GeometryFilter import LKObjectTypeFilter, RangeConstraintFilter, GroupingToDictionaryFilter


class FilterChain:
    def __init__(self, geopackage, clipsrc):
        self.geopackage = geopackage
        self.clipsrc = clipsrc
        self.lkobject_types = ('lkflaeche', 'lklinie', 'lkpunkt')
        self.filtered_dictionaries = ()

    def execute_filters(self) -> any:
        lkobjecttype_filter_results = LKObjectTypeFilter(self.geopackage, None).execute_filter()
        range_constraint_filter_results = RangeConstraintFilter(lkobjecttype_filter_results,
                                                                self.clipsrc).execute_filter()
        for lkobject_type in self.lkobject_types:
            grouped_dictionary_filter_result = GroupingToDictionaryFilter(
                range_constraint_filter_results, lkobject_type).execute_filter()
            for key, value in islice(grouped_dictionary_filter_result.items(), 1, None):
                characteristics_dictionary = CharacteristicsFilter(self.geopackage,
                                                                   {'obj_id': key,
                                                                    'lkobject_type': lkobject_type}).execute_filter()
                grouped_dictionary_filter_result[key]['characteristics'] = characteristics_dictionary
            self.filtered_dictionaries += (grouped_dictionary_filter_result,)
        return self.filtered_dictionaries
