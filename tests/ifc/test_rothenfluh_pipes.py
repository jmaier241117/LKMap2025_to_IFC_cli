import ifc.IfcProject as ifc
import ifc.IfcElementBuilderImpls as ifc_element
import ifc.ifc_element_proxy_builder as ifc_proxy

import pytest
import ifcopenshell.guid

ifc_file = ifcopenshell.file()


@pytest.fixture
def create_model():
    project = ifc.IfcProjectBuilder(ifc_file, "Pipe")
    site = ifc_element.IfcSiteBuilder(ifc_file, "Site", project.project_zero_placement)
    building = ifc_element.IfcBuildingBuilder(ifc_file, "Building", project.project_zero_placement)
    storey = ifc_element.IfcBuildingStoreyBuilder(ifc_file, "Storey", project.project_zero_placement)

    ifc_file.createIfcRelAggregates("alskdjfeslda", None, None, None, project.ifc_project, [site.site_element])
    ifc_file.createIfcRelAggregates("alskdjfeslfa", None, None, None, site.site_element, [building.building_element])
    ifc_file.createIfcRelAggregates("alskdjfeslea", None, None, None, building.building_element,
                                    [storey.storey_element])
    coordinates = [{'coord_x': 27.34, 'coord_y': 4.30}, {'coord_x': 19.58, 'coord_y': 13.89},
                   {'coord_x': 29.59, 'coord_y': 17.29}, {'coord_x': 1.82, 'coord_y': 4.27},
                   {'coord_x': 5.31, 'coord_y': 11.45}, {'coord_x': 20.94, 'coord_y': 4.81},
                   {'coord_x': 5.79, 'coord_y': 35.21}]

    chambers = ()
    for coord_tuple in coordinates:
        chamber_element1 = ifc_proxy.IfcBuildingElementProxyCHAMBER(ifc_file, project.project_sub_contexts,
                                                                    coord_tuple, 0.6)
        chambers += (chamber_element1.building_proxy_element,)

    coordinates_and_length = [
        {'coord_x': 29.04, 'coord_y': -2.41, 'length': 0.38, 'vector_x': -0.17, 'vector_y': 0.33},
        {'coord_x': 28.87, 'coord_y': -2.08, 'length': 6.55, 'vector_x': -1.38, 'vector_y': 6.41},
        {'coord_x': 25.38, 'coord_y': 11.95, 'length': 0.48, 'vector_x': -0.24, 'vector_y': -0.42},
        {'coord_x': 25.14, 'coord_y': 11.53, 'length': 2.95, 'vector_x': -1.47, 'vector_y': -2.56},
        {'coord_x': 23.67, 'coord_y': 8.97, 'length': 3.93, 'vector_x': -2.07, 'vector_y': -3.34},
        {'coord_x': 21.59, 'coord_y': 5.64, 'length': 1.06, 'vector_x': -0.65, 'vector_y': -0.83},
        {'coord_x': 20.44, 'coord_y': 4.73, 'length': 0.31, 'vector_x': -0.30, 'vector_y': 0.10},
        {'coord_x': 20.14, 'coord_y': 4.83, 'length': 6.80, 'vector_x': -5.32, 'vector_y': 4.24},
        {'coord_x': 14.83, 'coord_y': 9.07, 'length': 0.33, 'vector_x': -0.28, 'vector_y': 0.19},
        {'coord_x': 14.55, 'coord_y': 9.26, 'length': 2.71, 'vector_x': -2.22, 'vector_y': 1.55},
        {'coord_x': 12.33, 'coord_y': 10.81, 'length': 6.44, 'vector_x': -6.43, 'vector_y': 0.43},
        {'coord_x': 5.90, 'coord_y': 11.24, 'length': 0.63, 'vector_x': -0.59, 'vector_y': 0.21},
        {'coord_x': 1.82, 'coord_y': 4.27, 'length': 10.34, 'vector_x': -4.66, 'vector_y': -9.23},
        {'coord_x': -2.84, 'coord_y': -4.95, 'length': 3.99, 'vector_x': -1.81, 'vector_y': -3.56},
        {'coord_x': 1.98, 'coord_y': 4.38, 'length': 0.19, 'vector_x': -0.16, 'vector_y': -0.11},
        {'coord_x': 1.96, 'coord_y': 4.19, 'length': 0.16, 'vector_x': -0.14, 'vector_y': 0.08},
        {'coord_x': 14.17, 'coord_y': 17.20, 'length': 1.70, 'vector_x': -1.43, 'vector_y': 0.92},
        {'coord_x': 12.75, 'coord_y': 18.12, 'length': 18.18, 'vector_x': -15.28, 'vector_y': 9.84},
        {'coord_x': -2.53, 'coord_y': 27.96, 'length': 8.14, 'vector_x': -6.84, 'vector_y': 4.41},
        {'coord_x': 23.02, 'coord_y': 18.46, 'length': 2.36, 'vector_x': -1.08, 'vector_y': -2.10},
        {'coord_x': 29.16, 'coord_y': 17.14, 'length': 9.75, 'vector_x': -9.21, 'vector_y': -3.22},
        {'coord_x': 19.96, 'coord_y': 13.93, 'length': 0.48, 'vector_x': -0.45, 'vector_y': -0.16},
        {'coord_x': 28.53, 'coord_y': 17.20, 'length': 1.90, 'vector_x': -1.01, 'vector_y': -1.61},
        {'coord_x': 59.05, 'coord_y': 60.92, 'length': 2.27, 'vector_x': -1.34, 'vector_y': -1.83},
        {'coord_x': 57.71, 'coord_y': 59.09, 'length': 0.49, 'vector_x': -0.29, 'vector_y': -0.40},
        {'coord_x': 57.42, 'coord_y': 58.69, 'length': 6.70, 'vector_x': -3.86, 'vector_y': -5.47},
        {'coord_x': 53.56, 'coord_y': 53.22, 'length': 0.89, 'vector_x': -0.51, 'vector_y': -0.73},
        {'coord_x': 53.05, 'coord_y': 52.49, 'length': 8.81, 'vector_x': -5.04, 'vector_y': -7.23},
        {'coord_x': 48.01, 'coord_y': 45.26, 'length': 0.21, 'vector_x': -0.12, 'vector_y': -0.18},
        {'coord_x': 47.89, 'coord_y': 45.08, 'length': 5.21, 'vector_x': -2.97, 'vector_y': -4.28},
        {'coord_x': 44.92, 'coord_y': 40.80, 'length': 9.22, 'vector_x': -5.25, 'vector_y': -7.57},
        {'coord_x': 39.66, 'coord_y': 33.23, 'length': 18.02, 'vector_x': -10.34, 'vector_y': -14.76},
        {'coord_x': 57.13, 'coord_y': 57.19, 'length': 16.05, 'vector_x': -9.16, 'vector_y': -13.18},
        {'coord_x': 47.98, 'coord_y': 44.01, 'length': 12.81, 'vector_x': -7.31, 'vector_y': -10.52},
        {'coord_x': 40.67, 'coord_y': 33.50, 'length': 4.80, 'vector_x': -2.74, 'vector_y': -3.94},
        {'coord_x': 37.93, 'coord_y': 29.56, 'length': 0.29, 'vector_x': -0.17, 'vector_y': -0.24},
        {'coord_x': 37.77, 'coord_y': 29.32, 'length': 14.54, 'vector_x': -8.30, 'vector_y': -11.94},
        {'coord_x': 40.70, 'coord_y': 42.28, 'length': 0.31, 'vector_x': -0.13, 'vector_y': -0.28},
        {'coord_x': 40.36, 'coord_y': 37.91, 'length': 0.29, 'vector_x': -0.19, 'vector_y': -0.22},
        {'coord_x': 31.21, 'coord_y': 9.44, 'length': 0.97, 'vector_x': -0.96, 'vector_y': -0.12},
        {'coord_x': 30.25, 'coord_y': 9.32, 'length': 0.30, 'vector_x': -0.26, 'vector_y': -0.15},
        {'coord_x': 40.32, 'coord_y': 34.71, 'length': 0.29, 'vector_x': 0.00, 'vector_y': -0.29},
        {'coord_x': 40.31, 'coord_y': 34.42, 'length': 0.37, 'vector_x': 0.13, 'vector_y': -0.35},
        {'coord_x': 32.96, 'coord_y': 11.80, 'length': 0.18, 'vector_x': -0.12, 'vector_y': 0.13},
        {'coord_x': 50.19, 'coord_y': 19.71, 'length': 12.87, 'vector_x': -10.08, 'vector_y': 8.00},
        {'coord_x': 40.10, 'coord_y': 27.71, 'length': 2.84, 'vector_x': -2.34, 'vector_y': 1.61},
        {'coord_x': 40.85, 'coord_y': 42.57, 'length': 0.17, 'vector_x': -0.03, 'vector_y': -0.17},
        {'coord_x': 18.62, 'coord_y': 8.40, 'length': 0.32, 'vector_x': -0.27, 'vector_y': -0.16},
        {'coord_x': 18.35, 'coord_y': 8.23, 'length': 0.05, 'vector_x': -0.04, 'vector_y': -0.02},
        {'coord_x': 18.31, 'coord_y': 8.21, 'length': 0.05, 'vector_x': -0.04, 'vector_y': -0.02},
        {'coord_x': 18.27, 'coord_y': 8.19, 'length': 0.05, 'vector_x': -0.04, 'vector_y': -0.01},
        {'coord_x': 18.22, 'coord_y': 8.18, 'length': 0.05, 'vector_x': -0.05, 'vector_y': -0.01},
        {'coord_x': 18.18, 'coord_y': 8.17, 'length': 0.05, 'vector_x': -0.05, 'vector_y': -0.01},
        {'coord_x': 18.13, 'coord_y': 8.16, 'length': 0.05, 'vector_x': -0.05, 'vector_y': 0.00},
        {'coord_x': 18.08, 'coord_y': 8.16, 'length': 0.05, 'vector_x': -0.05, 'vector_y': 0.00},
        {'coord_x': 18.04, 'coord_y': 8.16, 'length': 0.05, 'vector_x': -0.05, 'vector_y': 0.01},
        {'coord_x': 17.99, 'coord_y': 8.16, 'length': 0.05, 'vector_x': -0.05, 'vector_y': 0.01},
        {'coord_x': 17.95, 'coord_y': 8.17, 'length': 0.05, 'vector_x': -0.04, 'vector_y': 0.01},
        {'coord_x': 17.90, 'coord_y': 8.19, 'length': 0.05, 'vector_x': -0.04, 'vector_y': 0.02},
        {'coord_x': 17.86, 'coord_y': 8.20, 'length': 0.05, 'vector_x': -0.04, 'vector_y': 0.02},
        {'coord_x': 17.82, 'coord_y': 8.23, 'length': 0.05, 'vector_x': -0.04, 'vector_y': 0.02},
        {'coord_x': 17.78, 'coord_y': 8.25, 'length': 0.05, 'vector_x': -0.04, 'vector_y': 0.03},
        {'coord_x': 17.74, 'coord_y': 8.28, 'length': 0.05, 'vector_x': -0.03, 'vector_y': 0.03},
        {'coord_x': 17.71, 'coord_y': 8.31, 'length': 1.98, 'vector_x': -1.41, 'vector_y': 1.39},
    ]
    pipes = ()
    for coord_tuple in coordinates_and_length:
        pipe_element = ifc_proxy.IfcBuildingElementProxy(ifc_file, project.project_sub_contexts,
                                                         coord_tuple, 0.3)
        pipes += (pipe_element.building_proxy_element,)

    ifc_file.createIfcRelContainedInSpatialStructure(
        '1M6hNzVfn0JeEKNuVP5AEI', None,
        None, None,
        pipes, storey.storey_element)

    ifc_file.createIfcRelContainedInSpatialStructure(
        '1M6hNzVfn0JeEKNuVP5AFI', None,
        None, None,
        chambers, storey.storey_element)

    ifc_file.write("export/test_pipe_with_swept_disk_solid.ifc")


def test_model_created(create_model):
    assert ifc_file != 0
