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
colors = {
    'uncertainty_imprecise': (1, 1, 0.88),
    'uncertainty_unknown': (1, 0.88, 0.75),
    'duct_element': (0.88, 0.88, 0.88),
    'pipe_element': (0.0, 0.0, 0.6),
    'special_structure': (0.88, 0.88, 0.88),
}


class Uncertainty(Enum):
    IMPRECISE = 'ungenau'
    PRECISE = 'genau'
    UNKNOWN = 'unbekannt'


def write_ifc_file(ifc_file, file_path):
    ifc_file.write(file_path)
