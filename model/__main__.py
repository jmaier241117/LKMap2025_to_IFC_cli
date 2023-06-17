from model import GeometryFilter
from model.CharacteristicsFilter import CharacteristicsFilter
from model.GeometryFilter import LKObjectTypeFilter, RangeConstraintFilter, GroupingToDictionaryFilter
from itertools import islice

# bbox = box(2635955.3, 1256666.5, 2635997.8, 1256709.9)

object_dictionary = LKObjectTypeFilter("Rothenfluh.gpkg", None).execute_filter()
print(object_dictionary['area_objects'])

objects_in_range_dictionary = RangeConstraintFilter(object_dictionary,
                                                    (2635955.3, 1256666.5, 2635997.8, 1256709.9)).execute_filter()

print(objects_in_range_dictionary['lkflaeche'])

dictionary = GroupingToDictionaryFilter(objects_in_range_dictionary, 'lkflaeche').execute_filter()

print(dictionary)

# Loop through the dictionary starting from the second element
for key, value in islice(dictionary.items(), 1, None):
    characteristics_dictionary = CharacteristicsFilter("Rothenfluh.gpkg",
                                                       {'obj_id': key, 'lkobject_type': 'lkflaeche'}).execute_filter()
    dictionary[key]['characteristics'] = characteristics_dictionary

print(dictionary)
