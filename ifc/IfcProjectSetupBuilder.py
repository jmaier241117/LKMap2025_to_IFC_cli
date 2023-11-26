import ifcopenshell

from ifc.IfcElements import AbstractIfcElement

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
        self.unit_assignment = self._create_unit_assignment()
        self.element = self.project_file.createIfcProject(ifcopenshell.guid.new(), None, project_name, None, None,
                                                              None,
                                                              None,
                                                              (self.project_contexts['model_context'],
                                                               self.project_contexts['plan_context']),
                                                              self._create_unit_assignment())
        self.project_zero_placement = self.project_file.createIfcLocalPlacement(None, self.project_zero_points['3D'])

    def _create_unit_assignment(self) -> any:
        length_si_unit = self.project_file.createIfcSIUnit(None, "LENGTHUNIT", None, length_unit)
        area_si_unit = self.project_file.createIfcSIUnit(None, "AREAUNIT", None, area_unit)
        volume_si_unit = self.project_file.createIfcSIUnit(None, "VOLUMEUNIT", None, volume_unit)
        plane_angle_si_unit = self.project_file.createIfcSIUnit(None, "PLANEANGLEUNIT", None, plane_angle_unit)
        degree = self.project_file.createIfcConversionBasedUnit(
            self.project_file.createIfcDimensionalExponents(0, 0, 0, 0, 0, 0, 0),
            "PLANEANGLEUNIT", 'degree', self.project_file.createIfcMeasureWithUnit(
                self.project_file.createIfcReal(0.0174532925199433), plane_angle_si_unit))
        return self.project_file.createIfcUnitAssignment((volume_si_unit, length_si_unit, degree, area_si_unit))


class IfcSite:
    def __init__(self, file, element_name, element_placement):
        self.element = file.createIfcSite(ifcopenshell.guid.new(), None, element_name, None,
                                          None, element_placement)

