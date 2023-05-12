from os.path import exists

import ifcopenshell
import pytest
from typing import Any
from ifcopenshell import file
from ifcopenshell.api import run
from ifcopenshell.ifcopenshell_wrapper import entity_instance

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
        create_direction(0.99, 0.0, -0.09), create_direction(-0.09, 0.0, -0.99)))
    building_placement = ifc_file.createIfcLocalPlacement(site_placement, ifc_file.createIfcAxis2Placement3D(
        create_cartesian_point(0.0, 0.0, 0.0),
        create_direction(0.0, 0.0, 1.0), create_direction(1.0, 0.0, -1.4)))
    storey_placement = ifc_file.createIfcLocalPlacement(building_placement, ifc_file.createIfcAxis2Placement3D(
        create_cartesian_point(0.0, 0.0, 0.0),
        create_direction(0.0, 0.0, 1.0), create_direction(1.0, 0.0, -1.4)))
    pipe_segment_element_placement = ifc_file.createIfcLocalPlacement(storey_placement,
                                                                      ifc_file.createIfcAxis2Placement3D(
                                                                          create_cartesian_point(0.0, 0.0, 0.0),
                                                                          create_direction(-0.09, 0.0, 0.99),
                                                                          create_direction(0.99, 0.0, 0.09)))

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
    unit_assignment = ifc_file.createIfcUnitAssignment((cubic_meters, meters, degree, square_meters))

    # setup of project, site, building, storey
    project = ifc_file.createIfcProject('3Mw7bnApr2c9W2BHbLjz8u', None, 'My Project', None, None, None, None,
                                        (model_context, plan_context), unit_assignment)
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
    cartesian_point_list_3d = ifc_file.createIfcCartesianPointList3D(((0., 0.483485996723175, -8.83390998840332),
                                                                      (0., 0.483485996723175, 8.83390998840332), (
                                                                          0.0943234413862228, 0.474195927381516,
                                                                          -8.83390998840332), (
                                                                          0.0943234413862228, 0.474195927381516,
                                                                          8.83390998840332), (
                                                                          0.185022085905075, 0.446682810783386,
                                                                          -8.83390998840332), (
                                                                          0.185022085905075, 0.446682810783386,
                                                                          8.83390998840332), (
                                                                          0.268610447645187, 0.402003914117813,
                                                                          -8.83390998840332), (
                                                                          0.268610447645187, 0.402003914117813,
                                                                          8.83390998840332), (
                                                                          0.341876208782196, 0.341876208782196,
                                                                          -8.83390998840332), (
                                                                          0.341876208782196, 0.341876208782196,
                                                                          8.83390998840332), (
                                                                          0.402003914117813, 0.268610447645187,
                                                                          -8.83390998840332), (
                                                                          0.402003914117813, 0.268610447645187,
                                                                          8.83390998840332), (
                                                                          0.446682810783386, 0.185022085905075,
                                                                          -8.83390998840332), (
                                                                          0.446682810783386, 0.185022085905075,
                                                                          8.83390998840332), (
                                                                          0.474195927381516, 0.0943234413862228,
                                                                          -8.83390998840332), (
                                                                          0.474195927381516, 0.0943234413862228,
                                                                          8.83390998840332),
                                                                      (0.483485996723175, 0., -8.83390998840332),
                                                                      (0.483485996723175, 0., 8.83390998840332), (
                                                                          0.474195927381516, -0.0943234413862228,
                                                                          -8.83390998840332), (
                                                                          0.474195927381516, -0.0943234413862228,
                                                                          8.83390998840332), (
                                                                          0.446682810783386, -0.185022085905075,
                                                                          -8.83390998840332), (
                                                                          0.446682810783386, -0.185022085905075,
                                                                          8.83390998840332), (
                                                                          0.402003914117813, -0.268610447645187,
                                                                          -8.83390998840332), (
                                                                          0.402003914117813, -0.268610447645187,
                                                                          8.83390998840332), (
                                                                          0.341876208782196, -0.341876208782196,
                                                                          -8.83390998840332), (
                                                                          0.341876208782196, -0.341876208782196,
                                                                          8.83390998840332), (
                                                                          0.268610447645187, -0.402003914117813,
                                                                          -8.83390998840332), (
                                                                          0.268610447645187, -0.402003914117813,
                                                                          8.83390998840332), (
                                                                          0.185022085905075, -0.446682810783386,
                                                                          -8.83390998840332), (
                                                                          0.185022085905075, -0.446682810783386,
                                                                          8.83390998840332), (
                                                                          0.0943234413862228, -0.474195927381516,
                                                                          -8.83390998840332), (
                                                                          0.0943234413862228, -0.474195927381516,
                                                                          8.83390998840332),
                                                                      (0., -0.483485996723175, -8.83390998840332),
                                                                      (0., -0.483485996723175, 8.83390998840332), (
                                                                          -0.0943234413862228, -0.474195927381516,
                                                                          -8.83390998840332), (
                                                                          -0.0943234413862228, -0.474195927381516,
                                                                          8.83390998840332), (
                                                                          -0.185022085905075, -0.446682810783386,
                                                                          -8.83390998840332), (
                                                                          -0.185022085905075, -0.446682810783386,
                                                                          8.83390998840332), (
                                                                          -0.268610447645187, -0.402003914117813,
                                                                          -8.83390998840332), (
                                                                          -0.268610447645187, -0.402003914117813,
                                                                          8.83390998840332), (
                                                                          -0.341876208782196, -0.341876208782196,
                                                                          -8.83390998840332), (
                                                                          -0.341876208782196, -0.341876208782196,
                                                                          8.83390998840332), (
                                                                          -0.402003914117813, -0.268610447645187,
                                                                          -8.83390998840332), (
                                                                          -0.402003914117813, -0.268610447645187,
                                                                          8.83390998840332), (
                                                                          -0.446682810783386, -0.185022085905075,
                                                                          -8.83390998840332), (
                                                                          -0.446682810783386, -0.185022085905075,
                                                                          8.83390998840332), (
                                                                          -0.474195927381516, -0.0943234413862228,
                                                                          -8.83390998840332), (
                                                                          -0.474195927381516, -0.0943234413862228,
                                                                          8.83390998840332),
                                                                      (-0.483485996723175, 0., -8.83390998840332),
                                                                      (-0.483485996723175, 0., 8.83390998840332), (
                                                                          -0.474195927381516, 0.0943234413862228,
                                                                          -8.83390998840332), (
                                                                          -0.474195927381516, 0.0943234413862228,
                                                                          8.83390998840332), (
                                                                          -0.446682810783386, 0.185022085905075,
                                                                          -8.83390998840332), (
                                                                          -0.446682810783386, 0.185022085905075,
                                                                          8.83390998840332), (
                                                                          -0.402003914117813, 0.268610447645187,
                                                                          -8.83390998840332), (
                                                                          -0.402003914117813, 0.268610447645187,
                                                                          8.83390998840332), (
                                                                          -0.341876208782196, 0.341876208782196,
                                                                          -8.83390998840332), (
                                                                          -0.341876208782196, 0.341876208782196,
                                                                          8.83390998840332), (
                                                                          -0.268610447645187, 0.402003914117813,
                                                                          -8.83390998840332), (
                                                                          -0.268610447645187, 0.402003914117813,
                                                                          8.83390998840332), (
                                                                          -0.185022085905075, 0.446682810783386,
                                                                          -8.83390998840332), (
                                                                          -0.185022085905075, 0.446682810783386,
                                                                          8.83390998840332), (
                                                                          -0.0943234413862228, 0.474195927381516,
                                                                          -8.83390998840332), (
                                                                          -0.0943234413862228, 0.474195927381516,
                                                                          8.83390998840332)))

    polygonal_faceset = ifc_file.createIfcPolygonalFaceSet(cartesian_point_list_3d, None, polygonalfaceset_tuple, None)

    # duct element and its reps
    element_shape_rep = ifc_file.createIfcShapeRepresentation(body_subcontext, 'Body', 'Tessellation',
                                                              [polygonal_faceset])
    point_of_element = ifc_file.createIfcCartesianPoint((-0.30, -0.30, -18.0))
    bounding_box_of_element = ifc_file.createIfcBoundingBox(point_of_element, 1.20, 1.20, 24.0)
    bounding_box_shape_rep = ifc_file.createIfcShapeRepresentation(box_subcontext, 'Box', 'BoundingBox',
                                                                   [bounding_box_of_element])
    pipe_segment_prod_def_shape = ifc_file.createIfcProductDefinitionShape(None, None,
                                                                           (bounding_box_shape_rep, element_shape_rep))
    pipe_segment_element = ifc_file.createIfcPipeSegment('3IryYYgibBfAnY6kfakPYk', None, 'Cylinder', None, None,
                                                         pipe_segment_element_placement, pipe_segment_prod_def_shape,
                                                         None, "CULVERT")

    ifc_file.createIfcRelContainedInSpatialStructure('1M6hNzVfn0JeEKNuVP5AEI', None, None, None, [pipe_segment_element],
                                                     storey)

    ifc_file.write("export/test_pipe_bsp.ifc")


def test_model_created(create_model):
    assert ifc_file != 0
