import ifcopenshell


class IfcBuildingElementProxy:
    def __init__(self, project_file, project_subcontexts, coordinates_and_length, element_radius):
        # self.placement = project_file.createIfcLocalPlacement(None,
        #                                                      project_file.createIfcAxis2Placement3D(
        #                                                          project_file.createIfcCartesianPoint(
        #                                                              (coordinates_and_length['coord_x'],
        #                                                               coordinates_and_length['coord_y'], -2.0)),
        #                                                          project_file.createIfcDirection(
        #                                                              (0.0, 0.0, 1.0)),
        #                                                          project_file.createIfcDirection(
        #                                                              (1.0, 0.0, 0.0))))
        self.coordinates_and_lengths = coordinates_and_length
        self.line = project_file.createIfcLine(project_file.createIfcCartesianPoint(
            (coordinates_and_length['coord_x'], coordinates_and_length['coord_y'], 0.0)),
            project_file.createIfcVector(
                project_file.createIfcDirection(
                    (coordinates_and_length['vector_x'],
                     coordinates_and_length['vector_y'], 0.0)),
                coordinates_and_length['length']))
        self.trimmed_curve = project_file.createIfcTrimmedCurve(self.line,
                                                                [project_file.createIfcParameterValue(0.0)],
                                                                [project_file.createIfcParameterValue(1.25)],
                                                                True,
                                                                "PARAMETER")
        self.composite_curve_segment = project_file.createIfcCompositeCurveSegment("CONTINUOUS", True,
                                                                                   self.trimmed_curve)
        self.composite_curve = project_file.createIfcCompositeCurve([self.composite_curve_segment], False)
        self.swept_disk_solid = project_file.createIfcSweptDiskSolid(self.composite_curve, element_radius)
        self.shape_rep = project_file.createIfcShapeRepresentation(project_subcontexts['body_subcontext'], 'Body',
                                                                   'SolidModel',
                                                                   [self.swept_disk_solid])
        self.bounding_box_of_element = project_file.createIfcBoundingBox(
            project_file.createIfcCartesianPoint((0.0, 0.0, -2.0)), element_radius * 2,
                                                                    element_radius * 2,
                                                                    coordinates_and_length['length'] * 2)
        self.bounding_box_shape_rep = project_file.createIfcShapeRepresentation(
            project_subcontexts['box_subcontext'],
            'Box', 'BoundingBox',
            [self.bounding_box_of_element])
        self.product_shape_def = project_file.createIfcProductDefinitionShape(None, None,
                                                                              (self.bounding_box_shape_rep,
                                                                               self.shape_rep))
        self.building_proxy_element = project_file.createIfcBuildingElementProxy(ifcopenshell.guid.new(), None, "proxy",
                                                                                 None, None, None,
                                                                                 self.product_shape_def, None,
                                                                                 "ELEMENT")


class IfcBuildingElementProxyCHAMBER:
    def __init__(self, project_file, project_subcontexts, coordinates, element_radius):
        # self.placement = project_file.createIfcLocalPlacement(None,
        #                                                      project_file.createIfcAxis2Placement3D(
        #                                                          project_file.createIfcCartesianPoint(
        #                                                              (coordinates_and_length['coord_x'],
        #                                                               coordinates_and_length['coord_y'], -2.0)),
        #                                                          project_file.createIfcDirection(
        #                                                              (0.0, 0.0, 1.0)),
        #                                                          project_file.createIfcDirection(
        #                                                              (1.0, 0.0, 0.0))))
        self.coordinates = coordinates
        self.line = project_file.createIfcLine(project_file.createIfcCartesianPoint(
            (coordinates['coord_x'], coordinates['coord_y'], 0.0)),
            project_file.createIfcVector(
                project_file.createIfcDirection(
                    (0.0, 0.0, 1.0)),
                2.0))
        self.trimmed_curve = project_file.createIfcTrimmedCurve(self.line,
                                                                [project_file.createIfcParameterValue(0.0)],
                                                                [project_file.createIfcParameterValue(1.25)],
                                                                True,
                                                                "PARAMETER")
        self.composite_curve_segment = project_file.createIfcCompositeCurveSegment("CONTINUOUS", True,
                                                                                   self.trimmed_curve)
        self.composite_curve = project_file.createIfcCompositeCurve([self.composite_curve_segment], False)
        self.swept_disk_solid = project_file.createIfcSweptDiskSolid(self.composite_curve, element_radius)
        self.shape_rep = project_file.createIfcShapeRepresentation(project_subcontexts['body_subcontext'], 'Body',
                                                                   'SolidModel',
                                                                   [self.swept_disk_solid])
        self.bounding_box_of_element = project_file.createIfcBoundingBox(
            project_file.createIfcCartesianPoint((0.0, 0.0, 0.0)), element_radius * 2,
                                                                   element_radius * 2,
            4)
        self.bounding_box_shape_rep = project_file.createIfcShapeRepresentation(
            project_subcontexts['box_subcontext'],
            'Box', 'BoundingBox',
            [self.bounding_box_of_element])
        self.product_shape_def = project_file.createIfcProductDefinitionShape(None, None,
                                                                              (self.bounding_box_shape_rep,
                                                                               self.shape_rep))
        self.building_proxy_element = project_file.createIfcBuildingElementProxy(ifcopenshell.guid.new(), None, "proxy",
                                                                                 None, None, None,
                                                                                 self.product_shape_def, None,
                                                                                 "ELEMENT")
