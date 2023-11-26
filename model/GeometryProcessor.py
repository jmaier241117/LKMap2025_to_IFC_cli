import geopandas
from shapely import box
from model.IProcessor import IProcessor


class LKObjectTypeProcessor(IProcessor):

    def execute_filter(self) -> any:
        areas = geopandas.read_file(self.dataset, layer='lkflaeche')
        lines = geopandas.read_file(self.dataset, layer='lklinie')
        points = geopandas.read_file(self.dataset, layer='lkpunkt')
        return {
            'area_objects': areas,
            'line_objects': lines,
            'point_objects': points
        }


class RangeConstraintProcessor(IProcessor):
    def execute_filter(self) -> any:
        # Filter Attribute is the given Range in the format of clipsrc[xmin ymin xmax ymax]
        bbox = box(self.filter_attribute[0], self.filter_attribute[1], self.filter_attribute[2],
                   self.filter_attribute[3])
        dataframe_in_range = {
            'lkflaeche': self.dataset['area_objects'].cx[bbox.bounds[0]:bbox.bounds[2],
                         bbox.bounds[1]:bbox.bounds[3]],
            'lklinie': self.dataset['line_objects'].cx[bbox.bounds[0]:bbox.bounds[2],
                       bbox.bounds[1]:bbox.bounds[3]],
            'lkpunkt': self.dataset['point_objects'].cx[bbox.bounds[0]:bbox.bounds[2],
                       bbox.bounds[1]:bbox.bounds[3]]
        }
        return dataframe_in_range

