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
        # areas
        grouped_area_dictionary_filter_result = GroupingToDictionaryFilter(
            range_constraint_filter_results, 'lkflaeche').execute_filter()
        for key in islice(grouped_area_dictionary_filter_result.keys(), 1, None):
            characteristics_dictionary = CharacteristicsFilter(self.geopackage,
                                                               {'obj_id': key,
                                                                'lkobject_type': 'lkflaeche'}).execute_filter()
            grouped_area_dictionary_filter_result[key]['characteristics'] = characteristics_dictionary
        self.filtered_dictionaries += (grouped_area_dictionary_filter_result,)

        # lines
        grouped_lines_dictionary_filter_result = GroupingToDictionaryFilter(
            range_constraint_filter_results, 'lklinie').execute_filter()
        for key in islice(grouped_lines_dictionary_filter_result.keys(), 1, None):
            characteristics_dictionary = CharacteristicsFilter(self.geopackage,
                                                               {'obj_id': key,
                                                                'lkobject_type': 'lklinie'}).execute_filter()
            grouped_lines_dictionary_filter_result[key]['characteristics'] = characteristics_dictionary
        self.filtered_dictionaries += (grouped_lines_dictionary_filter_result,)

        # points
        grouped_points_dictionary_filter_result = GroupingToDictionaryFilter(
            range_constraint_filter_results, 'lkpunkt').execute_filter()
        for key in islice(grouped_points_dictionary_filter_result.keys(), 1, None):
            characteristics_dictionary = CharacteristicsFilter(self.geopackage,
                                                               {'obj_id': key,
                                                                'lkobject_type': 'lkpunkt'}).execute_filter()
            grouped_points_dictionary_filter_result[key]['characteristics'] = characteristics_dictionary
        self.filtered_dictionaries += (grouped_points_dictionary_filter_result,)

        return self.filtered_dictionaries
