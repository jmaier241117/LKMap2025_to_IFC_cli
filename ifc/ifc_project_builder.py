import string

import ifcopenshell.guid
import config
from ifcopenshell import file


def create_project_setup(ifc_file: file, projectName: string):
    project = ifc_file.createIfcProject(ifcopenshell.guid.new(), None, projectName, None, None, None, None,
                                        (model_context, plan_context), unit_assignment)


def create_3d_and_2d_zero_point(ifc_file: file) -> any:
    zero_points = {'3D': ifc_file.createIfcAxis2Placement3D(ifc_file.createIfcCartesianPoint(config.zero_point_3D),
                                                            ifc_file.createIfcDirection(
                                                                config.zero_point_3D_direction_1),
                                                            ifc_file.createIfcDirection(
                                                                config.zero_point_3D_direction_2)),
                   '2D': ifc_file.createIfcAxis2Placement2D(ifc_file.createIfcCartesianPoint(config.zero_point_2D),
                                                            ifc_file.createIfcDirection(
                                                                config.zero_point_2D_direction))}
    return zero_points


def create_contexts(ifc_file: file) -> any:
    zero_points = create_3d_and_2d_zero_point(ifc_file)
    contexts = {
        'model_context': ifc_file.createIfcGeometricRepresentationContext(None, config.context_type_model, 3, 0.01,
                                                                          zero_points['3D'], None),
        'plan_context': ifc_file.createIfcGeometricRepresentationContext(None, config.context_type_plan, 2, 0.01,
                                                                         zero_points['2D'], None)}

    subcontexts = {
        'body_subcontext': ifc_file.createIfcGeometricRepresentationSubContext(config.context_identifier_body,
                                                                               config.context_type_model, None,
                                                                               None, None, None,
                                                                               contexts['model_context'], None,
                                                                               "MODEL_VIEW", None),
        'box_subcontext': ifc_file.createIfcGeometricRepresentationSubContext(config.context_identifier_box,
                                                                              config.context_type_model, None,
                                                                              None, None, None,
                                                                              contexts['model_context'], None,
                                                                              "MODEL_VIEW", None)}
    return {'contextsList': contexts, 'subcontextList': subcontexts}


def create_unit_assignment(ifc_file: file) -> any():
    length_si_unit = ifc_file.createIfcSIUnit(None, "LENGTHUNIT", None, config.length_unit)
    area_si_unit = ifc_file.createIfcSIUnit(None, "AREAUNIT", None, config.area_unit)
    volume_si_unit = ifc_file.createIfcSIUnit(None, "VOLUMEUNIT", None, config.volume_unit)
    plane_angle_si_unit = ifc_file.createIfcSIUnit(None, "PLANEANGLEUNIT", None, config.plane_angle_unit)
    degree = ifc_file.createIfcConversionBasedUnit(
        ifc_file.createIfcDimensionalExponents(0, 0, 0, 0, 0, 0, 0),
        "PLANEANGLEUNIT", 'degree', ifc_file.createIfcMeasureWithUnit(
            ifc_file.createIfcReal(0.0174532925199433), plane_angle_si_unit))
    return ifc_file.createIfcUnitAssignment((volume_si_unit, length_si_unit, degree, area_si_unit))
