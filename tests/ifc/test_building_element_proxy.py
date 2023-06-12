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

    cartesianPointList2D = ifc_file.createIfcCartesianPointList2D(((19.04, 14.07),
                                                                   (19.02, 14.03),
                                                                   (19.01, 14.00),
                                                                   (18.99, 13.96),
                                                                   (18.99, 13.92),
                                                                   (18.98, 13.88),
                                                                   (18.98, 13.84),
                                                                   (18.98, 13.80),
                                                                   (18.99, 13.75),
                                                                   (19.00, 13.71),
                                                                   (19.02, 13.67),
                                                                   (19.04, 13.63),
                                                                   (19.06, 13.59),
                                                                   (19.08, 13.55),
                                                                   (19.11, 13.51),
                                                                   (19.15, 13.48),
                                                                   (19.18, 13.45),
                                                                   (19.22, 13.42),
                                                                   (19.26, 13.39),
                                                                   (19.30, 13.36),
                                                                   (19.34, 13.34),
                                                                   (19.39, 13.32),
                                                                   (19.43, 13.31),
                                                                   (19.48, 13.30),
                                                                   (19.52, 13.29),
                                                                   (19.57, 13.29),
                                                                   (19.61, 13.28),
                                                                   (19.66, 13.29),
                                                                   (19.70, 13.29),
                                                                   (19.74, 13.30),
                                                                   (19.78, 13.32),
                                                                   (19.82, 13.34),
                                                                   (19.85, 13.36),
                                                                   (19.88, 13.38),
                                                                   (19.91, 13.41),
                                                                   (19.94, 13.44),
                                                                   (19.96, 13.47),
                                                                   (19.98, 13.50),
                                                                   (20.00, 13.54),
                                                                   (20.01, 13.57),
                                                                   (20.02, 13.61),
                                                                   (20.02, 13.66),
                                                                   (20.02, 13.70),
                                                                   (20.02, 13.74),
                                                                   (20.01, 13.78),
                                                                   (20.00, 13.82),
                                                                   (19.99, 13.86),
                                                                   (19.97, 13.90),
                                                                   (19.95, 13.94),
                                                                   (19.92, 13.98),
                                                                   (19.89, 14.02),
                                                                   (19.86, 14.05),
                                                                   (19.82, 14.09),
                                                                   (19.79, 14.12),
                                                                   (19.75, 14.14),
                                                                   (19.71, 14.17),
                                                                   (19.66, 14.19),
                                                                   (19.62, 14.21),
                                                                   (19.58, 14.22),
                                                                   (19.53, 14.24),
                                                                   (19.48, 14.24),
                                                                   (19.44, 14.25),
                                                                   (19.39, 14.25),
                                                                   (19.35, 14.25),
                                                                   (19.31, 14.24),
                                                                   (19.27, 14.23),
                                                                   (19.23, 14.22),
                                                                   (19.19, 14.20),
                                                                   (19.15, 14.18),
                                                                   (19.12, 14.15),
                                                                   (19.09, 14.13),
                                                                   (19.06, 14.10),
                                                                   (19.04, 14.07)))
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
    swept_disk_solid = ifc_file.createIfcSweptDiskSolid(composite_curve, 0.0025)
    plane = ifc_file.createIfcPlane(placement)
    curve_bounded_plane = ifc_file.createIfcCurveBoundedPlane(plane, polycurve)

    # 300= IFCRAILWAY('1CWLdx$bDBleY2a_KBTJBy',#10,'Railway',$,$,#3,#314,$,$);
    # 301= IFCCARTESIANPOINT((560.762,875.053));
    # 302= IFCCARTESIANPOINT((576.255,982.428));
    # 303= IFCCARTESIANPOINT((599.756,979.115));
    # 304= IFCCARTESIANPOINT((594.173,939.512));
    # 305= IFCCARTESIANPOINT((584.602,871.613));
    # 306= IFCCARTESIANPOINT((560.762,875.053));
    # 307= IFCPOLYLINE((#301,#302,#303,#304,#305,#306));
    # 308= IFCARBITRARYCLOSEDPROFILEDEF(.AREA.,'Railway area',#307);
    # 309= IFCCARTESIANPOINT((0.0,0.0,100.0));
    # 310= IFCAXIS2PLACEMENT3D(#309,$,$);
    # 311= IFCDIRECTION((0.0,0.0,1.0));
    # 312= IFCEXTRUDEDAREASOLID(#308,#310,#311,40.0);
    # 313= IFCSHAPEREPRESENTATION(#24,'Body','SweptSolid',(#312));
    # 314= IFCPRODUCTDEFINITIONSHAPE($,$,(#313));
    arbitrary_closed_profile = ifc_file.createIfcArbitraryClosedProfileDef('AREA', 'area', polycurve)
    direction = ifc_file.createIfcDirection((0.0, 0.0, 1.0))
    extruded_area_solid = ifc_file.createIfcExtrudedAreaSolid(arbitrary_closed_profile, placement, direction, 5.0)
    shape_rep = ifc_file.createIfcShapeRepresentation(project.project_sub_contexts['body_subcontext'], 'Body',
                                                      'SweptSolid',
                                                      [extruded_area_solid])
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

    ifc_file.write("export/test_spezial_bauwerk.ifc")


def test_model_created(create_model):
    assert ifc_file != 0
