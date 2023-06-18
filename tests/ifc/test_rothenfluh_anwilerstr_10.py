import ifc.IfcFileBuilder as IfcProjectBuilder
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

    chamber_coordinates = [((27.34, 4.30)), ((19.58, 13.89)),
                           ((29.59, 17.29)), ((1.82, 4.27)),
                           ((5.31, 11.45)), ((20.94, 4.81)),
                           ((5.79, 35.21))]
    chambers = ()
    for coord_tuple in chamber_coordinates:
        chamber_element = (
            IfcBuilder.IfcDistributionFlowElementBuilderImpl(ifc_file,
                                                             "duct").assign_to_ifcFile().element_name(
                "Chamber")
            .project_sub_contexts(project.project_sub_contexts).coordinates(coord_tuple).radius(0.6).build()
        )
        chamber_element.create_element_in_ifc_file()
        chambers += (chamber_element.element,)

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
            IfcBuilder.IfcDistributionFlowElementBuilderImpl(ifc_file, "pipe").assign_to_ifcFile().element_name(
                "Pipe").project_sub_contexts(project.project_sub_contexts).coordinates(
                coord_tuple).radius(0.3).build())
        pipe_element.create_element_in_ifc_file()
        pipes += (pipe_element.element,)

    special_structure_coordinates = [(
        (19.04, 14.07), (19.02, 14.03), (19.01, 14.00), (18.99, 13.96), (18.99, 13.92), (18.98, 13.88), (18.98, 13.84),
        (18.98, 13.80), (18.99, 13.75), (19.00, 13.71), (19.02, 13.67),
        (19.04, 13.63), (19.06, 13.59), (19.08, 13.55), (19.11, 13.51), (19.15, 13.48), (19.18, 13.45), (19.22, 13.42),
        (19.26, 13.39), (19.30, 13.36), (19.34, 13.34), (19.39, 13.32), (19.43, 13.31), (19.48, 13.30), (19.52, 13.29),
        (19.57, 13.29), (19.61, 13.28), (19.66, 13.29), (19.70, 13.29), (19.74, 13.30),
        (19.78, 13.32), (19.82, 13.34), (19.85, 13.36), (19.88, 13.38), (19.91, 13.41), (19.94, 13.44), (19.96, 13.47),
        (19.98, 13.50), (20.00, 13.54), (20.01, 13.57), (20.02, 13.61), (20.02, 13.66), (20.02, 13.70), (20.02, 13.74),
        (20.01, 13.78), (20.00, 13.82), (19.99, 13.86), (19.97, 13.90), (19.95, 13.94), (19.92, 13.98), (19.89, 14.02),
        (19.86, 14.05), (19.82, 14.09), (19.79, 14.12), (19.75, 14.14), (19.71, 14.17), (19.66, 14.19), (19.62, 14.21),
        (19.58, 14.22), (19.53, 14.24), (19.48, 14.24), (19.44, 14.25), (19.39, 14.25), (19.35, 14.25), (19.31, 14.24),
        (19.27, 14.23), (19.23, 14.22), (19.19, 14.20), (19.15, 14.18), (19.12, 14.15), (19.09, 14.13),
        (19.06, 14.10), (19.04, 14.07)),
        ((27.60, 3.79), (27.64, 3.80), (27.67, 3.81), (27.71, 3.83), (27.74, 3.85), (27.77, 3.88), (27.80, 3.91),
         (27.83, 3.94), (27.85, 3.98), (27.88, 4.01), (27.90, 4.05), (27.91, 4.09), (27.92, 4.14), (27.93, 4.18),
         (27.94, 4.23), (27.94, 4.28), (27.94, 4.33), (27.93, 4.37), (27.92, 4.42), (27.91, 4.47), (27.90, 4.51),
         (27.88, 4.56), (27.86, 4.60), (27.83, 4.64), (27.81, 4.68), (27.78, 4.71), (27.75, 4.74), (27.71, 4.77),
         (27.68, 4.80), (27.64, 4.82), (27.60, 4.84), (27.57, 4.85), (27.53, 4.86), (27.49, 4.87), (27.45, 4.87),
         (27.41, 4.87), (27.37, 4.86), (27.33, 4.85), (27.30, 4.84), (27.26, 4.82), (27.23, 4.80), (27.19, 4.77),
         (27.17, 4.75), (27.14, 4.71), (27.11, 4.68), (27.09, 4.64), (27.07, 4.60), (27.06, 4.56), (27.05, 4.51),
         (27.04, 4.47), (27.03, 4.42), (27.03, 4.38), (27.03, 4.33), (27.04, 4.28), (27.04, 4.23), (27.06, 4.19),
         (27.07, 4.14), (27.09, 4.10), (27.11, 4.05), (27.13, 4.01), (27.16, 3.98), (27.19, 3.94), (27.22, 3.91),
         (27.25, 3.88), (27.29, 3.85), (27.33, 3.83), (27.36, 3.81), (27.40, 3.80), (27.44, 3.79), (27.48, 3.78),
         (27.52, 3.78), (27.56, 3.78), (27.60, 3.79)),
        ((29.80, 17.82), (29.77, 17.84), (29.73, 17.86), (29.70, 17.88), (29.66, 17.89), (29.62, 17.90),
         (29.58, 17.90), (29.53, 17.90), (29.49, 17.89), (29.45, 17.88), (29.41, 17.87), (29.36, 17.86), (29.32, 17.84),
         (29.28, 17.81), (29.24, 17.79), (29.21, 17.76), (29.17, 17.73), (29.14, 17.69), (29.11, 17.65), (29.08, 17.61),
         (29.06, 17.57), (29.04, 17.53), (29.02, 17.49), (29.00, 17.44), (28.99, 17.40), (28.98, 17.35), (28.98, 17.31),
         (28.98, 17.26), (28.98, 17.22), (28.99, 17.18), (29.00, 17.14), (29.02, 17.10), (29.03, 17.06), (29.06, 17.03),
         (29.08, 17.00), (29.11, 16.97), (29.14, 16.94), (29.17, 16.92), (29.20, 16.90), (29.24, 16.89), (29.28, 16.88),
         (29.32, 16.87), (29.36, 16.87), (29.40, 16.87), (29.45, 16.87), (29.49, 16.88), (29.53, 16.89), (29.57, 16.91),
         (29.61, 16.93), (29.65, 16.95), (29.69, 16.98), (29.73, 17.01), (29.76, 17.04), (29.80, 17.07), (29.83, 17.11),
         (29.85, 17.15), (29.88, 17.19), (29.90, 17.23), (29.92, 17.28), (29.93, 17.32), (29.95, 17.37), (29.95, 17.41),
         (29.96, 17.46), (29.96, 17.50), (29.95, 17.54), (29.95, 17.59), (29.93, 17.63), (29.92, 17.67), (29.90, 17.70),
         (29.88, 17.74), (29.86, 17.77), (29.83, 17.80), (29.80, 17.82)),
        ((28.99, 18.68), (27.17, 15.80), (27.85, 15.38), (29.66, 18.25), (28.99, 18.68)),
        ((3.41, 3.66), (3.35, 3.55), (5.53, 2.36), (5.59, 2.47), (3.41, 3.66))]

    specials = ()
    for coord_tuple in special_structure_coordinates:
        special_element = (
            IfcBuilder.IfcDistributionFlowElementBuilderImpl(ifc_file,
                                                             "other_structure").assign_to_ifcFile().element_name(
                "Special").project_sub_contexts(project.project_sub_contexts).coordinates(coord_tuple).build())
        special_element.create_element_in_ifc_file()
        specials += (special_element.element,)

    ifc_file.createIfcRelContainedInSpatialStructure(
        '1M6hNzVfn0JeEKNuVP5AEI', None,
        None, None,
        pipes, storey.element)

    ifc_file.createIfcRelContainedInSpatialStructure(
        '1M6hNzVfn0JeEKNuVP5AFI', None,
        None, None,
        chambers, storey.element)

    ifc_file.createIfcRelContainedInSpatialStructure(
        '1M6hNzVfn0JeEKNuVP5AGI', None,
        None, None,
        specials, storey.element)

    ifc_file.write("export/test_rothenfluh-anwiler-all.ifc")


def test_model_created(create_model):
    assert ifc_file != 0
