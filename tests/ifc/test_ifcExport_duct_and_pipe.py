from os.path import exists

import ifcopenshell
import pytest
from ifcopenshell import file
from ifcopenshell.api import run

from ifc.IfcUtils import build_style_rep, build_shape_rep

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

    # geometricrepresentation contexts and subcontexts
    model_context = ifc_file.createIfcGeometricRepresentationContext(None, 'Model', 3, 0.01, point_of_model_context,
                                                                     None)
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

    run("aggregate.assign_object", ifc_file, relating_object=project, product=site)

    polyline = ifc_file.createIfcPolyline(
        (ifc_file.createIfcCartesianPoint((4.0, 5.0, 0.0)), ifc_file.createIfcCartesianPoint((4.0, 5.0, 2.0))))
    shape_rep1 = ifc_file.createIfcShapeRepresentation(model_context, 'Axis', 'Curve3D',
                                                       [polyline])
    direction = ifc_file.createIfcDirection((0.0, 0.0, 1.0))
    axis_placement = ifc_file.createIfcAxis2Placement3D(ifc_file.createIfcCartesianPoint((4.0, 5.0, 0.0)))
    circle_profile_def = ifc_file.createIfcCircleHollowProfileDef('AREA', None, None, 0.6, 0.0125)
    extruded_area_solid = ifc_file.createIfcExtrudedAreaSolid(circle_profile_def, axis_placement, direction, 2.0)
    shape_rep2 = ifc_file.createIfcShapeRepresentation(model_context, 'Body', 'SweptSolid',
                                                       [extruded_area_solid])

    prod_def_duct_shape = ifc_file.createIfcProductDefinitionShape(None, None, (shape_rep1, shape_rep2))

    chamber_element = ifc_file.createIfcDistributionFlowElement(ifcopenshell.guid.new(), None, 'Duct', None,
                                                                None, None, prod_def_duct_shape)
    ifc_file.createIfcRelContainedInSpatialStructure('1M6hNzVfn0JeEKNuVP5AEI', None,
                                                     None, None,
                                                     [chamber_element],
                                                     site)

    cartesian_point_list_2d = ifc_file.createIfcCartesianPointList2D(((20.44, 4.73), (0.0, 0.0)))
    poly_indexed_curve = ifc_file.createIfcIndexedPolyCurve(cartesian_point_list_2d)
    swept_disk_solid = ifc_file.createIfcSweptDiskSolidPolygonal(poly_indexed_curve, 0.5, 0.5 * 0.75)

    shape_rep = ifc_file.createIfcShapeRepresentation(model_context,
                                                  'Body', 'SolidModel',
                                                  [swept_disk_solid])
    bounding_box_of_element = ifc_file.createIfcBoundingBox(
        ifc_file.createIfcCartesianPoint((0.0, 0.0, 0.0)), 2, 2, 50)
    bounding_box_shape_rep = ifc_file.createIfcShapeRepresentation(
       model_context, 'Box', 'BoundingBox', [bounding_box_of_element])

    prod_def_pipe_shape = ifc_file.createIfcProductDefinitionShape(None, None, (bounding_box_shape_rep, shape_rep))

    element_color = ifc_file.createIfcColourRgb('color', 0.88, 0.88, 0.88)
    surface_style_rendering = ifc_file.createIfcSurfaceStyleRendering(element_color, 0.0,  # transparency
                                                                  None, None, None, None, None, None,
                                                                  'NOTDEFINED')
    surface_style = ifc_file.createIfcSurfaceStyle("style", 'BOTH', [surface_style_rendering])
    ifc_file.createIfcStyledItem(swept_disk_solid, [surface_style])

    pipe_element = ifc_file.createIfcDistributionFlowElement(ifcopenshell.guid.new(), None, 'Pipe', None,
                                                             None, None, prod_def_pipe_shape)
    ifc_file.createIfcRelContainedInSpatialStructure('1M6hNzVfn0JeEKNuVP5AEI', None,
                                                     None, None,
                                                     [pipe_element],
                                                     site)

    ifc_file.write("export/test_pipe_and_duct_bsp.ifc")


def test_model_created(create_model):
    assert ifc_file != 0
