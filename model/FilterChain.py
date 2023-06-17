from itertools import islice

from model.CharacteristicsFilter import CharacteristicsFilter
from model.GeometryFilter import LKObjectTypeFilter, RangeConstraintFilter, GroupingToDictionaryFilter


class FilterChain:
    def __init__(self, geopackage, filter_attributes):
        self.geopackage = geopackage
        self.filter_attributes = filter_attributes
        self.filtered_dictionaries = []

    def execute_filters(self) -> any:
        lkobjecttype_filter_results = LKObjectTypeFilter(self.geopackage, None).execute_filter()
        range_constraint_filter_results = RangeConstraintFilter(lkobjecttype_filter_results,
                                                                self.filter_attributes['clipsrc']).execute_filter
        print(range_constraint_filter_results)
        for lkobject_type in self.filter_attributes['lkobject_types']:
            grouped_dictionary_filter_result = GroupingToDictionaryFilter(
                range_constraint_filter_results[lkobject_type], lkobject_type).execute_filter()
            for key, value in islice(grouped_dictionary_filter_result.items(), 1, None):
                characteristics_dictionary = CharacteristicsFilter(self.geopackage,
                                                                   {'obj_id': key,
                                                                    'lkobject_type': lkobject_type}).execute_filter()
                grouped_dictionary_filter_result[key]['characteristics'] = characteristics_dictionary
            self.filtered_dictionaries.append(grouped_dictionary_filter_result)
        return self.filtered_dictionaries
