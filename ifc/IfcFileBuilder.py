import ifcopenshell
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


class IfcFileUtils:
    def __init__(self, file_path):
        self.file = ifcopenshell.file()
        self.file_path = file_path

    def relational_aggregates(self, from_element, to_element):
        self.file.createIfcRelAggregates(ifcopenshell.guid.new(), None, None, None, from_element, [to_element])

    def spatial_relations_of_elements(self, elements, spatial_endpoint):
        self.file.createIfcRelContainedInSpatialStructure(
            ifcopenshell.guid.new(), None,
            None, None,
            elements, spatial_endpoint.element)

    def write_ifc_file(self):
        self.file.write(self.file_path)


class IfcProject:

    def __init__(self, project_file, project_name):
        self.project_file = project_file
        self.project_name = project_name
        self.project_zero_points = {
            '3D': self.project_file.createIfcAxis2Placement3D(
                self.project_file.createIfcCartesianPoint(zero_point_3D),
                self.project_file.createIfcDirection(
                    zero_point_3D_direction_1),
                self.project_file.createIfcDirection(
                    zero_point_3D_direction_2)),
            '2D': self.project_file.createIfcAxis2Placement2D(
                self.project_file.createIfcCartesianPoint(zero_point_2D),
                self.project_file.createIfcDirection(
                    zero_point_2D_direction))}
        self.project_contexts = {
            'model_context': self.project_file.createIfcGeometricRepresentationContext(None, context_type_model, 3,
                                                                                       0.01,
                                                                                       self.project_zero_points['3D'],
                                                                                       None),
            'plan_context': self.project_file.createIfcGeometricRepresentationContext(None, context_type_plan, 2,
                                                                                      0.01,
                                                                                      self.project_zero_points['2D'],
                                                                                      None)}
        self.project_sub_contexts = {
            'body_subcontext': self.project_file.createIfcGeometricRepresentationSubContext(context_identifier_body,
                                                                                            context_type_model, None,
                                                                                            None, None, None,
                                                                                            self.project_contexts[
                                                                                                'model_context'], None,
                                                                                            "MODEL_VIEW", None),
            'box_subcontext': self.project_file.createIfcGeometricRepresentationSubContext(context_identifier_box,
                                                                                           context_type_model, None,
                                                                                           None, None, None,
                                                                                           self.project_contexts[
                                                                                               'model_context'], None,
                                                                                           "MODEL_VIEW", None)}
        self.unit_assignment = _create_unit_assignment(self.project_file)
        self.ifc_project = self.project_file.createIfcProject(ifcopenshell.guid.new(), None, project_name, None, None,
                                                              None,
                                                              None,
                                                              (self.project_contexts['model_context'],
                                                               self.project_contexts['plan_context']),
                                                              _create_unit_assignment(project_file))
        self.project_zero_placement = self.project_file.createIfcLocalPlacement(None, self.project_zero_points['3D'])


def _create_unit_assignment(project_file: file) -> any:
    length_si_unit = project_file.createIfcSIUnit(None, "LENGTHUNIT", None, length_unit)
    area_si_unit = project_file.createIfcSIUnit(None, "AREAUNIT", None, area_unit)
    volume_si_unit = project_file.createIfcSIUnit(None, "VOLUMEUNIT", None, volume_unit)
    plane_angle_si_unit = project_file.createIfcSIUnit(None, "PLANEANGLEUNIT", None, plane_angle_unit)
    degree = project_file.createIfcConversionBasedUnit(
        project_file.createIfcDimensionalExponents(0, 0, 0, 0, 0, 0, 0),
        "PLANEANGLEUNIT", 'degree', project_file.createIfcMeasureWithUnit(
            project_file.createIfcReal(0.0174532925199433), plane_angle_si_unit))
    return project_file.createIfcUnitAssignment((volume_si_unit, length_si_unit, degree, area_si_unit))
