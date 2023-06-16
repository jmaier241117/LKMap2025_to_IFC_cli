from model import GeometryFilter
from model.GeometryFilter import LKObjectTypeFilter, RangeConstraintFilter

# bbox = box(2635955.3, 1256666.5, 2635997.8, 1256709.9)

object_dictionary = LKObjectTypeFilter("Rothenfluh.gpkg", None).execute_filter()
print(object_dictionary)

objects_in_range_dictionary = RangeConstraintFilter(object_dictionary,
                                                    (2635955.3, 1256666.5, 2635997.8, 1256709.9)).execute_filter()

print(objects_in_range_dictionary)
areas_dict = {'type': 'LKFlaeche',
              'features': []}

points_dict = {'type': 'LKPunkt',
               'features': []}

lines_dict = {'type': 'LKLinie',
              'features': [],
              'characteristics': []}

# for index, row in points_constrained.iterrows():
# points_dict_feature = {'object_type': row.objektart,
#                      'obj_id': row.obj_id,
#                      'geometry': row.geometry.__geo_interface__}
#   points_dict['features'].append(points_dict_feature)

# for index, row in lines_constrained.iterrows():
# lines_dict_feature = {'object_type': row.objektart,
#                     'obj_id': row.obj_id,
#                     'geometry': row.geometry.__geo_interface__,
#                     'characteristics': select_eigenschaft_of_line_object(gpkg_connection, "'" + row.obj_id + "'")}
#   lines_dict['features'].append(lines_dict_feature)

# for index, row in areas_constrained.iterrows():
# area_dict_feature = {'object_type': row.objektart, 'obj_id': row.obj_id,
#                     'geometry': row.geometry.__geo_interface__}
#    areas_dict['features'].append(area_dict_feature)

# print(lines_dict)
# select_all_eigenschaften(gpkg_connection)
