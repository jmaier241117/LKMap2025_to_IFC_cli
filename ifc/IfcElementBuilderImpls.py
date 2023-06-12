from ifc.IfcElements import IfcSite, IfcBuilding, IfcBuildingStorey, IfcDistributionFlowElementPipe, \
    IfcDistributionFlowElementDuct, IfcDistributionFlowElementOtherStructure
from ifc.IIfcElementBuilder import IIfcElementBuilder


class IfcSimpleOriginPlacementElementBuilderImpl(IIfcElementBuilder):
    def __init__(self, project_file, element_type):
        self.project_file = project_file
        self.element_type = element_type
        if element_type == 'site':
            self.site = IfcSite()
        elif element_type == 'building':
            self.building = IfcBuilding()
        elif element_type == 'storey':
            self.storey = IfcBuildingStorey()
        else:
            raise Exception()

    def assign_to_ifcFile(self):
        if self.element_type == 'site':
            self.site.project_file = self.project_file
        elif self.element_type == 'building':
            self.building.project_file = self.project_file
        elif self.element_type == 'storey':
            self.storey.project_file = self.project_file
        else:
            raise Exception()
        return self

    def element_name(self, name):
        if self.element_type == 'site':
            self.site.element_name = name
        elif self.element_type == 'building':
            self.building.element_name = name
        elif self.element_type == 'storey':
            self.storey.element_name = name
        else:
            raise Exception()
        return self

    def element_zero_placement(self):
        element_placement = self.project_file.createIfcLocalPlacement(None,
                                                                      self.project_file.createIfcAxis2Placement3D(
                                                                          self.project_file.createIfcCartesianPoint(
                                                                              (0.0, 0.0, 0.0)),
                                                                          self.project_file.createIfcDirection(
                                                                              (0.0, 0.0, 1.0)),
                                                                          self.project_file.createIfcDirection(
                                                                              (1.0, 0.0, 0.0))))
        if self.element_type == 'site':
            self.site.element_placement = element_placement
        elif self.element_type == 'building':
            self.building.element_placement = element_placement
        elif self.element_type == 'storey':
            self.storey.element_placement = element_placement
        else:
            raise Exception()

        return self

    def build(self) -> any:
        if self.element_type == 'site':
            return self.site
        elif self.element_type == 'building':
            return self.building
        elif self.element_type == 'storey':
            return self.storey
        else:
            raise Exception()


class IfcDistributionFlowElementBuilderImpl(IIfcElementBuilder):
    def __init__(self, project_file, element_type):
        self.project_file = project_file
        self.element_type = element_type
        if element_type == 'pipe':
            self.pipe = IfcDistributionFlowElementPipe()
        elif element_type == 'duct':
            self.duct = IfcDistributionFlowElementDuct()
        elif element_type == 'other_structure':
            self.other_structure = IfcDistributionFlowElementOtherStructure()
        else:
            raise Exception()

    def assign_to_ifcFile(self):
        if self.element_type == 'pipe':
            self.pipe.project_file = self.project_file
        elif self.element_type == 'duct':
            self.duct.project_file = self.project_file
        elif self.element_type == 'other_structure':
            self.other_structure.project_file = self.project_file
        else:
            raise Exception()
        return self

    def element_name(self, name):
        if self.element_type == 'pipe':
            self.pipe.element_name = name
        elif self.element_type == 'duct':
            self.duct.element_name = name
        elif self.element_type == 'other_structure':
            self.other_structure.element_name = name
        else:
            raise Exception()
        return self

    def project_sub_contexts(self, sub_contexts):
        if self.element_type == 'pipe':
            self.pipe.project_sub_contexts = sub_contexts
        elif self.element_type == 'duct':
            self.duct.project_sub_contexts = sub_contexts
        elif self.element_type == 'other_structure':
            self.other_structure.project_sub_contexts = sub_contexts
        else:
            raise Exception()
        return self

    def coordinates(self, coordinates):
        if self.element_type == 'pipe':
            self.pipe.coordinates = coordinates
        elif self.element_type == 'duct':
            self.duct.coordinates = coordinates
        elif self.element_type == 'other_structure':
            self.other_structure.coordinates = coordinates
        else:
            raise Exception()
        return self

    def radius(self, radius):
        if self.element_type == 'pipe':
            self.pipe.radius = radius
        elif self.element_type == 'duct':
            self.duct.radius = radius
        else:
            raise Exception()
        return self

    def build(self) -> any:
        if self.element_type == 'pipe':
            cartesian_point_list_2d = self.project_file.createIfcCartesianPointList2D(self.pipe.coordinates)
            poly_indexed_curve = self.project_file.createIfcIndexedPolyCurve(cartesian_point_list_2d)
            swept_disk_solid = self.project_file.createIfcSweptDiskSolidPolygonal(poly_indexed_curve, self.pipe.radius,
                                                                                  self.pipe.radius * 0.75)
            element_color = self.project_file.createIfcColourRgb('color', 0.5, 0.0, 1.0)
            self.build_style_rep(swept_disk_solid, element_color)
            self.pipe.shape_rep = self.build_shape_rep(swept_disk_solid, 'SolidModel',
                                                       self.pipe.project_sub_contexts)

            return self.pipe
        elif self.element_type == 'duct':
            line = self.project_file.createIfcLine(self.project_file.createIfcCartesianPoint(self.duct.coordinates),
                                                   self.project_file.createIfcVector(
                                                       self.project_file.createIfcDirection(
                                                           (0.0, 0.0, 1.0)),
                                                       2.0))
            trimmed_curve = self.project_file.createIfcTrimmedCurve(line,
                                                                    [self.project_file.createIfcParameterValue(0.0)],
                                                                    [self.project_file.createIfcParameterValue(1.25)],
                                                                    True,
                                                                    "PARAMETER")

            composite_curve_segment = self.project_file.createIfcCompositeCurveSegment("CONTINUOUS", True,
                                                                                       trimmed_curve)
            composite_curve = self.project_file.createIfcCompositeCurve([composite_curve_segment], False)

            swept_disk_solid = self.project_file.createIfcSweptDiskSolidPolygonal(composite_curve, self.duct.radius,
                                                                                  self.duct.radius * 0.75)
            element_color = self.project_file.createIfcColourRgb('color', 0.0, 1.0, 0.5)
            self.build_style_rep(swept_disk_solid, element_color)
            self.duct.shape_rep = self.build_shape_rep(swept_disk_solid, 'SolidModel',
                                                       self.duct.project_sub_contexts)
            return self.duct
        elif self.element_type == 'other_structure':
            cartesian_point_list_2d = self.project_file.createIfcCartesianPointList2D(self.other_structure.coordinates)
            poly_indexed_curve = self.project_file.createIfcIndexedPolyCurve(cartesian_point_list_2d)
            arbitrary_closed_profile = self.project_file.createIfcArbitraryClosedProfileDef('AREA', 'area',
                                                                                            poly_indexed_curve)

            direction = self.project_file.createIfcDirection((0.0, 0.0, 1.0))
            extruded_area_solid = self.project_file.createIfcExtrudedAreaSolid(arbitrary_closed_profile, None,
                                                                               direction, 2.0)
            element_color = self.project_file.createIfcColourRgb('color', 1.0, 0.5, 0.0)
            self.build_style_rep(extruded_area_solid, element_color)
            self.other_structure.shape_rep = self.build_shape_rep(extruded_area_solid, 'SweptSolid',
                                                                  self.other_structure.project_sub_contexts)
            return self.other_structure
        else:
            raise Exception()

    def build_shape_rep(self, representation_element, representation_type, project_sub_contexts) -> any:

        shape_rep = self.project_file.createIfcShapeRepresentation(project_sub_contexts['body_subcontext'],
                                                                   'Body', representation_type,
                                                                   [representation_element])
        bounding_box_of_element = self.project_file.createIfcBoundingBox(
            self.project_file.createIfcCartesianPoint((0.0, 0.0, 0.0)), 2, 2, 50)
        bounding_box_shape_rep = self.project_file.createIfcShapeRepresentation(
            project_sub_contexts['box_subcontext'], 'Box', 'BoundingBox', [bounding_box_of_element])
        return self.project_file.createIfcProductDefinitionShape(None, None, (bounding_box_shape_rep,
                                                                              shape_rep))

    def build_style_rep(self, representation_element, element_color):
        surface_style_rendering = self.project_file.createIfcSurfaceStyleRendering(element_color, 0.0,  # transparency
                                                                                   None, None, None, None, None, None,
                                                                                   'NOTDEFINED')
        surface_style = self.project_file.createIfcSurfaceStyle("style", 'BOTH', [surface_style_rendering])
        self.project_file.createIfcStyledItem(representation_element, [surface_style])
