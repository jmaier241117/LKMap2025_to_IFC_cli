from enum import Enum

import click
import shapely
from shapely import GEOSException


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


(
    SUCCESS,
    CONFIG_ERROR,
    XTF_ERROR,
    IFC_ERROR,
) = range(4)
