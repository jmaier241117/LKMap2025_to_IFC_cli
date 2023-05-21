from ifc.IfcElements import IfcSite, IfcBuilding, IfcBuildingStorey, IfcBuildingElementProxyDuct, \
    IfcBuildingElementProxyPipe
from ifc.IIfcElementBuilder import IIfcElementBuilder


class IfcSimpleOriginPlacementElementBuilderImpl(IIfcElementBuilder):
    def __init__(self):
        self.element_name = None
        self.project_file = None

    def assign_to_ifcFile(self, project_file):
        self.project_file = project_file
        return self

    def element_name(self, name):
        self.element_name = name
        return self

    def element_zero_placement(self):
        self.project_file.createIfcLocalPlacement(None,
                                                  self.project_file.createIfcAxis2Placement3D(
                                                      self.project_file.createIfcCartesianPoint(
                                                          (0.0, 0.0, 0.0)),
                                                      self.project_file.createIfcDirection(
                                                          (0.0, 0.0, 1.0)),
                                                      self.project_file.createIfcDirection(
                                                          (1.0, 0.0, 0.0))))
        return self

    def build(self, element_type) -> any:
        if element_type == 'site':
            return IfcSite(self.project_file, self.element_name, self.element_zero_placement())
            pass
        elif element_type == 'building':
            return IfcBuilding(self.project_file, self.element_name, self.element_zero_placement())
            pass
        elif element_type == 'storey':
            return IfcBuildingStorey(self.project_file, self.element_name, self.element_zero_placement())
            pass
        else:
            raise Exception()


class IfcBuildingElementProxyBuilderImpl(IIfcElementBuilder):
    def __init__(self):
        self.coordinates = None
        self.element_length = None
        self.element_radius = None
        self.project_sub_contexts = None
        self.element_name = None
        self.project_file = None

    def assign_to_ifcFile(self, project_file):
        self.project_file = project_file
        return self

    def element_name(self, name):
        self.element_name = name
        return self

    def project_sub_contexts(self, sub_contexts):
        self.project_sub_contexts = sub_contexts
        return self

    def coordinates(self, coordinates):
        self.coordinates = coordinates
        return self

    def element_length(self, length):
        self.element_length = length
        return self

    def element_radius(self, radius):
        self.element_radius = radius
        return self

    def build(self, element_type) -> any:
        if element_type == 'pipe':
            line = self.project_file.createIfcLine(self.project_file.createIfcCartesianPoint(
                (self.coordinates['coord_x'], self.coordinates['coord_y'], 0.0)),
                self.project_file.createIfcVector(
                    self.project_file.createIfcDirection(
                        (self.coordinates['vector_x'],
                         self.coordinates['vector_y'], 0.0)),
                    self.element_length))
            shape_rep = self.build_shape_rep(self.build_curve(line))
            return IfcBuildingElementProxyPipe(self.project_file, self.element_name, shape_rep)
            pass
        elif element_type == 'duct':
            line = self.project_file.createIfcLine(self.project_file.createIfcCartesianPoint(
                (self.coordinates['coord_x'], self.coordinates['coord_y'], 0.0)),
                self.project_file.createIfcVector(
                    self.project_file.createIfcDirection((0.0, 0.0, 1.0)), 2.0))
            shape_rep = self.build_shape_rep(self.build_curve(line))
            return IfcBuildingElementProxyDuct(self.project_file, self.element_name, shape_rep)
            pass
        else:
            raise Exception()

    def build_curve(self, line) -> any:
        trimmed_curve = self.project_file.createIfcTrimmedCurve(line,
                                                                [self.project_file.createIfcParameterValue(0.0)],
                                                                [self.project_file.createIfcParameterValue(1.25)],
                                                                True, "PARAMETER")
        composite_curve_segment = self.project_file.createIfcCompositeCurveSegment("CONTINUOUS", True,
                                                                                   trimmed_curve)
        return self.project_file.createIfcCompositeCurve([composite_curve_segment], False)

    def build_shape_rep(self, composite_curve) -> any:
        swept_disk_solid = self.project_file.createIfcSweptDiskSolid(composite_curve, self.element_radius)
        shape_rep = self.project_file.createIfcShapeRepresentation(self.project_sub_contexts['body_subcontext'],
                                                                   'Body', 'SolidModel', [swept_disk_solid])
        bounding_box_of_element = self.project_file.createIfcBoundingBox(
            self.project_file.createIfcCartesianPoint((0.0, 0.0, 0.0)),
            self.element_radius * 2, self.element_radius * 2, 50)
        bounding_box_shape_rep = self.project_file.createIfcShapeRepresentation(
            self.project_sub_contexts['box_subcontext'], 'Box', 'BoundingBox', [bounding_box_of_element])
        return self.project_file.createIfcProductDefinitionShape(None, None, (bounding_box_shape_rep,
                                                                              shape_rep))
