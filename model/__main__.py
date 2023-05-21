import json
import pprint

import geopandas
from shapely.geometry import box

areas_constrained.set_index("T_Ili_Tid")
lines_constrained.set_index("T_Ili_Tid")
points_constrained.set_index("T_Ili_Tid")

points_dict = {'type': 'LKPunkt',
               'features': []}

lines_dict = {'type': 'LKLinie',
              'features': []}

for index, row in points_constrained.iterrows():
    points_dict_feature = {'object_type': row.objektart,
                           'obj_id': row.obj_id,
                           'geometry': row.geometry.__geo_interface__}
    points_dict['features'].append(points_dict_feature)

for index, row in lines_constrained.iterrows():
    lines_dict_feature = {'object_type': row.objektart, 'obj_id': row.obj_id,
                          'geometry': row.geometry.__geo_interface__}
    lines_dict['features'].append(lines_dict_feature)

pprint.pprint(lines_dict)
