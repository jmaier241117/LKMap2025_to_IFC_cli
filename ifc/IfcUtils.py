from enum import Enum

import ifcopenshell
import ifcopenshell.guid

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
    surface_style_rendering_imprecise = ifc_file.createIfcSurfaceStyleShading(imprecise_color, 0.75)
    global surface_style_imprecise
    surface_style_imprecise = ifc_file.createIfcSurfaceStyle("style", 'BOTH',
                                                             [surface_style_rendering_imprecise])
    unknown_color = ifc_file.createIfcColourRgb('color', 1.0, 0.88, 0.75)
    surface_style_rendering_unknown = ifc_file.createIfcSurfaceStyleShading(unknown_color, 0.75)
    global surface_style_unknown
    surface_style_unknown = ifc_file.createIfcSurfaceStyle("style", 'BOTH',
                                                           [surface_style_rendering_unknown])


def write_ifc_file(ifc_file, file_path):
    ifc_file.write(file_path)
