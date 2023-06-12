import json
import pprint

import geopandas
from shapely.geometry import box
import geopandas
from shapely.geometry import box

rothenfluh_areas = geopandas.read_file("Rothenfluh.gpkg", layer='lkflaeche')
rothenfluh_lines = geopandas.read_file("Rothenfluh.gpkg", layer='lklinie')
rothenfluh_points = geopandas.read_file("Rothenfluh.gpkg", layer='lkpunkt')

bbox = box(2635955.3, 1256666.5, 2635997.8, 1256709.9)

areas_constrained = rothenfluh_areas.cx[bbox.bounds[0]:bbox.bounds[2], bbox.bounds[1]:bbox.bounds[3]]
lines_constrained = rothenfluh_lines.cx[bbox.bounds[0]:bbox.bounds[2], bbox.bounds[1]:bbox.bounds[3]]
points_constrained = rothenfluh_points.cx[bbox.bounds[0]:bbox.bounds[2], bbox.bounds[1]:bbox.bounds[3]]

filtered_data = data.loc[data['id'].isin(ids)]

areas_constrained.set_index("T_Ili_Tid")
lines_constrained.set_index("T_Ili_Tid")
points_constrained.set_index("T_Ili_Tid")

areas_dict = {'type': 'LKFlaeche',
              'features': []}

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

for index, row in areas_constrained.iterrows():
    area_dict_feature = {'object_type': row.objektart, 'obj_id': row.obj_id,
                         'geometry': row.geometry.__geo_interface__}
    areas_dict['features'].append(area_dict_feature)

pprint.pprint(areas_dict)
