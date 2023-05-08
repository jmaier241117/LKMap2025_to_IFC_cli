from os.path import exists

import ifcopenshell
import pytest
from ifcopenshell import file
from ifcopenshell.api import run

ifc_file: file = ifcopenshell.file()


def create_cartesian_point(x, y, z):
    return ifc_file.createIfcCartesianPoint((x, y, z))


def create_direction(x, y, z):
    return ifc_file.createIfcDirection((x, y, z))


@pytest.fixture
def create_model():
    # all ifc points directions and axis and local placements (not concerning shape)
    point_of_model_context = ifc_file.createIfcAxis2Placement3D(create_cartesian_point(0.0, 0.0, 0.0),
                                                                create_direction(0.0, 0.0, 1.0),
                                                                create_direction(1.0, 0.0, 0.0))
    point_of_plan_context = ifc_file.createIfcAxis2Placement2D(ifc_file.createIfcCartesianPoint((0.0, 0.0)),
                                                               ifc_file.createIfcDirection((1.0, 0.0)))
    site_placement = ifc_file.createIfcLocalPlacement(None, ifc_file.createIfcAxis2Placement3D(
        create_cartesian_point(0.0, 0.0, 0.0),
        create_direction(0.0, 0.0, 1.0), create_direction(1.0, 0.0, 0.0)))
    building_placement = ifc_file.createIfcLocalPlacement(None, ifc_file.createIfcAxis2Placement3D(
        create_cartesian_point(0.0, 0.0, 0.0),
        create_direction(0.0, 0.0, 1.0), create_direction(1.0, 0.0, 0.0)))
    storey_placement = ifc_file.createIfcLocalPlacement(None, ifc_file.createIfcAxis2Placement3D(
        create_cartesian_point(0.0, 0.0, 0.0),
        create_direction(0.0, 0.0, 1.0), create_direction(1.0, 0.0, 0.0)))
    chamber_element_placement = ifc_file.createIfcLocalPlacement(storey_placement, ifc_file.createIfcAxis2Placement3D(
        create_cartesian_point(0.0, 0.0, 0.0),
        create_direction(0.0, 0.0, -2.0), create_direction(1.0, 0.0, 0.0)))
    pipe_segment_element_placement = ifc_file.createIfcLocalPlacement(storey_placement,
                                                                      ifc_file.createIfcAxis2Placement3D(
                                                                          create_cartesian_point(0.0, 0.0, -2.0),
                                                                          create_direction(1.0, 0.0, 0.0),
                                                                          create_direction(0.0, 0.0, -1.0)))

    # geometricrepresentation contexts and subcontexts
    model_context = ifc_file.createIfcGeometricRepresentationContext(None, 'Model', 3, 0.01, point_of_model_context,
                                                                     None)
    body_subcontext = ifc_file.createIfcGeometricRepresentationSubContext('Body', 'Model', None, None, None, None,
                                                                          model_context, None, "MODEL_VIEW", None)
    box_subcontext = ifc_file.createIfcGeometricRepresentationSubContext('Box', 'Model', None, None, None, None,
                                                                         model_context, None, "MODEL_VIEW", None)
    plan_context = ifc_file.createIfcGeometricRepresentationContext(None, 'Plan', 2, 0.01, point_of_plan_context, None)

    # unit assignment
    meters = ifc_file.createIfcSIUnit(None, "LENGTHUNIT", None, "METRE")
    square_meters = ifc_file.createIfcSIUnit(None, "AREAUNIT", None, "SQUARE_METRE")
    cubic_meters = ifc_file.createIfcSIUnit(None, "VOLUMEUNIT", None, "CUBIC_METRE")
    radian = ifc_file.createIfcSIUnit(None, "PLANEANGLEUNIT", None, "RADIAN")
    degree = ifc_file.createIfcConversionBasedUnit(
        ifc_file.createIfcDimensionalExponents(0, 0, 0, 0, 0, 0, 0),
        "PLANEANGLEUNIT", 'degree', ifc_file.createIfcMeasureWithUnit(
            ifc_file.createIfcReal(0.0174532925199433), radian))
    number_9 = ifc_file.createIfcUnitAssignment((cubic_meters, meters, degree, square_meters))

    # setup of project, site, building, storey
    project = ifc_file.createIfcProject('3Mw7bnApr2c9W2BHbLjz8u', None, 'My Project', None, None, None, None,
                                        (model_context, plan_context), number_9)
    site = ifc_file.createIfcSite('09lELwXV10KwfwS9Yk8xNU', None, 'My Site', None, None, site_placement)
    building = ifc_file.createIfcBuilding('07LQpIgG19OA8IqP7TdCKf', None, 'My Building', None, None, building_placement)
    storey = ifc_file.createIfcBuildingStorey('0P35MQM2zBqvf7SHE9DS4X', None, 'My Storey', None, None, storey_placement)

    run("aggregate.assign_object", ifc_file, relating_object=project, product=site)
    run("aggregate.assign_object", ifc_file, relating_object=site, product=building)
    run("aggregate.assign_object", ifc_file, relating_object=building, product=storey)

    # 43 - 72 setup of 3D representation of duct
    polygonalface_list = []
    polygonalface_counter = 1
    while polygonalface_counter < 62:
        parameter_tuple = (
            polygonalface_counter, polygonalface_counter + 1, polygonalface_counter + 3, polygonalface_counter + 2)
        polygonalface_list.append(parameter_tuple)
        polygonalface_counter += 2

    polygonalfaceset_tuple = ()
    for polygonalface_tuples in polygonalface_list:
        polygonalfaceset_tuple += (ifc_file.createIfcIndexedPolygonalFace(polygonalface_tuples),)

    # 73-78 setup of 3D representation of duct
    odd_tuple = ()
    for i in range(1, 64, 2):
        odd_tuple += (i,)
    even_tuple = (4, 2)
    for i in range(64, 5, -2):
        even_tuple += (i,)
    polygonalfaceset_tuple += (ifc_file.createIfcIndexedPolygonalFace(even_tuple),)
    polygonalfaceset_tuple += (ifc_file.createIfcIndexedPolygonalFace((63, 64, 2, 1)),)
    polygonalfaceset_tuple += (ifc_file.createIfcIndexedPolygonalFace(odd_tuple),)
    cartesian_point_list_3d_for_duct = ifc_file.createIfcCartesianPointList3D(
        ((0.00, 0.60, -2.00), (0.00, 0.60, 2.00), (0.12, 0.59, -2.00),
         (0.12, 0.59, 2.00), (0.23, 0.55, -2.00), (0.23, 0.55, 2.00),
         (0.33, 0.50, -2.00), (0.33, 0.50, 2.00), (0.42, 0.42, -2.00),
         (0.42, 0.42, 2.00), (0.50, 0.33, -2.00), (0.50, 0.33, 2.00),
         (0.55, 0.23, -2.00), (0.55, 0.23, 2.00), (0.59, 0.12, -2.00),
         (0.59, 0.12, 2.00), (0.60, 0.00, -2.00), (0.60, 0.00, 2.00),
         (0.59, -0.12, -2.00), (0.59, -0.12, 2.00), (0.55, -0.23, -2.00),
         (0.55, -0.23, 2.00), (0.50, -0.33, -2.00), (0.50, -0.33, 2.00),
         (0.42, -0.42, -2.00), (0.42, -0.42, 2.00), (0.33, -0.50, -2.00),
         (0.33, -0.50, 2.00), (0.23, -0.55, -2.00), (0.23, -0.55, 2.00),
         (0.12, -0.59, -2.00), (0.12, -0.59, 2.00), (0.00, -0.60, -2.00),
         (0.00, -0.60, 2.00), (-0.12, -0.59, -2.0), (-0.12, -0.59, 2.00),
         (-0.23, -0.55, -2.0), (-0.23, -0.55, 2.00), (-0.33, -0.50, -2.0),
         (-0.33, -0.50, 2.00), (-0.42, -0.42, -2.0), (-0.42, -0.42, 2.00),
         (-0.50, -0.33, -2.0), (-0.50, -0.33, 2.00), (-0.55, -0.23, -2.0),
         (-0.55, -0.23, 2.00), (-0.59, -0.12, -2.0), (-0.59, -0.12, 2.00),
         (-0.60, 0.00, -2.00), (-0.60, 0.00, 2.00), (-0.59, 0.12, -2.00),
         (-0.59, 0.12, 2.00), (-0.55, 0.23, -2.00), (-0.55, 0.23, 2.00),
         (-0.50, 0.33, -2.00), (-0.50, 0.33, 2.00), (-0.42, 0.42, -2.00),
         (-0.42, 0.42, 2.00), (-0.33, 0.50, -2.00), (-0.33, 0.50, 2.00),
         (-0.23, 0.55, -2.00), (-0.23, 0.55, 2.00), (-0.12, 0.59, -2.00),
         (-0.12, 0.59, 2.00)))

    cartesian_point_list_3d_for_pipe = ifc_file.createIfcCartesianPointList3D(
        ((0.00, 0.30, -18.00), (0.00, 0.30, 18.00), (0.06, 0.29, -18.00),
         (0.06, 0.29, 18.00), (0.11, 0.28, -18.00), (0.11, 0.28, 18.00),
         (0.17, 0.25, -18.00), (0.17, 0.25, 18.00), (0.21, 0.21, -18.00),
         (0.21, 0.21, 18.00), (0.25, 0.17, -18.00), (0.25, 0.17, 18.00),
         (0.28, 0.11, -18.00), (0.28, 0.11, 18.00), (0.29, 0.06, -18.00),
         (0.29, 0.06, 18.00), (0.30, 0.00, -18.00), (0.30, 0.00, 18.00),
         (0.29, -0.0, -18.00), (0.29, -0.0, 18.00), (0.28, -0.1, -18.00),
         (0.28, -0.1, 18.00), (0.25, -0.1, -18.00), (0.25, -0.1, 18.00),
         (0.21, -0.2, -18.00), (0.21, -0.2, 18.00), (0.17, -0.2, -18.00),
         (0.17, -0.2, 18.00), (0.11, -0.2, -18.00), (0.11, -0.2, 18.00),
         (0.06, -0.2, -18.00), (0.06, -0.2, 18.00), (0.00, -0.3, -18.00),
         (0.00, -0.3, 18.00), (-0.06, -0.29, -18.00), (-0.06, -0.29, 18.00),
         (-0.11, -0.28, -18.00), (-0.11, -0.28, 18.00), (-0.17, -0.25, -18.00),
         (-0.17, -0.25, 18.00), (-0.21, -0.21, -18.00), (-0.21, -0.21, 18.00),
         (-0.25, -0.17, -18.00), (-0.25, -0.17, 18.00), (-0.28, -0.11, -18.00),
         (-0.28, -0.11, 18.00), (-0.29, -0.06, -18.00), (-0.29, -0.06, 18.00),
         (-0.30, 0.00, -18.00), (-0.30, 0.00, 18.00), (-0.29, 0.06, -18.00),
         (-0.29, 0.06, 18.00), (-0.28, 0.11, -18.00), (-0.28, 0.11, 18.00),
         (-0.25, 0.17, -18.00), (-0.25, 0.17, 18.00), (-0.21, 0.21, -18.00),
         (-0.21, 0.21, 18.00), (-0.17, 0.25, -18.00), (-0.17, 0.25, 18.00),
         (-0.11, 0.28, -18.00), (-0.11, 0.28, 18.00), (-0.06, 0.29, -18.00),
         (-0.06, 0.29, 18.00)))

    polygonal_faceset_for_duct = ifc_file.createIfcPolygonalFaceSet(cartesian_point_list_3d_for_duct, None,
                                                                    polygonalfaceset_tuple, None)

    polygonal_faceset_for_pipe = ifc_file.createIfcPolygonalFaceSet(cartesian_point_list_3d_for_pipe, None,
                                                                    polygonalfaceset_tuple, None)
    # duct element and its reps
    duct_element_shape_rep = ifc_file.createIfcShapeRepresentation(body_subcontext, 'Body', 'Tessellation',
                                                                   [polygonal_faceset_for_duct])
    point_of_duct_element = ifc_file.createIfcCartesianPoint((-1.0, -1.0, -1.5))
    bounding_box_of_duct_element = ifc_file.createIfcBoundingBox(point_of_duct_element, 2.0, 2.0, 4.0)
    bounding_box_duct_shape_rep = ifc_file.createIfcShapeRepresentation(box_subcontext, 'Box', 'BoundingBox',
                                                                        [bounding_box_of_duct_element])
    prod_def_duct_shape = ifc_file.createIfcProductDefinitionShape(None, None,
                                                                   (
                                                                       bounding_box_duct_shape_rep,
                                                                       duct_element_shape_rep))
    chamber_element = ifc_file.createIfcDistributionChamberElement('3C_jsCNl10VeIaDd7IWf28', None, 'Cylinder', None,
                                                                   None,
                                                                   chamber_element_placement, prod_def_duct_shape, None,
                                                                   "FORMEDDUCT")
    ifc_file.createIfcRelContainedInSpatialStructure('1M6hNzVfn0JeEKNuVP5AEI', None,
                                                     None, None,
                                                     [chamber_element],
                                                     storey)

    pipe_element_shape_rep = ifc_file.createIfcShapeRepresentation(body_subcontext, 'Body', 'Tessellation',
                                                                   [polygonal_faceset_for_pipe])
    point_of_pipe_element = ifc_file.createIfcCartesianPoint((-0.30, -0.30, -18.0))
    bounding_box_of_pipe_element = ifc_file.createIfcBoundingBox(point_of_pipe_element, 1.20, 1.20, 36.0)
    bounding_box_pipe_shape_rep = ifc_file.createIfcShapeRepresentation(box_subcontext, 'Box', 'BoundingBox',
                                                                        [bounding_box_of_pipe_element])
    prod_def_pipe_shape = ifc_file.createIfcProductDefinitionShape(None, None,
                                                                   (
                                                                       bounding_box_pipe_shape_rep,
                                                                       pipe_element_shape_rep))
    pipe_element = ifc_file.createIfcPipeSegment('2iirh2nx97a8aH1wk0tTo5', None, 'Pipe', None,
                                                 None,
                                                 pipe_segment_element_placement, prod_def_pipe_shape,
                                                 None,
                                                 "CULVERT")

    ifc_file.createIfcRelContainedInSpatialStructure('1M6hNzVfn0JeEKNuVP5AEI', None,
                                                     None, None,
                                                     [pipe_element],
                                                     storey)
    ifc_file.write("test_pipe_and_duct_bsp.ifc")


def test_model_created(create_model):
    assert ifc_file != 0
