from os.path import exists

import ifcopenshell
import pytest
from ifcopenshell import file
import ifc.IfcProject as IfcProjectBuilder
import ifc.IfcElementBuilderImpls as IfcBuilder

ifc_file: file = ifcopenshell.file()


@pytest.fixture
def create_model():
    project = IfcProjectBuilder.IfcProject(ifc_file, "Pipes ")
    site = (
        IfcBuilder.IfcSimpleOriginPlacementElementBuilderImpl(ifc_file, "site").assign_to_ifcFile().element_name(
            "Site").element_zero_placement().build())
    building = (
        IfcBuilder.IfcSimpleOriginPlacementElementBuilderImpl(ifc_file, "building").assign_to_ifcFile().element_name(
            "Building").element_zero_placement().build())
    storey = (
        IfcBuilder.IfcSimpleOriginPlacementElementBuilderImpl(ifc_file, "storey").assign_to_ifcFile().element_name(
            "Ground Floor").element_zero_placement().build())
    site.create_element_in_ifc_file()
    building.create_element_in_ifc_file()
    storey.create_element_in_ifc_file()
    ifc_file.createIfcRelAggregates("alskdjfeslda", None, None, None, project.ifc_project, [site.element])
    ifc_file.createIfcRelAggregates("alskdjfeslfa", None, None, None, site.element, [building.element])
    ifc_file.createIfcRelAggregates("alskdjfeslea", None, None, None, building.element, [storey.element])

    cartesianPointList2D = ifc_file.createIfcCartesianPointList2D(((20.44, 4.73), (20.14, 4.83),
                                                                   (14.83, 9.07), (14.55, 9.26),
                                                                   (12.33, 10.81), (5.90, 11.24),
                                                                   (5.31, 11.45)))

    polycurve = ifc_file.createIfcIndexedPolyCurve(cartesianPointList2D)

    swept_disk_solid = ifc_file.createIfcSweptDiskSolid(polycurve, 0.0025, 0.002)
    shape_rep = ifc_file.createIfcShapeRepresentation(project.project_sub_contexts['body_subcontext'], 'Body',
                                                      'SolidModel',
                                                      [swept_disk_solid])
    bounding_box_of_element = ifc_file.createIfcBoundingBox(
        ifc_file.createIfcCartesianPoint((0.0, 0.0, 0.0)), 2, 2, 50)
    bounding_box_shape_rep = ifc_file.createIfcShapeRepresentation(
        project.project_sub_contexts['box_subcontext'], 'Box', 'BoundingBox', [bounding_box_of_element])
    pipe_prod_shape = ifc_file.createIfcProductDefinitionShape(None, None, (bounding_box_shape_rep,
                                                                            shape_rep))

    pipe_segment_element = ifc_file.createIfcDistributionFlowElement('3IryYYgibBfAnY6kfakPYk', None, 'Pipe', None,
                                                                     None, None, pipe_prod_shape)

    ifc_file.createIfcRelContainedInSpatialStructure('1M6hNzVfn0JeEKNuVP5AEI', None, None, None, [pipe_segment_element],
                                                     storey.element)

    ifc_file.write("export/test_pipe_swept_disk_solid.ifc")


def test_model_created(create_model):
    assert ifc_file != 0
