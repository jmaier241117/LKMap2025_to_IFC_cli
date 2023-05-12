import string

import ifcopenshell.guid

from ifcopenshell import file


class IfcElementBuilder:
    def __init__(self, project_file, element_name, element_placement):
        self.project_file = project_file
        self.element_name = element_name
        self.element_placement = element_placement

    def create_ifc_local_placement(self, coord_x: float, coord_y: float, coord_z: float, vector_dim_x: float,
                                   vector_dim_y: float, vector_dim_z: float):
        self.project_file.createIfcLocalPlacement(None, self.project_file.createIfcAxis2Placement3D(
            self.project_file.createIfcCartesianPoint((coord_x, coord_y, coord_z)),
            self.project_file.createIfcDirection((vector_dim_x, vector_dim_y, vector_dim_z)),
            self.project_file.createIfcDirection((1.0, 0.0, 0.0))))


class IfcSiteBuilder(IfcElementBuilder):
    def __init__(self, project_file, element_name, element_placement, site_element):
        super().__init__(self, project_file, element_name, element_placement)
        self.site_element = site_element

    def create_ifc_site(self):
        self.site_element = self.project_file.createIfcSite(ifcopenshell.guid.new(), None, self.element_name, None,
                                                            None, self.element_placement)


class IfcBuildingBuilder(IfcElementBuilder):
    def __init__(self, project_file, element_name, element_placement, building_element):
        super().__init__(self, project_file, element_name, element_placement)
        self.building_element = building_element

    def create_ifc_building(self):
        building = self.project_file.createIfcBuilding(ifcopenshell.guid.new(), None, self.element_name, None, None,
                                                       self.element_placement)


class IfcBuildingStoreyBuilder(IfcElementBuilder):
    def __init__(self, project_file, element_name, element_placement, storey_element):
        super().__init__(self, project_file, element_name, element_placement)
        self.storey_element = storey_element

    def create_ifc_building_storey(self):
        self.storey_element = self.project_file.createIfcBuildingStorey(ifcopenshell.guid.new(), None,
                                                                        self.element_name, None, None,
                                                                        self.element_placement)


class IfcElementWithShapeRepBuilder(IfcElementBuilder):
    def __init__(self, project_file, element_name, element_placement, element_shape_rep):
        super().__init__(self, project_file, element_name, element_placement)
        self.element_shape_rep = element_shape_rep


class IfcDistributionChamberElementBuilder(IfcElementWithShapeRepBuilder):
    def __init__(self, project_file, element_name, element_placement, element_shape_rep, distribution_chamber_element):
        super().__init__(self, project_file, element_name, element_placement, element_shape_rep)
        self.distribution_chamber_element = distribution_chamber_element


class IfcPipeSegmentBuilder(IfcElementWithShapeRepBuilder):
    def __init__(self, project_file, element_name, element_placement, pipe_element):
        super().__init__(self, project_file, element_name, element_placement, element_shape_rep)
        self.pipe_element = pipe_element

        def create_dsitribution_chamber_element(self, element_name: str, dimx: float, dimy: float,
                                                product_shape_def: any,
                                                element_type: str) -> any:
            placement = self.project_file.createIfcLocalPlacement(None, self.project_file.createIfcAxis2Placement3D(
                self.project_file.createIfcCartesianPoint((dimx, dimy, 0.0)),
                self.project_file.createIfcDirection((0.0, 0.0, -2.0)),
                self.project_file.createIfcDirection((1.0, 0.0, 0.0))))
            return self.project_file.createIfcDistributionChamberElement(ifcopenshell.guid.new(), None, element_name,
                                                                         None,
                                                                         None, placement, product_shape_def, None,
                                                                         element_type)

    def create_3d_pointlist_for_chamber_element(self) -> any:
        return self.project_file.createIfcCartesianPointList3D(
            ((0.00, 0.60, -2.00), (0.00, 0.60, 2.00),
             (0.42, 0.42, -2.00), (0.42, 0.42, 2.00),
             (0.60, 0.00, -2.00), (0.60, 0.00, 2.00),
             (0.42, -0.42, -2.00), (0.42, -0.42, 2.00),
             (0.00, -0.60, -2.00), (0.00, -0.60, 2.00),
             (-0.42, -0.42, -2.0), (-0.42, -0.42, 2.00),
             (-0.60, 0.00, -2.00), (-0.60, 0.00, 2.00),
             (-0.42, 0.42, -2.00), (-0.42, 0.42, 2.00)))

    def create_pipe_segment_element(self, element_name: str, dimx: float, dimy: float, product_shape_def: any,
                                    element_type: str) -> any:
        placement = self.project_file.createIfcLocalPlacement(None, self.project_file.createIfcAxis2Placement3D(
            self.project_file.createIfcCartesianPoint(
                (dimx, dimy, -2.0)),
            self.project_file.createIfcDirection((dimx, dimy, 0.0)),
            self.project_file.createIfcDirection((0.0, 0.0, -1.0))))
        return self.project_file.createIfcPipeSegment(ifcopenshell.guid.new(), None, element_name, None,
                                                      None, placement, product_shape_def, None, element_type)

    def create_3d_pointlist_for_pipe_element(self, pipe_length: float) -> any:
        return self.project_file.createIfcCartesianPointList3D(((0.00, 0.30, -pipe_length), (0.00, 0.30, pipe_length),
                                                                (0.21, 0.21, -pipe_length), (0.21, 0.21, pipe_length),
                                                                (0.30, 0.00, -pipe_length), (0.30, 0.00, pipe_length),
                                                                (0.21, -0.2, -pipe_length), (0.21, -0.2, pipe_length),
                                                                (0.00, -0.3, -pipe_length), (0.00, -0.3, pipe_length),
                                                                (-0.21, -0.21, -pipe_length),
                                                                (-0.21, -0.21, pipe_length),
                                                                (-0.30, 0.00, -pipe_length), (-0.30, 0.00, pipe_length),
                                                                (-0.21, 0.21, -pipe_length),
                                                                (-0.21, 0.21, pipe_length)))

    def create_polygonal_faceset_tesselation_16face(self, cartesian_point_list_3d: any) -> any:
        polygonalface_list = []
        polygonalface_counter = 1
        while polygonalface_counter < 14:
            parameter_tuple = (
                polygonalface_counter, polygonalface_counter + 1, polygonalface_counter + 3, polygonalface_counter + 2)
            polygonalface_list.append(parameter_tuple)
            polygonalface_counter += 2
        polygonalfaceset_tuple = ()
        for polygonalface_tuples in polygonalface_list:
            polygonalfaceset_tuple += (self.project_file.createIfcIndexedPolygonalFace(polygonalface_tuples),)
            odd_tuple = ()
        for i in range(1, 16, 2):
            odd_tuple += (i,)
        even_tuple = (4, 2)
        for i in range(16, 5, -2):
            even_tuple += (i,)
        polygonalfaceset_tuple += (self.project_file.createIfcIndexedPolygonalFace(even_tuple),)
        polygonalfaceset_tuple += (self.project_file.createIfcIndexedPolygonalFace((15, 16, 2, 1)),)
        polygonalfaceset_tuple += (self.project_file.createIfcIndexedPolygonalFace(odd_tuple),)
        return self.project_file.createIfcPolygonalFaceSet(cartesian_point_list_3d, None, polygonalfaceset_tuple, None)
