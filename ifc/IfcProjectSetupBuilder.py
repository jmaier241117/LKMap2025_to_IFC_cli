import ifcopenshell

from ifc import IfcUtils


class IfcProject:

    def __init__(self, ifc_file, project_name, reference_null_point):
        self.project_file = ifc_file
        self.project_name = project_name
        self.element = self.project_file.createIfcProject(ifcopenshell.guid.new(), None, project_name, None, None,
                                                          None, None, (IfcUtils.project_model_context,
                                                                       IfcUtils.project_plan_context),
                                                          self._create_unit_assignment())
        projected_crs = self.project_file.createIfcProjectedCRS('EPSG:2056', 'CH1903+ / LV95', 'CH1903Plus_1', None,
                                                                'Swiss', None, self.length_si_unit)
        self.project_file.createIfcMapConversion(IfcUtils.project_model_context, projected_crs,
                                                 reference_null_point[0], reference_null_point[1],
                                                 reference_null_point[2])

    def _create_unit_assignment(self) -> any:
        self.length_si_unit = self.project_file.createIfcSIUnit(None, "LENGTHUNIT", None, IfcUtils.length_unit)
        area_si_unit = self.project_file.createIfcSIUnit(None, "AREAUNIT", None, IfcUtils.area_unit)
        volume_si_unit = self.project_file.createIfcSIUnit(None, "VOLUMEUNIT", None, IfcUtils.volume_unit)
        plane_angle_si_unit = self.project_file.createIfcSIUnit(None, "PLANEANGLEUNIT", None, IfcUtils.plane_angle_unit)
        degree = self.project_file.createIfcConversionBasedUnit(
            self.project_file.createIfcDimensionalExponents(0, 0, 0, 0, 0, 0, 0),
            "PLANEANGLEUNIT", 'degree', self.project_file.createIfcMeasureWithUnit(
                self.project_file.createIfcReal(0.0174532925199433), plane_angle_si_unit))
        return self.project_file.createIfcUnitAssignment((volume_si_unit, self.length_si_unit, degree, area_si_unit))


class IfcSite:
    def __init__(self, ifc_file, element_name, element_placement):
        self.element = ifc_file.createIfcSite(ifcopenshell.guid.new(), None, element_name, None,
                                              None, element_placement)
