import ifcopenshell
import pytest

import ifc.IfcProject as ifc
import ifc.IfcElementBuilderImpls as ifc_element

ifc_file = ifcopenshell.file()


@pytest.fixture
def create_model():
    project = ifc.IfcProjectBuilder(ifc_file, "Pipes")
    site = ifc_element.IfcSiteBuilder(ifc_file, "Site", project.project_zero_placement)
    building = ifc_element.IfcBuildingBuilder(ifc_file, "Building", project.project_zero_placement)
    storey = ifc_element.IfcBuildingStoreyBuilder(ifc_file, "Storey", project.project_zero_placement)

    ifc_file.createIfcRelAggregates("alskdjfeslda", None, None, None, project.ifc_project, [site.site_element])
    ifc_file.createIfcRelAggregates("alskdjfeslfa", None, None, None, site.site_element, [building.building_element])
    ifc_file.createIfcRelAggregates("alskdjfeslea", None, None, None, building.building_element,
                                    [storey.storey_element])

    placement = ifc_file.createIfcLocalPlacement(None,
                                                 ifc_file.createIfcAxis2Placement3D(
                                                     ifc_file.createIfcCartesianPoint(
                                                         (5.0, 3.0, -2.0)),
                                                     ifc_file.createIfcDirection(
                                                         (0.0, 0.0, 1.0)),
                                                     ifc_file.createIfcDirection(
                                                         (1.0, 0.0, 0.0))))
    line = ifc_file.createIfcLine(ifc_file.createIfcCartesianPoint((0.0, 0.0, 0.0)),
                                  ifc_file.createIfcVector(
                                      ifc_file.createIfcDirection(
                                          (5.0, 3.0, 0.0)),
                                      5))
    trimmed_curve = ifc_file.createIfcTrimmedCurve(line, [ifc_file.createIfcParameterValue(0.0)],
                                                   [ifc_file.createIfcParameterValue(1.25)], True,
                                                   "PARAMETER")
    composite_curve_segment = ifc_file.createIfcCompositeCurveSegment("CONTINUOUS", True,
                                                                      trimmed_curve)
    composite_curve = ifc_file.createIfcCompositeCurve([composite_curve_segment], False)
    swept_disk_solid = ifc_file.createIfcSweptDiskSolid(composite_curve, 0.25)
    shape_rep = ifc_file.createIfcShapeRepresentation(project.project_sub_contexts['body_subcontext'], 'Body',
                                                      'SolidModel',
                                                      [swept_disk_solid])
    bounding_box_of_pipe_element = ifc_file.createIfcBoundingBox(placement, 1.20, 1.20, 36.0)
    bounding_box_pipe_shape_rep = ifc_file.createIfcShapeRepresentation(project.project_sub_contexts['box_subcontext'],
                                                                        'Box', 'BoundingBox',
                                                                        [bounding_box_of_pipe_element])
    product_shape_def = ifc_file.createIfcProductDefinitionShape(None, None,
                                                                 (bounding_box_pipe_shape_rep, shape_rep))
    building_proxy_element = ifc_file.createIfcBuildingElementProxy(ifcopenshell.guid.new(), None, "proxy",
                                                                    None, None, placement,
                                                                    product_shape_def, None,
                                                                    "ELEMENT")
    ifc_file.createIfcRelContainedInSpatialStructure(
        '1M6hNzVfn0JeEKNuVP5AEI', None,
        None, None,
        [building_proxy_element],
        storey.storey_element)

    ifc_file.write("export/test_building_element_proxy.ifc")


def test_model_created(create_model):
    assert ifc_file != 0
