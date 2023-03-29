from typing import Any

import ifcopenshell
import pytest
from ifcopenshell import file
from ifcopenshell.api import run

# test_with_pytest.py

_model: file = ifcopenshell.file()
_project: Any = run("root.create_entity", _model, ifc_class="IfcProject", name="My _project")


# Arrange
@pytest.fixture
def create_model():
    run("unit.assign_unit", _model)

    context = run("context.add_context", _model, context_type="_model")

    body = run("context.add_context", _model, context_type="_model",
               context_identifier="Body", target_view="MODEL_VIEW", parent=context)

    site = run("root.create_entity", _model, ifc_class="IfcSite", name="My Site")
    building = run("root.create_entity", _model, ifc_class="IfcBuilding", name="Building A")
    storey = run("root.create_entity", _model, ifc_class="IfcBuildingStorey", name="Ground Floor")

    run("aggregate.assign_object", _model, relating_object=_project, product=site)
    run("aggregate.assign_object", _model, relating_object=site, product=building)
    run("aggregate.assign_object", _model, relating_object=building, product=storey)

    wall = run("root.create_entity", _model, ifc_class="IfcWall")
    representation = run("geometry.add_wall_representation", _model, context=body, length=5, height=3, thickness=0.2)
    run("geometry.assign_representation", _model, product=wall, representation=representation)

    run("spatial.assign_container", _model, relating_structure=storey, product=wall)


def test_ifc_file_created():
    assert _model != 0


def test_ifc_project_element_created(create_model):
    assert _project != 0


def test_write_model():
    _model.write('/export/ifc/testModel.ifc')
