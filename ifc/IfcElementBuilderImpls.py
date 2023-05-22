from ifc.IfcElements import IfcSite, IfcBuilding, IfcBuildingStorey, IfcBuildingElementProxyDuct, \
    IfcBuildingElementProxyPipe
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


class IfcBuildingElementProxyBuilderImpl(IIfcElementBuilder):
    def __init__(self, project_file, element_type):
        self.project_file = project_file
        self.element_type = element_type
        if element_type == 'pipe':
            self.pipe = IfcBuildingElementProxyPipe()
        elif element_type == 'duct':
            self.duct = IfcBuildingElementProxyDuct()
        else:
            raise Exception()

    def assign_to_ifcFile(self):
        if self.element_type == 'pipe':
            self.pipe.project_file = self.project_file
        elif self.element_type == 'duct':
            self.duct.project_file = self.project_file
        else:
            raise Exception()
        return self

    def element_name(self, name):
        if self.element_type == 'pipe':
            self.pipe.element_name = name
        elif self.element_type == 'duct':
            self.duct.element_name = name
        else:
            raise Exception()
        return self

    def project_sub_contexts(self, sub_contexts):
        if self.element_type == 'pipe':
            self.pipe.project_sub_contexts = sub_contexts
        elif self.element_type == 'duct':
            self.duct.project_sub_contexts = sub_contexts
        else:
            raise Exception()
        return self

    def coordinates(self, coordinates):
        if self.element_type == 'pipe':
            self.pipe.coordinates = coordinates
        elif self.element_type == 'duct':
            self.duct.coordinates = coordinates
        else:
            raise Exception()
        return self

    def length(self, length):
        if self.element_type == 'pipe':
            self.pipe.length = length
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
            line = self.project_file.createIfcLine(self.project_file.createIfcCartesianPoint(
                (self.pipe.coordinates['coord_x'], self.pipe.coordinates['coord_y'], 0.0)),
                self.project_file.createIfcVector(
                    self.project_file.createIfcDirection(
                        (self.pipe.coordinates['vector_x'],
                         self.pipe.coordinates['vector_y'], 0.0)),
                    self.pipe.length['length']))
            self.pipe.shape_rep = self.build_shape_rep(self.build_curve(line), self.pipe.radius,
                                                       self.pipe.project_sub_contexts)
            return self.pipe
        elif self.element_type == 'duct':
            line = self.project_file.createIfcLine(self.project_file.createIfcCartesianPoint(
                (self.duct.coordinates['coord_x'], self.duct.coordinates['coord_y'], 0.0)),
                self.project_file.createIfcVector(
                    self.project_file.createIfcDirection((0.0, 0.0, 1.0)), 2.0))
            self.duct.shape_rep = self.build_shape_rep(self.build_curve(line), self.duct.radius,
                                                       self.duct.project_sub_contexts)
            return self.duct
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

    def build_shape_rep(self, composite_curve, radius, project_sub_contexts) -> any:

        swept_disk_solid = self.project_file.createIfcSweptDiskSolid(composite_curve, radius)

        shape_rep = self.project_file.createIfcShapeRepresentation(project_sub_contexts['body_subcontext'],
                                                                   'Body', 'SolidModel', [swept_disk_solid])
        bounding_box_of_element = self.project_file.createIfcBoundingBox(
            self.project_file.createIfcCartesianPoint((0.0, 0.0, 0.0)), 2, 2, 50)
        bounding_box_shape_rep = self.project_file.createIfcShapeRepresentation(
            project_sub_contexts['box_subcontext'], 'Box', 'BoundingBox', [bounding_box_of_element])
        return self.project_file.createIfcProductDefinitionShape(None, None, (bounding_box_shape_rep,
                                                                              shape_rep))
