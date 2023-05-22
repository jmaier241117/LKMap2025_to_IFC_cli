import ifcopenshell.guid
from ifcopenshell import file

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
context_identifier_body = 'Body'
context_identifier_box = 'Box'


class IfcProject:

    def __init__(self, project_file, project_name):
        self.project_file = project_file
        self.project_name = project_name
        self.project_zero_points = {
            '3D': project_file.createIfcAxis2Placement3D(
                project_file.createIfcCartesianPoint(zero_point_3D),
                project_file.createIfcDirection(
                    zero_point_3D_direction_1),
                project_file.createIfcDirection(
                    zero_point_3D_direction_2)),
            '2D': project_file.createIfcAxis2Placement2D(
                project_file.createIfcCartesianPoint(zero_point_2D),
                project_file.createIfcDirection(
                    zero_point_2D_direction))}
        self.project_contexts = {
            'model_context': project_file.createIfcGeometricRepresentationContext(None, context_type_model, 3,
                                                                                  0.01,
                                                                                  self.project_zero_points['3D'], None),
            'plan_context': project_file.createIfcGeometricRepresentationContext(None, context_type_plan, 2,
                                                                                 0.01,
                                                                                 self.project_zero_points['2D'], None)}
        self.project_sub_contexts = {
            'body_subcontext': project_file.createIfcGeometricRepresentationSubContext(context_identifier_body,
                                                                                       context_type_model, None,
                                                                                       None, None, None,
                                                                                       self.project_contexts[
                                                                                           'model_context'], None,
                                                                                       "MODEL_VIEW", None),
            'box_subcontext': project_file.createIfcGeometricRepresentationSubContext(context_identifier_box,
                                                                                      context_type_model, None,
                                                                                      None, None, None,
                                                                                      self.project_contexts[
                                                                                          'model_context'], None,
                                                                                      "MODEL_VIEW", None)}
        self.unit_assignment = create_unit_assignment(project_file)
        self.ifc_project = project_file.createIfcProject(ifcopenshell.guid.new(), None, project_name, None, None, None,
                                                         None,
                                                         (self.project_contexts['model_context'],
                                                          self.project_contexts['plan_context']),
                                                         create_unit_assignment(project_file))
        self.project_zero_placement = project_file.createIfcLocalPlacement(None, self.project_zero_points['3D'])


def create_unit_assignment(project_file: file) -> any:
    length_si_unit = project_file.createIfcSIUnit(None, "LENGTHUNIT", None, length_unit)
    area_si_unit = project_file.createIfcSIUnit(None, "AREAUNIT", None, area_unit)
    volume_si_unit = project_file.createIfcSIUnit(None, "VOLUMEUNIT", None, volume_unit)
    plane_angle_si_unit = project_file.createIfcSIUnit(None, "PLANEANGLEUNIT", None, plane_angle_unit)
    degree = project_file.createIfcConversionBasedUnit(
        project_file.createIfcDimensionalExponents(0, 0, 0, 0, 0, 0, 0),
        "PLANEANGLEUNIT", 'degree', project_file.createIfcMeasureWithUnit(
            project_file.createIfcReal(0.0174532925199433), plane_angle_si_unit))
    return project_file.createIfcUnitAssignment((volume_si_unit, length_si_unit, degree, area_si_unit))
