import pprint

import geopandas
from shapely.geometry import box

rothenfluh_areas = geopandas.read_file("Rothenfluh.gpkg", layer='lkflaeche')
rothenfluh_lines = geopandas.read_file("Rothenfluh.gpkg", layer='lklinie')
rothenfluh_points = geopandas.read_file("Rothenfluh.gpkg", layer='lkpunkt')

bbox = box(2635955.3, 1256666.5, 2635997.8, 1256709.9)

areas_constrained = rothenfluh_areas.cx[bbox.bounds[0]:bbox.bounds[2], bbox.bounds[1]:bbox.bounds[3]]
lines_constrained = rothenfluh_lines.cx[bbox.bounds[0]:bbox.bounds[2], bbox.bounds[1]:bbox.bounds[3]]
points_constrained = rothenfluh_points.cx[bbox.bounds[0]:bbox.bounds[2], bbox.bounds[1]:bbox.bounds[3]]
