import math
from enum import Enum

import ifcopenshell
import ifcopenshell.guid
from scipy import stats

zero_point_3D = (0.0, 0.0, 0.0)
zero_point_3D_direction_1 = (0.0, 0.0, 1.0)
zero_point_3D_direction_2 = (1.0, 0.0, 0.0)
zero_point_2D = (0.0, 0.0)
zero_point_2D_direction = (1.0, 0.0)
length_unit = "METRE"
area_unit = "SQUARE_METRE"
volume_unit = "CUBIC_METRE"
plane_angle_unit = "RADIAN"
context_type_model = 'Model'
context_type_plan = 'Plan'
uncertainty_surcharge = {
    'IMPRECISE': 0.3,
    'UNKNOWN': 0.6,
    'PRECISE': 0.0,
    'DEFAULT_IMPRECISE': 0.6,
    'DEFAULT_UNKNOWN': 0.9,
    'DEFAULT_PRECISE': 0.3
}

default_surface_style = None
surface_style_imprecise = None
surface_style_unknown = None
surface_style_unknown_height = None


class Uncertainty(Enum):
    IMPRECISE = 'ungenau'
    PRECISE = 'genau'
    UNKNOWN = 'unbekannt'


def initialize_styles(ifc_file):
    default_element_color = ifc_file.createIfcColourRgb('color', 0.88, 0.88, 0.88)
    surface_style_rendering = ifc_file.createIfcSurfaceStyleShading(default_element_color, 0.0)
    global default_surface_style
    default_surface_style = ifc_file.createIfcSurfaceStyle("style", 'BOTH', [surface_style_rendering])
    imprecise_color = ifc_file.createIfcColourRgb('color', 1.0, 1.0, 0.88)
    surface_style_rendering_imprecise = ifc_file.createIfcSurfaceStyleShading(imprecise_color, 0.70)
    global surface_style_imprecise
    surface_style_imprecise = ifc_file.createIfcSurfaceStyle("style", 'BOTH',
                                                             [surface_style_rendering_imprecise])
    unknown_color = ifc_file.createIfcColourRgb('color', 1.0, 0.82, 0.72)
    surface_style_rendering_unknown = ifc_file.createIfcSurfaceStyleShading(unknown_color, 0.75)
    global surface_style_unknown
    surface_style_unknown = ifc_file.createIfcSurfaceStyle("style", 'BOTH',
                                                           [surface_style_rendering_unknown])
    height_unknown_color = ifc_file.createIfcColourRgb('color', 1.0, 0.75, 0.79)
    surface_style_rendering_height_unknown = ifc_file.createIfcSurfaceStyleShading(height_unknown_color, 0.80)
    global surface_style_unknown_height
    surface_style_unknown_height = ifc_file.createIfcSurfaceStyle("style", 'BOTH',
                                                                  [surface_style_rendering_height_unknown])


def write_ifc_file(ifc_file, file_path):
    ifc_file.write(file_path)


def get_height_uncertainty_coordinates(point1, point2, radius) -> any:
    x_values = [point1[0], point2[0]]
    y_values = [point1[1], point2[1]]
    print(x_values)
    slope, intercept, r_value, p_value, std_err = stats.linregress(x_values, y_values)
    dy = math.sqrt(radius ** 2 / (slope ** 2 + 1))
    dx = -slope * dy
    new_point1 = (float(round(point1[0] + dx, 4)), round(point1[1] + dy, 4), point1[2])
    new_point2 = (float(round(point1[0] - dx, 4)), round(point1[1] - dy, 4), point1[2])
    new_point3 = (float(round(point2[0] + dx, 4)), round(point2[1] + dy, 4), point2[2])
    new_point4 = (float(round(point2[0] - dx, 4)), round(point2[1] - dy, 4), point2[2])
    return new_point1, new_point3, new_point4, new_point2, new_point1
