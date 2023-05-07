from os.path import exists

import ifcopenshell
import pytest
from typing import Any
from ifcopenshell import file
from ifcopenshell.api import run
from ifcopenshell.ifcopenshell_wrapper import entity_instance

ifc_file: file = ifcopenshell.file()


@pytest.fixture
def create_model():
    project = ifc_file.createIfcProject(
        Name='My Project',
        Description='A project',
        ObjectType='IfcProject'
    )

    start_point_ifc = ifc_file.createIfcCartesianPoint([0.0, 0.0, 0.0])
    end_point_ifc = ifc_file.createIfcCartesianPoint([10.0, 0.0, 0.0])

    placement = ifc_file.createIfcAxis2Placement3D(start_point_ifc)

    context = ifc_file.createIfcGeometricRepresentationContext(
        ContextType='Model',
        CoordinateSpaceDimension=3,
        Precision=0.01
    )

    polyline = ifc_file.createIfcPolyline([start_point_ifc, end_point_ifc])

    shape_rep = ifc_file.createIfcShapeRepresentation(
        ContextOfItems=context,
        RepresentationIdentifier='Body',
        RepresentationType='Curve'
        # Representations=polyline
    )
    index = entity_instance.get_argument_index(shape_rep.self, "Representations")

    product_definition_shape = ifc_file.createIfcProductDefinitionShape(
        representations=[shape_rep]
    )

    pipe = ifc_file.createIfcPipeSegment(
        Name="My Pipe",
        Description="A pipe",
        ObjectPlacement=placement,
        Representation=product_definition_shape,
        PredefinedType="RIGIDSEGMENT"
    )

    ifc_file.write("my_pipe.ifc")


def test_model_created(create_model):
    assert ifc_file != 0


def test_write_model():
    assert exists('/export/ifc/testpipe.ifc')
