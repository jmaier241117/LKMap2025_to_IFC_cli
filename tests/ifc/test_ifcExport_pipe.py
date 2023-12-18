from os.path import exists

import ifcopenshell
import pytest
from ifcopenshell import file
from ifc.IfcProjectSetupBuilder import IfcProject, IfcSite
from ifc import IfcUtils

ifc_file: file = ifcopenshell.file(schema="IFC4X3")


@pytest.fixture
def create_model():
    project = IfcProject(ifc_file, "Pipes", (200, 100, 4))
    site = IfcSite(ifc_file, 'Site', ifc_file.createIfcLocalPlacement(None,
                                                     ifc_file.createIfcAxis2Placement3D(
                                                         ifc_file.createIfcCartesianPoint(
                                                             IfcUtils.zero_point_3D),
                                                         ifc_file.createIfcDirection(
                                                             IfcUtils.zero_point_3D_direction_1),
                                                         ifc_file.createIfcDirection(
                                                             IfcUtils.zero_point_3D_direction_2))))
    ifc_file.createIfcRelAggregates(ifcopenshell.guid.new(), None, None, None, project.element, [site.element])

    cartesianPointList2D = ifc_file.createIfcCartesianPointList2D(((20.44, 4.73), (20.14, 4.83)))

    polycurve = ifc_file.createIfcIndexedPolyCurve(cartesianPointList2D)

    swept_disk_solid = ifc_file.createIfcSweptDiskSolid(polycurve, 0.0025, 0.002)
    swept_disk_solid_uncertainty = ifc_file.createIfcSweptDiskSolid(polycurve, 0.005, 0.002)

    element_color1 = ifc_file.createIfcColourRgb('color', 0.5, 0.4, 3)
    surface_style_rendering = ifc_file.createIfcSurfaceStyleShading(element_color1, 0.0)
    surface_style1 = ifc_file.createIfcSurfaceStyle("style", 'BOTH', [surface_style_rendering])
    ifc_file.createIfcStyledItem(swept_disk_solid, [surface_style1])

    element_color2 = ifc_file.createIfcColourRgb('color', 0.2, 0.2, 1)
    surface_style_rendering_uncertainty = ifc_file.createIfcSurfaceStyleShading(element_color2, 0.75)
    surface_style2 = ifc_file.createIfcSurfaceStyle("style", 'BOTH', [surface_style_rendering_uncertainty])
    ifc_file.createIfcStyledItem(swept_disk_solid_uncertainty, [surface_style2])

    shape_rep = ifc_file.createIfcShapeRepresentation(project.project_contexts['model_context'], 'Body',
                                                      'SolidModel',
                                                      [swept_disk_solid, swept_disk_solid_uncertainty])
    bounding_box_of_element = ifc_file.createIfcBoundingBox(
        ifc_file.createIfcCartesianPoint((0.0, 0.0, 0.0)), 2, 2, 50)
    bounding_box_shape_rep = ifc_file.createIfcShapeRepresentation(
        project.project_contexts['model_context'], 'Box', 'BoundingBox', [bounding_box_of_element])
    pipe_prod_shape = ifc_file.createIfcProductDefinitionShape(None, None, (bounding_box_shape_rep,
                                                                            shape_rep))

    pipe_segment_element = ifc_file.createIfcDistributionFlowElement(ifcopenshell.guid.new(), None, 'Pipe', None,
                                                                     None, None, pipe_prod_shape)

    ifc_file.createIfcRelContainedInSpatialStructure(ifcopenshell.guid.new(), None, None, None, [pipe_segment_element],
                                                     site.element)

    ifc_file.write("export/test_pipe_43_TC1.ifc")


def test_model_created(create_model):
    assert ifc_file != 0
