import ifcopenshell.guid


class IfcSite:
    def __init__(self, project_file, element_name, element_placement):
        self.project_file = project_file
        self.element_name = element_name
        self.element_placement = element_placement
        self.ifc_element = project_file.createIfcSite(ifcopenshell.guid.new(), None, element_name, None,
                                                      None, element_placement)


class IfcBuilding:
    def __init__(self, project_file, element_name, element_placement):
        self.project_file = project_file
        self.element_name = element_name
        self.element_placement = element_placement
        self.ifc_element = project_file.createIfcBuilding(ifcopenshell.guid.new(), None, element_name,
                                                          None, None,
                                                          element_placement)


class IfcBuildingStorey:
    def __init__(self, project_file, element_name, element_placement):
        self.project_file = project_file
        self.element_name = element_name
        self.element_placement = element_placement
        self.ifc_element = project_file.createIfcBuildingStorey(ifcopenshell.guid.new(), None,
                                                                element_name, None, None,
                                                                element_placement)


class IfcBuildingElementProxyPipe:
    def __init__(self, project_file, element_name, element_shape_def):
        self.project_file = project_file
        self.element_name = element_name
        self.element_shape_def = element_shape_def
        self.ifc_element = project_file.createIfcBuildingElementProxy(ifcopenshell.guid.new(), None, element_name,
                                                                      None, None, None,
                                                                      self.element_shape_def, None,
                                                                      "ELEMENT")


class IfcBuildingElementProxyDuct:
    def __init__(self, project_file, element_name, element_shape_def):
        self.project_file = project_file
        self.element_name = element_name
        self.element_shape_def = element_shape_def
        self.ifc_element = project_file.createIfcBuildingElementProxy(ifcopenshell.guid.new(), None, element_name,
                                                                      None, None, None,
                                                                      self.product_shape_def, None,
                                                                      "ELEMENT")


class IfcDistributionChamberElement:
    def __init__(self, project_file, element_name, project_subcontexts, coord_x, coord_y, element_type):
        self.project_file = project_file
        self.element_name = element_name
        self.project_subcontexts = project_subcontexts
        self.coord_x = coord_x
        self.coord_y = coord_y
        self.element_type = element_type
