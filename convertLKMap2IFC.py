import click
import shapely.wkt
from shapely import GEOSException

from controller import Controller


class PointParamType(click.ParamType):
    name = "WKT POINT"

    def convert(self, value, param, ctx) -> any:
        try:
            point = shapely.wkt.loads(value)
            coords = list(point.coords)
            return coords[0]
        except GEOSException:
            self.fail(f"{value!r} is not a valid WKT Point", param, ctx)

POINT = PointParamType()


class PolygonParamType(click.ParamType):
    name = "WKT POLYGON"

    def convert(self, value, param, ctx) -> any:
        try:
            polygon = shapely.wkt.loads(value)
            coords = list(polygon.exterior.coords)
            bbox_tuple = (min(coords, key=lambda coord: coord[0])[0], min(coords, key=lambda coord: coord[1])[1],
                          max(coords, key=lambda coord: coord[0])[0], max(coords, key=lambda coord: coord[1])[1])
            return bbox_tuple
        except GEOSException:
            self.fail(f"{value!r} is not a valid WKT Polygon", param, ctx)



POLYGON = PolygonParamType()


@click.command()
@click.argument('importfile', type=click.Path(exists=True))
@click.option('--nullpoint', required=True, type=POINT,
              help='The Reference Null Point used for creating the elements, example: \'POINT(2691039.8 1236160.3 420.0)\'')
@click.option('--exportpath', default=None, type=click.Path(exists=False),
              help='The path to where you would like your IFC file to be generated')
@click.option('--clipsrc', default=None, type=POLYGON,
              help='The range for which elements should be included, example: \'POLYGON((69.0 41.0, 69.0 41.4, 69.4 41.4, 69.4 41.0, 69.0 41.0))\'')
def convert(importfile, nullpoint, exportpath, clipsrc):
    """
     IMPORTFILE is the path to the INTERLIS transferfile (.xtf) you would like to use!

     NULLPOINT is the reference null point for all elements, format LV95: x , y, z

     EXPORTFILE is , format: <name>.ifc
    """
    print(nullpoint)
    controller = Controller(
        {'xtf': importfile, 'reference_null_point': nullpoint},
        {'clipsrc': clipsrc, 'ifc_file_path': exportpath})
    #controller.run_conversion()


if __name__ == '__main__':
    convert()
