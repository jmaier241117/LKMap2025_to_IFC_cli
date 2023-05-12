import string
from os.path import exists
import ifc.ifc_project_builder
import ifcopenshell
import pytest
from ifcopenshell import file
from ifcopenshell.api import run
import ifcopenshell.guid

from ifc.ifc_element_builder import create_dsitribution_chamber_element, create_polygonal_faceset_tesselation_16face, \
    create_3d_pointlist_for_pipe_element

ifc_file: file = ifcopenshell.file()
cartesian_point_3d = ifc_file.createIfcAxis2Placement3D(ifc_file.createIfcCartesianPoint((0.0, 0.0, 0.0)),
                                                        ifc_file.createIfcDirection((0.0, 0.0, 1.0)),
                                                        ifc_file.createIfcDirection((1.0, 0.0, 0.0)))
cartesian_point_2d = ifc_file.createIfcAxis2Placement2D(ifc_file.createIfcCartesianPoint((0.0, 0.0)),
                                                        ifc_file.createIfcDirection((1.0, 0.0)))


@pytest.fixture
def create_model():
    context_dict = ifc.create_contexts(ifc_file)

    project = ifc_file.createIfcProject('3Mw7bnApr2c9W2BHbLjz8u', None, 'Anwilerstrasse 10', None, None, None, None,
                                        (context_dict['contextsList']['model_context'],
                                         context_dict['contextsList']['plan_context']),
                                        ifc.create_unit_assignment(ifc_file))
    site = ifc_file.createIfcSite('09lELwXV10KwfwS9Yk8xNU', None, 'My Site', None, None, cartesian_point_3d)
    building = ifc_file.createIfcBuilding('07LQpIgG19OA8IqP7TdCKf', None, 'My Building', None, None, cartesian_point_3d)
    storey = ifc_file.createIfcBuildingStorey('0P35MQM2zBqvf7SHE9DS4X', None, 'GroundFloor', None, None,
                                              cartesian_point_3d)

    run("aggregate.assign_object", ifc_file, relating_object=project, product=site)
    run("aggregate.assign_object", ifc_file, relating_object=site, product=building)
    run("aggregate.assign_object", ifc_file, relating_object=building, product=storey)

    chamber_shape_rep = ifc_file.createIfcShapeRepresentation(context_dict['subcontextsList']['body_subcontext'],
                                                              'Body', 'Tessellation',
                                                              [create_polygonal_faceset_tesselation_16face(ifc_file,
                                                                                                           create_3d_pointlist_for_chamber_element(
                                                                                                               ifc_file))])
    point_of_element = ifc_file.createIfcCartesianPoint((-0.60, -0.60, -2.0))
    bounding_box_of_element = ifc_file.createIfcBoundingBox(point_of_element, 1.20, 1.20, 4.0)
    bounding_box_chamber_shape_rep = ifc_file.createIfcShapeRepresentation(
        context_dict['subcontextsList']['box_subcontext'],
        'Box', 'BoundingBox',
        [bounding_box_of_element])
    chamber_product_shape_def = ifc_file.createIfcProductDefinitionShape(None, None,
                                                                         (bounding_box_chamber_shape_rep,
                                                                          chamber_shape_rep))

    chamber_element1 = create_dsitribution_chamber_element(ifc_file, "chamber1", 27.34, 4.30,
                                                           chamber_product_shape_def, "FORMEDDUCT")
    chamber_element2 = create_dsitribution_chamber_element(ifc_file, "chamber2", 19.58, 13.89,
                                                           chamber_product_shape_def, "FORMEDDUCT")
    chamber_element3 = create_dsitribution_chamber_element(ifc_file, "chamber3", 29.59, 17.29,
                                                           chamber_product_shape_def, "FORMEDDUCT")
    chamber_element4 = create_dsitribution_chamber_element(ifc_file, "chamber4", 1.82, 4.27,
                                                           chamber_product_shape_def, "FORMEDDUCT")
    chamber_element5 = create_dsitribution_chamber_element(ifc_file, "chamber5", 20.94, 4.81,
                                                           chamber_product_shape_def, "FORMEDDUCT")
    chamber_element6 = create_dsitribution_chamber_element(ifc_file, "chamber6", 5.31, 11.45,
                                                           chamber_product_shape_def, "FORMEDDUCT")
    chamber_element7 = create_dsitribution_chamber_element(ifc_file, "chamber7", 5.79, 35.21,
                                                           chamber_product_shape_def, "FORMEDDUCT")
    ifc_file.createIfcRelContainedInSpatialStructure('1M6hNzVfn0JeEKNuVP5AEI', None,
                                                     None, None,
                                                     [chamber_element1, chamber_element2, chamber_element3,
                                                      chamber_element4, chamber_element5, chamber_element6,
                                                      chamber_element7],
                                                     storey)

    pipe_element_shape_rep = ifc_file.createIfcShapeRepresentation(body_subcontext, 'Body', 'Tessellation',
                                                                   [create_polygonal_faceset_tesselation_16face(
                                                                       ifc_file,
                                                                       create_3d_pointlist_for_pipe_element(
                                                                           ifc_file, length))])
    point_of_pipe_element = ifc_file.createIfcCartesianPoint((-0.30, -0.30, -18.0))
    bounding_box_of_pipe_element = ifc_file.createIfcBoundingBox(point_of_pipe_element, 1.20, 1.20, 36.0)
    bounding_box_pipe_shape_rep = ifc_file.createIfcShapeRepresentation(box_subcontext, 'Box', 'BoundingBox',
                                                                        [bounding_box_of_pipe_element])
    prod_def_pipe_shape = ifc_file.createIfcProductDefinitionShape(None, None,
                                                                   (
                                                                       bounding_box_pipe_shape_rep,
                                                                       pipe_element_shape_rep))

    ifc_file.createIfcRelContainedInSpatialStructure('1M6hNzVfn0JeEKNuVP5AEI', None,
                                                     None, None,
                                                     [pipe_element],
                                                     storey)
    ifc_file.write("test_rothenfluh_anwielerstr_10_bsp.ifc")


def test_model_created(create_model):
    assert ifc_file != 0


def test_write_model():
    ifc_file.write("/export/ifc/testLINE.ifc")
    assert exists('/export/ifc/testLINE.ifc')
