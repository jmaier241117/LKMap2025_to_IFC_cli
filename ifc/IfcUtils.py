import math
from enum import Enum

from scipy import stats

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


class Uncertainty(Enum):
    IMPRECISE = 'ungenau'
    PRECISE = 'genau'
    UNKNOWN = 'unbekannt'


zero_point_3D = None
zero_point_2D = None


def initialize_zero_points(ifc_file):
    global zero_point_3D
    zero_point_3D = ifc_file.createIfcCartesianPoint((0.0, 0.0, 0.0))
    global zero_point_2D
    zero_point_2D = ifc_file.createIfcCartesianPoint((0.0, 0.0))


z_axis_3D_direction = None
x_axis_3D_direction = None
x_axis_2D_direction = None


def initialize_directions(ifc_file):
    global z_axis_3D_direction
    z_axis_3D_direction = ifc_file.createIfcDirection((0.0, 0.0, 1.0))
    global x_axis_3D_direction
    x_axis_3D_direction = ifc_file.createIfcDirection((1.0, 0.0, 0.0))
    global x_axis_2D_direction
    x_axis_2D_direction = ifc_file.createIfcDirection((1.0, 0.0))


default_surface_style = None
surface_style_imprecise = None
surface_style_unknown = None
surface_style_unknown_height = None


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


axis_2_placement_3d = None
project_model_context = None
axis_2_placement_2d = None
project_plan_context = None


def initialize_contexts(ifc_file):
    global axis_2_placement_3d
    axis_2_placement_3d = ifc_file.createIfcAxis2Placement3D(zero_point_3D, z_axis_3D_direction, x_axis_3D_direction)
    global project_model_context
    project_model_context = ifc_file.createIfcGeometricRepresentationContext(None, context_type_model, 3, 0.01,
                                                                             axis_2_placement_3d)
    global axis_2_placement_2d
    axis_2_placement_2d = ifc_file.createIfcAxis2Placement2D(zero_point_2D, x_axis_2D_direction)
    global project_plan_context
    project_plan_context = ifc_file.createIfcGeometricRepresentationContext(None, context_type_plan, 2, 0.01,
                                                                            axis_2_placement_2d)


def write_ifc_file(ifc_file, file_path):
    ifc_file.write(file_path)


def get_height_uncertainty_coordinates(point1, point2, radius) -> any:
    x_values = [point1[0], point2[0]]
    y_values = [point1[1], point2[1]]
    slope, intercept, r_value, p_value, std_err = stats.linregress(x_values, y_values)
    dy = math.sqrt(radius ** 2 / (slope ** 2 + 1))
    dx = -slope * dy
    new_point1 = (float(round(point1[0] + dx, 4)), round(point1[1] + dy, 4), point1[2])
    new_point2 = (float(round(point1[0] - dx, 4)), round(point1[1] - dy, 4), point1[2])
    new_point3 = (float(round(point2[0] + dx, 4)), round(point2[1] + dy, 4), point2[2])
    new_point4 = (float(round(point2[0] - dx, 4)), round(point2[1] - dy, 4), point2[2])
    return new_point1, new_point3, new_point4, new_point2, new_point1
