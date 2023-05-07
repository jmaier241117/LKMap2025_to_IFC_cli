import unittest

from os.path import exists

import ifcopenshell
import pytest
from typing import Any
from ifcopenshell import file
from ifcopenshell import geom
from ifcopenshell.api import run

ifc_file: file = ifcopenshell.file()


@pytest.fixture
def create_model():
    project = ifc_file.createIfcProject(
        Name='My Project',
        Description='A project',
        ObjectType='IfcProject'
    )

    context = ifc_file.createIfcGeometricRepresentationContext(
        ContextType='Model',
        CoordinateSpaceDimension=3,
        Precision=0.01
    )

    body = run("context.add_context", ifc_file, context_type="ifc_file",
               context_identifier="Body", target_view="MODEL_VIEW", parent=context)

    site = run("root.create_entity", ifc_file, ifc_class="IfcSite", name="My Site")
    building = run("root.create_entity", ifc_file, ifc_class="IfcBuilding", name="Building A")
    storey = run("root.create_entity", ifc_file, ifc_class="IfcBuildingStorey", name="Ground Floor")

    run("aggregate.assign_object", ifc_file, relating_object=project, product=site)
    run("aggregate.assign_object", ifc_file, relating_object=site, product=building)
    run("aggregate.assign_object", ifc_file, relating_object=building, product=storey)

    # create a new IfcPolyline entity
    polyline = ifc_file.create_entity("IfcPolyline")

    # set the coordinates of the line
    points = [(0.0, 0.0, 0.0), (1.0, 0.0, 0.0)]
    polyline.Points = [ifc_file.create_entity("IfcCartesianPoint", Coordinates=point) for point in points]

    # create a new IfcRelContainedInSpatialStructure entity
    rel_contained = ifc_file.create_entity("IfcRelContainedInSpatialStructure")
    rel_contained.RelatingStructure = storey
    rel_contained.RelatedElements = [polyline]

    placement = ifc_file.createIfcAxis2Placement2D(ifc_file.createIfcCartesianPoint((0.0, 0.0)))

    # Create an IfcShapeRepresentation entity with a POLYLINE representation type
    shape_representation = ifc_file.createIfcShapeRepresentation(context, "id", "Curve2D", [polyline])
    spatial_element = ifc_file.createIfcSpatialElement("alskdfj", None, "spatialelement", None, None, placement,
                                                       shape_representation)

    # Create an IfcDistributionSystem
    distribution_system = ifc_file.createIfcDistributionSystem("0kwpywPjv4egYhY$H2Io1T")

    # create the distribution flow element
    distribution_flow_element = ifc_file.createIfcDistributionFlowElement("32bZzvIg5E5Ot5bx5fCCWt",
                                                                          None, "distFlowElement", None,
                                                                          None, placement, shape_representation)

    distribution_flow_element_type = ifc_file.createIfcDistributionFlowElementType("3vhdgIg5E5Ot5bx5fCCWt")
    ifc_file.createIfcRelDefinesByType("32bZzvIg5E5Ot5bx5fCCWu", None, None, None, [distribution_flow_element],
                                       distribution_flow_element_type
                                       )

    rel_contained_in_spatial_structure = ifc_file.createIfcRelContainedInSpatialStructure("3vhdgIg5E5Ot5bx5fCCWy"
                                                                                          , None,
                                                                                          "relspatialstructure", None
                                                                                          , [storey,
                                                                                             distribution_flow_element],
                                                                                          spatial_element)

    ifc_file.add(rel_contained_in_spatial_structure)

    # Create an IFCRELSPACEBOUNDARY entity
    rel_space_boundary = ifc_file.createIfcRelSpaceBoundary(
        "2bQ2y_vlH8vuvlGpKftJNR", None, "spaceboundry", None, storey, distribution_flow_element)

    # save the IFC file
    ifc_file.write("testLINE.ifc")


def test_model_created(create_model):
    assert ifc_file != 0


def test_write_model():
    ifc_file.write("/export/ifc/testLINE.ifc")
    assert exists('/export/ifc/testLINE.ifc')
