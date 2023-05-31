import ifcopenshell
import pytest

import ifc.IfcProject as IfcProjectBuilder
import ifc.IfcElementBuilderImpls as IfcBuilder

ifc_file = ifcopenshell.file()


@pytest.fixture
def create_model():
    project = IfcProjectBuilder.IfcProject(ifc_file, "Building Element proxy")
    site = (
        IfcBuilder.IfcSimpleOriginPlacementElementBuilderImpl(ifc_file, "site").assign_to_ifcFile().element_name(
            "Site").build())
    building = (
        IfcBuilder.IfcSimpleOriginPlacementElementBuilderImpl(ifc_file, "building").assign_to_ifcFile().element_name(
            "Building").build())
    storey = (
        IfcBuilder.IfcSimpleOriginPlacementElementBuilderImpl(ifc_file, "storey").assign_to_ifcFile().element_name(
            "Ground Floor").build())
    site.create_element_in_ifc_file()
    building.create_element_in_ifc_file()
    storey.create_element_in_ifc_file()
    ifc_file.createIfcRelAggregates("alskdjfeslda", None, None, None, project.ifc_project, [site.element])
    ifc_file.createIfcRelAggregates("alskdjfeslfa", None, None, None, site.element, [building.element])
    ifc_file.createIfcRelAggregates("alskdjfeslea", None, None, None, building.element, [storey.element])

    placement = ifc_file.createIfcLocalPlacement(None,
                                                 ifc_file.createIfcAxis2Placement3D(
                                                     ifc_file.createIfcCartesianPoint(
                                                         (5.0, 3.0, -2.0)),
                                                     ifc_file.createIfcDirection(
                                                         (0.0, 0.0, 1.0)),
                                                     ifc_file.createIfcDirection(
                                                         (1.0, 0.0, 0.0))))

    cartesianPointList2D = ifc_file.createIfcCartesianPointList2D(((0.0, 1.0),
                                                                   (1.0, 1.5),
                                                                   (1.5, 2.0),
                                                                   (1.5, 1.0)))
    polycurve = ifc_file.createIfcIndexedPolyCurve(cartesianPointList2D)
    line = ifc_file.createIfcLine(ifc_file.createIfcCartesianPoint((0.0, 0.0, 0.0)),
                                  ifc_file.createIfcVector(
                                      ifc_file.createIfcDirection(
                                          (5.0, 3.0, 0.0)),
                                      20))
    trimmed_curve = ifc_file.createIfcTrimmedCurve(line, [ifc_file.createIfcParameterValue(0.0)],
                                                   [ifc_file.createIfcParameterValue(1.25)], True,
                                                   "PARAMETER")

    composite_curve_segment = ifc_file.createIfcCompositeCurveSegment("CONTINUOUS", True,
                                                                      trimmed_curve)
    composite_curve = ifc_file.createIfcCompositeCurve([composite_curve_segment], False)
    swept_disk_solid = ifc_file.createIfcSweptDiskSolid(polycurve, 0.0025, 0.002)
    shape_rep = ifc_file.createIfcShapeRepresentation(project.project_sub_contexts['body_subcontext'], 'Body',
                                                      'SolidModel',
                                                      [swept_disk_solid])
    bounding_box_of_pipe_element = ifc_file.createIfcBoundingBox(ifc_file.createIfcCartesianPoint(
        (0.0, 0.0, 0.0)), 1.20, 1.20, 36.0)
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
        storey.element)

    ifc_file.write("export/test_building_element_proxy_polycurve2.ifc")


def test_model_created(create_model):
    assert ifc_file != 0
