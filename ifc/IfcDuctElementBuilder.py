from ifc.IfcElements import IfcDistributionFlowElement
from ifc.IIfcElementBuilder import IIfcElementBuilder
from ifc.IfcUtils import build_shape_rep, build_style_rep


class IfcDuctElementBuilder(IIfcElementBuilder):
    def __init__(self, project_file, element_type, geometric_context):
        self.project_file = project_file
        self.element_type = element_type
        self.element = IfcDistributionFlowElement()
        self.color = (0, 0, 0)  # Black
        self.geometric_context = geometric_context

    def assign_to_ifcFile(self):
        self.element.project_file = self.project_file
        return self

    def element_name(self, name):
        self.element.element_name = name
        return self

    def element_color(self, color_tuple):
        self.color = color_tuple
        return self

    def coordinates(self, coordinates):
        self.element.coordinates = coordinates
        return self

    def radius(self, radius):
        self.element.radius = radius
        return self

    def build(self) -> any:
        polyline = self.project_file.createIfcPolyline(
            (self.project_file.createIfcCartesianPoint((0.0, 0.0, 0.0)),
            self.project_file.createIfcCartesianPoint((0.0, 0.0, 2.0))))
        shape_rep1 = self.project_file.createIfcShapeRepresentation(self.geometric_context['model_context'],
                                                                    'Axis', 'Curve3D',
                                                                    [polyline])
        direction = self.project_file.createIfcDirection((0.0, 0.0, 1.0))
        self.element.coordinates += (-2.0,)
        axis_placement = self.project_file.createIfcAxis2Placement3D(
            self.project_file.createIfcCartesianPoint(self.element.coordinates))
        circle_profile_def = self.project_file.createIfcCircleHollowProfileDef('AREA', None, None, 0.6, 0.0125)
        extruded_area_solid = self.project_file.createIfcExtrudedAreaSolid(circle_profile_def, axis_placement,
                                                                           direction, 2.0)
        shape_rep2 = self.project_file.createIfcShapeRepresentation(self.geometric_context['model_context'],
                                                                    'Body', 'SweptSolid',
                                                                    [extruded_area_solid])

        self.element.shape_rep = self.project_file.createIfcProductDefinitionShape(None, None, (shape_rep1, shape_rep2))
        return self.element
