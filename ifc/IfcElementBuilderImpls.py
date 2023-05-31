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
            cartesian_point_list_2d = self.project_file.createIfcCartesianPointList2D(self.pipe.coordinates)
            poly_indexed_curve = self.project_file.createIfcIndexedPolyCurve(cartesian_point_list_2d)
            self.pipe.shape_rep = self.build_shape_rep(poly_indexed_curve, self.pipe.radius,
                                                       self.pipe.project_sub_contexts)
            return self.pipe
        elif self.element_type == 'duct':
            cartesian_point_list_2d = self.project_file.createIfcCartesianPointList2D([self.duct.coordinates])
            poly_indexed_curve = self.project_file.createIfcIndexedPolyCurve(cartesian_point_list_2d)
            self.duct.shape_rep = self.build_shape_rep(poly_indexed_curve, self.duct.radius,
                                                       self.duct.project_sub_contexts)
            return self.duct
        else:
            raise Exception()

    def build_shape_rep(self, poly_indexed_curve, radius, project_sub_contexts) -> any:

        swept_disk_solid = self.project_file.createIfcSweptDiskSolidPolygonal(poly_indexed_curve, radius, radius * 0.75)

        shape_rep = self.project_file.createIfcShapeRepresentation(project_sub_contexts['body_subcontext'],
                                                                   'Body', 'SolidModel', [swept_disk_solid])
        bounding_box_of_element = self.project_file.createIfcBoundingBox(
            self.project_file.createIfcCartesianPoint((0.0, 0.0, 0.0)), 2, 2, 50)
        bounding_box_shape_rep = self.project_file.createIfcShapeRepresentation(
            project_sub_contexts['box_subcontext'], 'Box', 'BoundingBox', [bounding_box_of_element])
        return self.project_file.createIfcProductDefinitionShape(None, None, (bounding_box_shape_rep,
                                                                              shape_rep))
