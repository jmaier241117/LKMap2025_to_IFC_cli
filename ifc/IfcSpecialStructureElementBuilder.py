from ifc.IfcElements import IfcDistributionFlowElement
from ifc.IIfcElementBuilder import IIfcElementBuilder
from ifc.IfcUtils import build_style_rep, build_shape_rep


class IfcSpecialStructureElementBuilder(IIfcElementBuilder):
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

    def build(self) -> any:
        cartesian_point_list_2d = self.project_file.createIfcCartesianPointList2D(self.element.coordinates)
        poly_indexed_curve = self.project_file.createIfcIndexedPolyCurve(cartesian_point_list_2d)
        arbitrary_closed_profile = self.project_file.createIfcArbitraryClosedProfileDef('AREA', 'area',
                                                                                        poly_indexed_curve)

        direction = self.project_file.createIfcDirection((0.0, 0.0, 1.0))
        extruded_area_solid = self.project_file.createIfcExtrudedAreaSolid(arbitrary_closed_profile, None,
                                                                           direction, 2.0)
        element_color = self.project_file.createIfcColourRgb('color', 0.88, 0.88, 0.88)
        build_style_rep(self.project_file, extruded_area_solid, element_color)
        self.element.shape_rep = build_shape_rep(self.project_file, extruded_area_solid, 'SweptSolid',
                                                      self.geometric_context['model_context'])
        return self.element
