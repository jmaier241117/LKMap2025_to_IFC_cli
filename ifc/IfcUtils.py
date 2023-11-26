import ifcopenshell
import ifcopenshell.guid


def relational_aggregates(file, from_element, to_element):
    file.createIfcRelAggregates(ifcopenshell.guid.new(), None, None, None, from_element, [to_element])


def spatial_relations_of_elements(file, elements, spatial_endpoint):
    file.createIfcRelContainedInSpatialStructure(
        ifcopenshell.guid.new(), None,
        None, None,
        elements, spatial_endpoint.element)


def write_ifc_file(file, file_path):
    file.write(file_path)


def create_zero_placement(file):
    return file.createIfcLocalPlacement(None,
                                        file.createIfcAxis2Placement3D(
                                            file.createIfcCartesianPoint(
                                                (0.0, 0.0, 0.0)),
                                            file.createIfcDirection(
                                                (0.0, 0.0, 1.0)),
                                            file.createIfcDirection(
                                                (1.0, 0.0, 0.0))))


def build_shape_rep(file, representation_element, representation_type, geometric_context) -> any:
    shape_rep = file.createIfcShapeRepresentation(geometric_context,
                                                  'Body', representation_type,
                                                  [representation_element])
    bounding_box_of_element = file.createIfcBoundingBox(
        file.createIfcCartesianPoint((0.0, 0.0, 0.0)), 2, 2, 50)
    bounding_box_shape_rep = file.createIfcShapeRepresentation(
        geometric_context, 'Box', 'BoundingBox', [bounding_box_of_element])
    return file.createIfcProductDefinitionShape(None, None, (bounding_box_shape_rep,
                                                             shape_rep))


def build_style_rep(file, representation_element, element_color):
    surface_style_rendering = file.createIfcSurfaceStyleRendering(element_color, 0.0,  # transparency
                                                                  None, None, None, None, None, None,
                                                                  'NOTDEFINED')
    surface_style = file.createIfcSurfaceStyle("style", 'BOTH', [surface_style_rendering])
    file.createIfcStyledItem(representation_element, [surface_style])
