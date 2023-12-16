import ifcopenshell

from ifc.IfcUtils import uncertainty_surcharge, colors


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
        self.representation_elements = {
            'default': None,
            'imprecise': None,
            'unknown': None,
        }
        self.representation_type = None
        self.shape_representation = None
        self.default_dimension_value = None
        self.imprecise_color = self.project_file.createIfcColourRgb('color', colors['uncertainty_imprecise'][0],
                                                                    colors['uncertainty_imprecise'][1],
                                                                    colors['uncertainty_imprecise'][2])
        self.unknown_color = self.project_file.createIfcColourRgb('color', colors['uncertainty_unknown'][0],
                                                                  colors['uncertainty_unknown'][1],
                                                                  colors['uncertainty_unknown'][2])

    def create_element_in_ifc_file(self) -> any:
        self.distribution_flow_element = self.project_file.createIfcDistributionFlowElement(ifcopenshell.guid.new(),
                                                                                            None,
                                                                                            self.element_name,
                                                                                            None, None, None,
                                                                                            self.shape_representation)

    def build_style_representation(self):
        surface_style_rendering = self.project_file.createIfcSurfaceStyleShading(self.element_color, 0.0)
        surface_style = self.project_file.createIfcSurfaceStyle("style", 'BOTH', [surface_style_rendering])
        self.project_file.createIfcStyledItem(self.representation_elements['default'], [surface_style])
        if self.representation_elements['imprecise']:
            surface_style_rendering_imprecise = self.project_file.createIfcSurfaceStyleShading(self.imprecise_color
                                                                                               , 0.75)
            surface_style_imprecise = self.project_file.createIfcSurfaceStyle("style", 'BOTH',
                                                                              [surface_style_rendering_imprecise])
            self.project_file.createIfcStyledItem(self.representation_elements['imprecise'], [surface_style_imprecise])
        elif self.representation_elements['unknown']:
            surface_style_rendering_unknown = self.project_file.createIfcSurfaceStyleShading(self.unknown_color
                                                                                             , 0.75)
            surface_style_unknown = self.project_file.createIfcSurfaceStyle("style", 'BOTH',
                                                                            [surface_style_rendering_unknown])
            self.project_file.createIfcStyledItem(self.representation_elements['unknown'], [surface_style_unknown])

    def build_shape_representation(self) -> any:
        rep_elements_list = list(self.representation_elements.values())
        rep_elements = [element for element in rep_elements_list if element is not None]
        shape_rep = self.project_file.createIfcShapeRepresentation(self.geometric_context,
                                                                   'Body', self.representation_type,
                                                                   rep_elements)
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
        self.element_color = self.project_file.createIfcColourRgb('color', colors['pipe_element'][0],
                                                                  colors['pipe_element'][1], colors['pipe_element'][2])
        self.poly_indexed_curve = None

    def build_representation_element(self):
        cartesian_point_list_3d = self.project_file.createIfcCartesianPointList3D(self.coordinates)
        self.poly_indexed_curve = self.project_file.createIfcIndexedPolyCurve(cartesian_point_list_3d)
        self.representation_elements['default'] = self.project_file.createIfcSweptDiskSolidPolygonal(
            self.poly_indexed_curve,
            self.radius if not self.default_dimension_value else uncertainty_surcharge['DEFAULT_PRECISE'],
            self.radius * 0.75)

    def build_representation_uncertainty_imprecise_element(self):
        uncertainty_addon = uncertainty_surcharge['IMPRECISE'] if not self.default_dimension_value else \
            uncertainty_surcharge['DEFAULT_IMPRECISE']
        self.representation_elements['imprecise'] = self.project_file.createIfcSweptDiskSolidPolygonal(
            self.poly_indexed_curve,
            self.radius + uncertainty_addon,
            self.radius)

    def build_representation_uncertainty_unknown_element(self):
        uncertainty_addon = uncertainty_surcharge['UNKNOWN'] if not self.default_dimension_value else \
            uncertainty_surcharge['DEFAULT_UNKNOWN']
        self.representation_elements['unknown'] = self.project_file.createIfcSweptDiskSolidPolygonal(
            self.poly_indexed_curve,
            self.radius + uncertainty_addon,
            self.radius)


class IfcDuctDistributionFlowElement(IIfcDistributionFlowElement):
    def __init__(self, ifc_file):
        super().__init__(ifc_file)
        self.radius = None
        self.representation_type = 'SolidModel'
        self.element_color = self.project_file.createIfcColourRgb('color', colors['duct_element'][0],
                                                                  colors['duct_element'][1], colors['duct_element'][2])
        self.poly_indexed_curve = None

    def build_representation_element(self):
        cartesian_point_list_3d = self.project_file.createIfcCartesianPointList3D(self.coordinates)
        self.poly_indexed_curve = self.project_file.createIfcIndexedPolyCurve(cartesian_point_list_3d)
        self.representation_elements['default'] = self.project_file.createIfcSweptDiskSolidPolygonal(
            self.poly_indexed_curve,
            self.radius if not self.default_dimension_value else uncertainty_surcharge['DEFAULT_PRECISE'],
            self.radius * 0.75)

    def build_representation_uncertainty_imprecise_element(self):
        uncertainty_addon = uncertainty_surcharge['IMPRECISE'] if not self.default_dimension_value else \
            uncertainty_surcharge['DEFAULT_IMPRECISE']
        self.representation_elements['imprecise'] = self.project_file.createIfcSweptDiskSolidPolygonal(
            self.poly_indexed_curve, self.radius + uncertainty_addon, self.radius)

    def build_representation_uncertainty_unknown_element(self):
        uncertainty_addon = uncertainty_surcharge['UNKNOWN'] if not self.default_dimension_value else \
            uncertainty_surcharge['DEFAULT_UNKNOWN']
        self.representation_elements['unknown'] = self.project_file.createIfcSweptDiskSolidPolygonal(
            self.poly_indexed_curve,
            self.radius + uncertainty_addon,
            self.radius)


class IfcSpecialStructureDistributionFlowElement(IIfcDistributionFlowElement):
    def __init__(self, ifc_file):
        super().__init__(ifc_file)
        self.thickness = None
        self.representation_type = 'SweptSolid'
        self.element_color = self.project_file.createIfcColourRgb('color', colors['special_structure'][0],
                                                                  colors['special_structure'][1],
                                                                  colors['special_structure'][2])
        self.extrusion_direction = None

    def build_representation_element(self):
        cartesian_point_list_3d = self.project_file.createIfcCartesianPointList3D(self.coordinates)
        poly_indexed_curve = self.project_file.createIfcIndexedPolyCurve(cartesian_point_list_3d)
        arbitrary_closed_profile = self.project_file.createIfcArbitraryClosedProfileDef('AREA', 'area',
                                                                                        poly_indexed_curve)
        self.extrusion_direction = self.project_file.createIfcDirection((0.0, 0.0, 1.0))
        self.representation_elements['default'] = self.project_file.createIfcExtrudedAreaSolid(
            arbitrary_closed_profile,
            None,
            self.extrusion_direction,
            self.thickness)

    def build_representation_uncertainty_imprecise_element(self):
        uncertainty_coordinates = []
        for coordinate in self.coordinates:
            uncertainty_tuple = (coordinate[0] + uncertainty_surcharge['IMPRECISE'],
                                 coordinate[1] + uncertainty_surcharge['IMPRECISE'], coordinate[2])
            uncertainty_coordinates.append(uncertainty_tuple)
        cartesian_point_list_3d = self.project_file.createIfcCartesianPointList3D(uncertainty_coordinates)
        poly_indexed_curve = self.project_file.createIfcIndexedPolyCurve(cartesian_point_list_3d)
        arbitrary_closed_profile = self.project_file.createIfcArbitraryClosedProfileDef('AREA', 'area',
                                                                                        poly_indexed_curve)
        self.representation_elements['imprecise'] = self.project_file.createIfcExtrudedAreaSolid(
            arbitrary_closed_profile,
            None,
            self.extrusion_direction,
            self.thickness)

    def build_representation_uncertainty_unknown_element(self):
        uncertainty_coordinates = []
        for coordinate in self.coordinates:
            if not self.default_dimension_value:
                uncertainty_tuple = (coordinate[0] + uncertainty_surcharge['UNKNOWN'],
                                     coordinate[1] + uncertainty_surcharge['UNKNOWN'], coordinate[2])
            else:
                uncertainty_tuple = (coordinate[0] + uncertainty_surcharge['DEFAULT_UNKNOWN'],
                                     coordinate[1] + uncertainty_surcharge['DEFAULT_UNKNOWN'], coordinate[2])
            uncertainty_coordinates.append(uncertainty_tuple)
        cartesian_point_list_3d = self.project_file.createIfcCartesianPointList3D(uncertainty_coordinates)
        poly_indexed_curve = self.project_file.createIfcIndexedPolyCurve(cartesian_point_list_3d)
        arbitrary_closed_profile = self.project_file.createIfcArbitraryClosedProfileDef('AREA', 'area',
                                                                                        poly_indexed_curve)
        self.representation_elements['unknown'] = self.project_file.createIfcExtrudedAreaSolid(
            arbitrary_closed_profile,
            None,
            self.extrusion_direction,
            self.thickness)
