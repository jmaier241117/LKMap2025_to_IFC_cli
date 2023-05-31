import ifc.IfcProject as IfcProjectBuilder
import ifc.IfcElementBuilderImpls as IfcBuilder

import pytest
import ifcopenshell.guid

ifc_file = ifcopenshell.file()


@pytest.fixture
def create_model():
    project = IfcProjectBuilder.IfcProject(ifc_file, "Anwilerstr 10")
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

    coordinates = [((29.04, -2.41), (28.87, -2.08), (27.48, 4.33)),
                   ((25.38, 11.95), (25.14, 11.53), (23.67, 8.97), (21.59, 5.64), (20.94, 4.81)),
                   ((20.44, 4.73), (20.14, 4.83), (14.83, 9.07), (14.55, 9.26), (12.33, 10.81), (5.90, 11.24),
                    (5.31, 11.45)),
                   ((1.82, 4.27), (-2.84, -4.95), (-4.65, -8.51)),
                   ((1.98, 4.38), (1.82, 4.27)),
                   ((1.96, 4.19), (1.82, 4.27)),
                   ((14.17, 17.20), (12.75, 18.12), (-2.53, 27.96), (-9.38, 32.36)),
                   ((23.02, 18.46), (21.94, 16.36)),
                   ((29.16, 17.14), (19.96, 13.93), (19.50, 13.77)),
                   ((28.53, 17.20), (27.51, 15.59)),
                   ((59.05, 60.92), (57.71, 59.09), (57.42, 58.69), (53.56, 53.22), (53.05, 52.49), (48.01, 45.26),
                    (47.89, 45.08), (44.92, 40.80), (39.66, 33.23), (29.32, 18.47)),
                   ((57.13, 57.19), (47.98, 44.01), (40.67, 33.50), (37.93, 29.56), (37.77, 29.32), (29.47, 17.38)),
                   ((40.70, 42.28), (40.57, 42.00)),
                   ((40.36, 37.91), (40.17, 37.69)),
                   ((31.21, 9.44), (30.25, 9.32), (29.99, 9.17)),
                   ((40.32, 34.71), (40.31, 34.42), (40.45, 34.07)),
                   ((32.96, 11.80), (32.84, 11.93)),
                   ((50.19, 19.71), (40.10, 27.71), (37.77, 29.32)),
                   ((40.85, 42.57), (40.81, 42.40)),
                   ((18.62, 8.40), (18.35, 8.23), (18.31, 8.21), (18.27, 8.19), (18.22, 8.18), (18.18, 8.17),
                    (18.13, 8.16),
                    (18.08, 8.16), (18.04, 8.16), (17.99, 8.16), (17.95, 8.17), (17.90, 8.19), (17.86, 8.20),
                    (17.82, 8.23), (17.78, 8.25), (17.74, 8.28), (17.71, 8.31), (16.30, 9.70))]

    pipes = ()
    for coord_tuple in coordinates:
        pipe_element = (
            IfcBuilder.IfcBuildingElementProxyBuilderImpl(ifc_file, "pipe").assign_to_ifcFile().element_name(
                "Pipe").project_sub_contexts(project.project_sub_contexts).coordinates(coord_tuple).radius(0.3).build())
        pipe_element.create_element_in_ifc_file()
        pipes += (pipe_element.element,)

    ifc_file.createIfcRelContainedInSpatialStructure(

        '1M6hNzVfn0JeEKNuVP5AEI', None,
        None, None,
        pipes, storey.element)

    ifc_file.write("export/test_rothenfluh_new.ifc")


def test_model_created(create_model):
    assert ifc_file != 0
