import ifcopenshell
import os.path
from ifcopenshell import file


class IfcFileBuilder:
    def __init__(self, file_name):
        self.file = ifcopenshell.file(file_name)


def write_ifc_file(fileName: string, directoryPath: path):
    ifc_file.write(path + fileName)
    exists()


class IfcDistributionChamberElementBuilderImpl(IIfcElementBuilder):

    def __init__(self):
        self.project_file
        self.element_name
        self.placement
        self.point_list_3d
        self.polygonal_faceset_16
        self.shape_rep
        self.distribution_chamber_element

    def assign_to_ifcFile(self, ifc_file):
        self.placement = project_file.createIfcLocalPlacement(None,
                                                              project_file.createIfcAxis2Placement3D(
                                                                  project_file.createIfcCartesianPoint(
                                                                      (coord_x, coord_y, -2.0)),
                                                                  project_file.createIfcDirection(
                                                                      (0.0, 0.0, 1.0)),
                                                                  project_file.createIfcDirection(
                                                                      (1.0, 0.0, 0.0))))
        self.point_list_3d = project_file.createIfcCartesianPointList3D(
            ((0.00, 0.60, -2.00), (0.00, 0.60, 2.00),
             (0.42, 0.42, -2.00), (0.42, 0.42, 2.00),
             (0.60, 0.00, -2.00), (0.60, 0.00, 2.00),
             (0.42, -0.42, -2.00), (0.42, -0.42, 2.00),
             (0.00, -0.60, -2.00), (0.00, -0.60, 2.00),
             (-0.42, -0.42, -2.0), (-0.42, -0.42, 2.00),
             (-0.60, 0.00, -2.00), (-0.60, 0.00, 2.00),
             (-0.42, 0.42, -2.00), (-0.42, 0.42, 2.00)))
        self.polygonal_faceset_16 = create_polygonal_faceset_tesselation_16face(project_file, self.point_list_3d)
        self.shape_rep = project_file.createIfcShapeRepresentation(project_subcontexts['body_subcontext'], 'Body',
                                                                   'Tessellation',
                                                                   [self.polygonal_faceset_16])
        self.distribution_chamber_element = project_file.createIfcDistributionChamberElement(
            ifcopenshell.guid.new(), None, "Duct Element", None,
            None, self.placement, self.shape_rep, None, element_type)

        self.size = project_file.createIfcCartesianPoint((-0.60, -0.60, -2.0))
        self.bounding_box = project_file.createIfcBoundingBox(self.size, 1.20, 1.20, 4.0)
        self.bounding_box_shape_rep = project_file.createIfcShapeRepresentation(
            project_subcontexts['box_subcontext'], 'Box', 'BoundingBox', [self.bounding_box])
        self.product_shape_def = project_file.createIfcProductDefinitionShape(None, None,
                                                                              (self.bounding_box_shape_rep,
                                                                               self.shape_rep))


# class IfcPipeSegmentBuilder:
#   def __init__(self, project_file, project_subcontexts, pipe_segments, element_type):
#        pipe_segment_keys = list(pipe_segments.keys())
# for i, key in enumerate(pipe_segment_keys):
#   if i > 0:
#       key = pipe_segment_keys[i]
#       value = pipe_segments[key]
#       previous_key = pipe_segment_keys[i - 1]
#       previous_value = pipe_segments[previous_key]
#       self.placement = project_file.createIfcLocalPlacement(None,
#                                                             project_file.createIfcAxis2Placement3D(
#                                                                 project_file.createIfcCartesianPoint(
#                                                                     (previous_value[
#                                                                          'coord_x'],
#                                                                      previous_value[
#                                                                          'coord_y'],
#                                                                      0.0)),
#                                                                 project_file.createIfcDirection(
#                                                                     (coordinates_and_lengths['coord_x'],
#                                                                      coordinates_and_lengths['coord_y'],
#                                                                      0.0)),
#                                                                 project_file.createIfcDirection(
#                                                                     (1.0, 0.0, 0.0))))
# self.point_list_3d = project_file.createIfcCartesianPointList3D(
#   ((0.00, 0.30, -coordinates_and_lengths['length']), (0.00, 0.30, coordinates_and_lengths['length']),
#    (0.21, 0.21, -coordinates_and_lengths['length']), (0.21, 0.21, coordinates_and_lengths['length']),
#    (0.30, 0.00, -coordinates_and_lengths['length']), (0.30, 0.00, coordinates_and_lengths['length']),
#    (0.21, -0.2, -coordinates_and_lengths['length']), (0.21, -0.2, coordinates_and_lengths['length']),
#    (0.00, -0.3, -coordinates_and_lengths['length']), (0.00, -0.3, coordinates_and_lengths['length']),
#    (-0.21, -0.21, -coordinates_and_lengths['length']), (-0.21, -0.21, coordinates_and_lengths['length']),
#    (-0.30, 0.00, -coordinates_and_lengths['length']), (-0.30, 0.00, coordinates_and_lengths['length']),
#    (-0.21, 0.21, -coordinates_and_lengths['length']), (-0.21, 0.21, coordinates_and_lengths['length'])))

# self.polygonal_faceset_16 = create_polygonal_faceset_tesselation_16face(project_file, self.point_list_3d)
# self.shape_rep = project_file.createIfcShapeRepresentation(project_subcontexts['body_subcontext'], 'Body',
#                                                    'Tessellation',
#                                                    [self.polygonal_faceset_16])
# self.pipe_segment = project_file.createIfcPipeSegment(ifcopenshell.guid.new(), None, "Pipe Element", None,
#                                                    None, self.placement, self.shape_rep, None,
#                                                  element_type)
# self.pipe_length = coordinates_and_lengths['length']
# self.size = project_file.createIfcCartesianPoint((-0.30, -0.30, self.pipe_length))
# self.bounding_box = project_file.createIfcBoundingBox(self.size, 1.20, 1.20,
#                                                      self.pipe_length * 2)
# self.bounding_box_shape_rep = project_file.createIfcShapeRepresentation(
#    project_subcontexts['box_subcontext'], 'Box', 'BoundingBox', [self.bounding_box])
# self.product_shape_def = project_file.createIfcProductDefinitionShape(None, None,
#                                                                     (
#                                                                     self.bounding_box_shape_rep,
#                                                                     self.shape_rep))


def create_polygonal_faceset_tesselation_16face(project_file, cartesian_point_list_3d: any) -> any:
    polygonalface_list = []
    polygonalface_counter = 1
    while polygonalface_counter < 14:
        parameter_tuple = (
            polygonalface_counter, polygonalface_counter + 1, polygonalface_counter + 3, polygonalface_counter + 2)
        polygonalface_list.append(parameter_tuple)
        polygonalface_counter += 2
    polygonalfaceset_tuple = ()
    for polygonal_tuples in polygonalface_list:
        polygonalfaceset_tuple += (project_file.createIfcIndexedPolygonalFace(polygonal_tuples),)
    odd_tuple = ()
    for i in range(1, 16, 2):
        odd_tuple += (i,)
    even_tuple = (4, 2)
    for i in range(16, 5, -2):
        even_tuple += (i,)
    polygonalfaceset_tuple += (project_file.createIfcIndexedPolygonalFace(even_tuple),)
    polygonalfaceset_tuple += (project_file.createIfcIndexedPolygonalFace((15, 16, 2, 1)),)
    polygonalfaceset_tuple += (project_file.createIfcIndexedPolygonalFace(odd_tuple),)
    return project_file.createIfcPolygonalFaceSet(cartesian_point_list_3d, None,
                                                  polygonalfaceset_tuple, None)
