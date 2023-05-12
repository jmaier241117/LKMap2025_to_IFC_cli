import ifcopenshell
from ifcopenshell import file
from ifcopenshell.api import run

# test_with_pytest.py

_model: file = ifcopenshell.open('/import/ifc/Vorderladern.ifc')


def test_ifc_file_opened():
    assert _model != 0


def test_ifc_schema():
    assert _model.schema == 'IFC4'


def test_ifc_project_by_guid_element():
    project = _model.by_guid('30i7SElnjAlgItRP0GGxtR')
    assert project.is_a('IfcProject')


def test_ifc_only_one_project_element():
    project = _model.by_type('IfcProject')
    assert len(project) == 1


def test_ifc_propertieSets():
    buildingElementProxy = model.by_type('IfcBuildingElementProxy')
    type = ifcopenshell.util.element.get_type(buildingElementProxy)

    psets = ifcopenshell.util.element.get_psets(type)
    print(psets)
