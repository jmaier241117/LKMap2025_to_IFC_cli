import ifcopenshell


class IIfcDistributionFlowElement:
    def __init__(self, ifc_file):
        self.project_file = ifc_file
        self.geometric_context = None
        self.distribution_flow_element = None
        self.element_name = None
        self.element_color = (0, 0, 0)  # Black
        self.coordinates = None
        self.position_uncertain = None
        self.height_position_uncertain = None
        self.representation_elements = []
        self.representation_type = None
        self.shape_representation = None

    def create_element_in_ifc_file(self) -> any:
        self.distribution_flow_element = self.project_file.createIfcDistributionFlowElement(ifcopenshell.guid.new(),
                                                                                            None,
                                                                                            self.element_name,
                                                                                            None, None, None,
                                                                                            self.shape_representation)

    def build_style_representation(self):
        surface_style_rendering = self.project_file.createIfcSurfaceStyleShading(self.element_color, 0.0)
        surface_style = self.project_file.createIfcSurfaceStyle("style", 'BOTH', [surface_style_rendering])
        self.project_file.createIfcStyledItem(self.representation_elements[0], [surface_style])
        if self.position_uncertain and len(self.representation_elements) == 2:
            surface_style_rendering_uncertain = self.project_file.createIfcSurfaceStyleShading(
                self.project_file.createIfcColourRgb('color', 1, 1, 0.88), 0.75)
            surface_style_uncertain = self.project_file.createIfcSurfaceStyle("style", 'BOTH',
                                                                              [surface_style_rendering_uncertain])
            self.project_file.createIfcStyledItem(self.representation_elements[1], [surface_style_uncertain])

    def build_shape_representation(self) -> any:
        shape_rep = self.project_file.createIfcShapeRepresentation(self.geometric_context,
                                                                   'Body', self.representation_type,
                                                                   self.representation_elements)
        # Not sure if needed bb
        bounding_box_of_element = self.project_file.createIfcBoundingBox(
            self.project_file.createIfcCartesianPoint((0.0, 0.0, 0.0)), 2, 2, 50)
        bounding_box_shape_rep = self.project_file.createIfcShapeRepresentation(
            self.geometric_context, 'Box', 'BoundingBox', [bounding_box_of_element])
        self.shape_representation = self.project_file.createIfcProductDefinitionShape(None, None,
                                                                                      (bounding_box_shape_rep,
                                                                                       shape_rep))


class IfcPipeDistributionFlowElement(IIfcDistributionFlowElement):
    def __init__(self, ifc_file):
        super().__init__(ifc_file)
        self.radius = None
        self.representation_type = 'SolidModel'
        self.element_color = self.project_file.createIfcColourRgb('color', 0, 0, 0)

    def build_representation_element(self):
        cartesian_point_list_3d = self.project_file.createIfcCartesianPointList3D(self.coordinates)
        poly_indexed_curve = self.project_file.createIfcIndexedPolyCurve(cartesian_point_list_3d)
        self.representation_elements.append(self.project_file.createIfcSweptDiskSolidPolygonal(poly_indexed_curve,
                                                                                               self.radius,
                                                                                               self.radius * 0.75))
        if self.position_uncertain:
            self.representation_elements.append(self.project_file.createIfcSweptDiskSolidPolygonal(poly_indexed_curve,
                                                                                                   self.radius * 1.75,
                                                                                                   self.radius))


class IfcDuctDistributionFlowElement(IIfcDistributionFlowElement):
    def __init__(self, ifc_file):
        super().__init__(ifc_file)
        self.radius = None
        self.representation_type = 'SolidModel'
        self.element_color = self.project_file.createIfcColourRgb('color', 0.88, 0.88, 0.88)

    def build_representation_element(self):
        cartesian_point_list_3d = self.project_file.createIfcCartesianPointList3D(self.coordinates)
        poly_indexed_curve = self.project_file.createIfcIndexedPolyCurve(cartesian_point_list_3d)
        self.representation_elements.append(self.project_file.createIfcSweptDiskSolidPolygonal(poly_indexed_curve,
                                                                                               self.radius,
                                                                                               self.radius * 0.75))
        if self.position_uncertain:
            self.representation_elements.append(self.project_file.createIfcSweptDiskSolidPolygonal(poly_indexed_curve,
                                                                                                   self.radius * 1.75,
                                                                                                   self.radius))


class IfcSpecialStructureDistributionFlowElement(IIfcDistributionFlowElement):
    def __init__(self, ifc_file):
        super().__init__(ifc_file)
        self.thickness = None
        self.representation_type = 'SweptSolid'
        self.element_color = self.project_file.createIfcColourRgb('color', 0.88, 0.88, 0.88)

    def build_representation_element(self):
        cartesian_point_list_3d = self.project_file.createIfcCartesianPointList3D(self.coordinates)
        poly_indexed_curve = self.project_file.createIfcIndexedPolyCurve(cartesian_point_list_3d)
        arbitrary_closed_profile = self.project_file.createIfcArbitraryClosedProfileDef('AREA', 'area',
                                                                                        poly_indexed_curve)
        direction = self.project_file.createIfcDirection((0.0, 0.0, 1.0))
        self.representation_element = self.project_file.createIfcExtrudedAreaSolid(arbitrary_closed_profile, None,
                                                                                   direction, self.thickness)
