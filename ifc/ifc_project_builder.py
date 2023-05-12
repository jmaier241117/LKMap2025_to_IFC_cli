import ifcopenshell.guid
import config
from ifcopenshell import file


class IfcProjectBuilder:

    def __init__(self, project_file, project_name):
        self.project_file = project_file
        self.project_name = project_name
        self.project_zero_points = {
            '3D': self.project_file.createIfcAxis2Placement3D(
                project_file.createIfcCartesianPoint(config.zero_point_3D),
                project_file.createIfcDirection(
                    config.zero_point_3D_direction_1),
                project_file.createIfcDirection(
                    config.zero_point_3D_direction_2)),
            '2D': project_file.createIfcAxis2Placement2D(
                project_file.createIfcCartesianPoint(config.zero_point_2D),
                project_file.createIfcDirection(
                    config.zero_point_2D_direction))}
        self.project_contexts = create_contexts(self.project_file, self.project_zero_points)
        self.unit_assignment = create_unit_assignment(self.project_file)
        self.ifc_project = create_ifc_project(self.project_file, self.project_name, self.project_contexts)


def create_ifc_project(project_file: file, project_name: str, contexts: any) -> any:
    return project_file.createIfcProject(ifcopenshell.guid.new(), None, project_name, None, None, None, None,
                                         (contexts['model_context'], contexts['plan_context']),
                                         create_unit_assignment(project_file))


def create_contexts(project_file: file, zero_points: any) -> any:
    contexts = {
        'model_context': project_file.createIfcGeometricRepresentationContext(None, config.context_type_model, 3,
                                                                              0.01,
                                                                              zero_points['3D'], None),
        'plan_context': project_file.createIfcGeometricRepresentationContext(None, config.context_type_plan, 2,
                                                                             0.01,
                                                                             zero_points['2D'], None)}
    subcontexts = {
        'body_subcontext': project_file.createIfcGeometricRepresentationSubContext(config.context_identifier_body,
                                                                                   config.context_type_model, None,
                                                                                   None, None, None,
                                                                                   contexts['model_context'], None,
                                                                                   "MODEL_VIEW", None),
        'box_subcontext': project_file.createIfcGeometricRepresentationSubContext(config.context_identifier_box,
                                                                                  config.context_type_model, None,
                                                                                  None, None, None,
                                                                                  contexts['model_context'], None,
                                                                                  "MODEL_VIEW", None)}
    return {'contextsList': contexts, 'subcontextList': subcontexts}


def create_unit_assignment(project_file: file) -> any:
    length_si_unit = project_file.createIfcSIUnit(None, "LENGTHUNIT", None, config.length_unit)
    area_si_unit = project_file.createIfcSIUnit(None, "AREAUNIT", None, config.area_unit)
    volume_si_unit = project_file.createIfcSIUnit(None, "VOLUMEUNIT", None, config.volume_unit)
    plane_angle_si_unit = project_file.createIfcSIUnit(None, "PLANEANGLEUNIT", None, config.plane_angle_unit)
    degree = project_file.createIfcConversionBasedUnit(
        project_file.createIfcDimensionalExponents(0, 0, 0, 0, 0, 0, 0),
        "PLANEANGLEUNIT", 'degree', project_file.createIfcMeasureWithUnit(
            project_file.createIfcReal(0.0174532925199433), plane_angle_si_unit))
    return project_file.createIfcUnitAssignment((volume_si_unit, length_si_unit, degree, area_si_unit))
