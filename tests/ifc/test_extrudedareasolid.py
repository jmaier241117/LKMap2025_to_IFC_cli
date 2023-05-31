import ifc.IfcProject as IfcProjectBuilder
import ifc.IfcElementBuilderImpls as IfcBuilder

import pytest
import ifcopenshell.guid

ifc_file = ifcopenshell.file()


@pytest.fixture
def create_model():
    project = IfcProjectBuilder.IfcProject(ifc_file, "Extruded Area Solid")
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

    coordinates = [{'coord_x': 27.34, 'coord_y': 4.30}, {'coord_x': 19.58, 'coord_y': 13.89},
                   {'coord_x': 29.59, 'coord_y': 17.29}, {'coord_x': 1.82, 'coord_y': 4.27},
                   {'coord_x': 5.31, 'coord_y': 11.45}, {'coord_x': 20.94, 'coord_y': 4.81},
                   {'coord_x': 5.79, 'coord_y': 35.21}]

    cartesianPointList2D = ifc_file.createIfcCartesianPointList2D(((27.34, 4.30),
                                                                   (27.64, 4.30),
                                                                   (27.64, 4.60),
                                                                   (27.34, 4.60),
                                                                   (27.34, 4.30)
                                                                   ))
    polycurve = ifc_file.createIfcIndexedPolyCurve(cartesianPointList2D)

    arbitrary_closed_polyline = ifc_file.createIfcArbitraryClosedProfileDef('AREA', 'Sammalammintie area', polycurve)

    extruded_area_solid_polyline = ifc_file.createIfcExtrudedAreaSolid(arbitrary_closed_polyline,
                                                                       project.project_zero_points['3D'],
                                                                       ifc_file.createIfcDirection((1.0, 0.0, 0.0)),
                                                                       0.6)
    shape_rep_polyline = ifc_file.createIfcShapeRepresentation(project.project_sub_contexts['body_subcontext'], 'Body',
                                                               'SweptSolid', [extruded_area_solid_polyline])

    line = ifc_file.createIfcLine(ifc_file.createIfcCartesianPoint(
        (29.59, 17.29, 0.0)),
        ifc_file.createIfcVector(
            ifc_file.createIfcDirection((0.0, 0.0, 1.0)), 2.0))
    trimmed_curve = ifc_file.createIfcTrimmedCurve(line,
                                                   [ifc_file.createIfcParameterValue(0.0)],
                                                   [ifc_file.createIfcParameterValue(1.25)],
                                                   True, "PARAMETER")

    arbitrary_closed_trimmed_curve = ifc_file.createIfcArbitraryClosedProfileDef('CURVE', 'curve',
                                                                                 trimmed_curve)

    extruded_area_solid_trimmed_curve = ifc_file.createIfcExtrudedAreaSolid(arbitrary_closed_trimmed_curve,
                                                                            None,
                                                                            ifc_file.createIfcDirection(
                                                                                (1.0, 0.0, 0.0)), 0.6)

    shape_rep_trimmed_curve = ifc_file.createIfcShapeRepresentation(project.project_sub_contexts['body_subcontext'],
                                                                    'Body',
                                                                    'SolidModel', [extruded_area_solid_trimmed_curve])
    bounding_box_of_element = ifc_file.createIfcBoundingBox(
        ifc_file.createIfcCartesianPoint((0.0, 0.0, 0.0)), 2, 2, 50)
    bounding_box_shape_rep = ifc_file.createIfcShapeRepresentation(
        project.project_sub_contexts['box_subcontext'], 'Box', 'BoundingBox', [bounding_box_of_element])
    prod_shape_definition_polyline = ifc_file.createIfcProductDefinitionShape(None, None, (bounding_box_shape_rep,
                                                                                           shape_rep_polyline))

    prod_shape_definition_trimmed_curve = ifc_file.createIfcProductDefinitionShape(None, None, (bounding_box_shape_rep,
                                                                                                shape_rep_trimmed_curve))
    chamber1 = ifc_file.createIfcBuildingElementProxy("asldfjölasdk", None, "piesps",
                                                      None, None, None,
                                                      prod_shape_definition_polyline, None,
                                                      "ELEMENT")

    chamber2 = ifc_file.createIfcBuildingElementProxy("asldfjölasdj", None, "piesps2",
                                                      None, None, None,
                                                      prod_shape_definition_trimmed_curve, None,
                                                      "ELEMENT")

    ifc_file.createIfcRelContainedInSpatialStructure('1M6hNzVfn0JeEKNuVP5AEI', None, None, None, [chamber1, chamber2],
                                                     storey.element)

    ifc_file.write("export/test_extrudedareasolid.ifc")


def test_model_created(create_model):
    assert ifc_file != 0
