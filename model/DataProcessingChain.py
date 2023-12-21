import os

from model.GeoPackageUtils import convert_ili_2_gpkg, cleanUp_db
from model.GeometryProcessor import GeometryProcessor
from model.GroupingToDictionaryProcessor import GroupingToDictionaryProcessor
from model.TapPointProcessor import TapPointProcessor
from model.CoordinateAdapter import CoordinateAdapter


class DataProcessingChain:
    def __init__(self, cli_arguments, clipsrc):
        self.datafile = cli_arguments['xtf']
        self.reference_null_point = cli_arguments['reference_null_point']
        self.clipsrc = clipsrc
        self.filtered_dictionaries = ()

    def execute_filters(self) -> any:
        convert_ili_2_gpkg(self.datafile)
        geopackage = "GeoPackage.gpkg"
        if os.path.isfile(geopackage):
            geom_processor = GeometryProcessor(geopackage, self.clipsrc)
            tapping_points_processor = TapPointProcessor(geopackage)
            coordinate_adapter = CoordinateAdapter(self.reference_null_point)
            lkobject_geometries = geom_processor.execute_processor()
            line_object_type = 'lklinie'
            line_tapping_points = tapping_points_processor.execute_processor(line_object_type)
            lines_dictionary = coordinate_adapter.execute_line_coordinate_adapter(
                lkobject_geometries[line_object_type],
                line_tapping_points)
            group_lines = GroupingToDictionaryProcessor(geopackage)
            final_lines = group_lines.execute_processor(line_object_type, lines_dictionary)
            self.filtered_dictionaries += (final_lines,)

            point_object_type = 'lkpunkt'
            point_tapping_points = tapping_points_processor.execute_processor(point_object_type)
            point_dictionary = coordinate_adapter.execute_point_coordinate_adapter(
                lkobject_geometries[point_object_type],
                point_tapping_points)
            group_points = GroupingToDictionaryProcessor(geopackage)
            final_points = group_points.execute_processor(point_object_type, point_dictionary)
            self.filtered_dictionaries += (final_points,)

            area_object_type = 'lkflaeche'
            area_tapping_points = tapping_points_processor.execute_processor(area_object_type)
            area_dictionary = coordinate_adapter.execute_area_coordinate_adapter(
                lkobject_geometries[area_object_type],
                area_tapping_points)
            group_areas = GroupingToDictionaryProcessor(geopackage)
            final_areas = group_areas.execute_processor(area_object_type, area_dictionary)
            self.filtered_dictionaries += (final_areas,)
            print(self.filtered_dictionaries)
            cleanUp_db(geopackage)
        return self.filtered_dictionaries
