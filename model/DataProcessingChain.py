import os

from model.GeoPackageUtils import convert_ili_2_gpkg, cleanUp_geopackage
from model.GeometryProcessor import GeometryProcessor
from model.GroupingToDictionaryProcessor import GroupingToDictionaryProcessor
from model.TapPointProcessor import TapPointProcessor
from model.CoordinateAdapter import CoordinateAdapter


class DataProcessingChain:
    def __init__(self, cli_arguments, clipsrc):
        self.datafile = cli_arguments['xtf']
        self.reference_null_point = cli_arguments['reference_null_point']
        self.clipsrc = clipsrc
        self.filtered_dictionaries = {}
        self.geopackage = "GeoPackage.gpkg"
        self.lkobject_types = ('lklinie', 'lkpunkt', 'lkflaeche')
        self.geometry_processor = GeometryProcessor(self.geopackage, self.clipsrc)
        self.coordinate_adapter = CoordinateAdapter(self.reference_null_point)
        self.tapping_points_processor = TapPointProcessor(self.geopackage)
        self.to_dictionary_processor = GroupingToDictionaryProcessor(self.geopackage)

    def execute_processing_chain(self) -> any:
        convert_ili_2_gpkg(self.datafile)
        if os.path.isfile(self.geopackage):
            lkobject_geometries = self.geometry_processor.execute_processor()
            for lkobject_type in self.lkobject_types:
                tapping_points = self.tapping_points_processor.execute_processor(lkobject_type)
                adapted_dictionary = self.coordinate_adapter.execute_processor(lkobject_type,
                                                                               lkobject_geometries[lkobject_type],
                                                                               tapping_points)
                final_dictionary = self.to_dictionary_processor.execute_processor(lkobject_type, adapted_dictionary)
                self.filtered_dictionaries[lkobject_type] = final_dictionary
            cleanUp_geopackage(self.geopackage)
        return self.filtered_dictionaries

