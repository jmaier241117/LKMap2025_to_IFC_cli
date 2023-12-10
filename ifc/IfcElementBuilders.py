from ifc.IfcDistributionFlowElements import IfcPipeDistributionFlowElement, IfcDuctDistributionFlowElement, \
    IfcSpecialStructureDistributionFlowElement


class IIfcElementBuilder:
    def __init__(self, ifc_file):
        if isinstance(self, IfcPipeElementBuilder):
            self.element = IfcPipeDistributionFlowElement(ifc_file)
        elif isinstance(self, IfcDuctElementBuilder):
            self.element = IfcDuctDistributionFlowElement(ifc_file)
        elif isinstance(self, IfcSpecialStructureElementBuilder):
            self.element = IfcSpecialStructureDistributionFlowElement(ifc_file)

    def geometric_context(self, geometric_context):
        self.element.geometric_context = geometric_context
        return self

    def element_name(self, name):
        self.element.element_name = name
        return self

    def element_color(self, color_tuple):
        self.element.element_color = color_tuple
        return self

    def coordinates(self, coordinates):
        self.element.coordinates = coordinates
        return self

    def position_uncertain(self, position_uncertain):
        self.element.position_uncertain = position_uncertain
        return self

    def height_position_uncertain(self, height_position_uncertain):
        self.element.height_position_uncertain = height_position_uncertain
        return self

    def build(self) -> any:
        raise NotImplementedError()


class IfcDuctElementBuilder(IIfcElementBuilder):
    def __init__(self, ifc_file):
        super().__init__(ifc_file)

    def radius(self, radius):
        self.element.radius = radius
        return self

    def build(self) -> any:
        self.element.build_representation_element()
        self.element.build_style_representation()
        self.element.build_shape_representation()
        self.element.create_element_in_ifc_file()
        return self.element


class IfcPipeElementBuilder(IIfcElementBuilder):
    def __init__(self, ifc_file):
        super().__init__(ifc_file)

    def radius(self, radius):
        self.element.radius = radius
        return self

    def build(self) -> any:
        self.element.build_representation_element()
        self.element.build_style_representation()
        self.element.build_shape_representation()
        self.element.create_element_in_ifc_file()
        return self.element


class IfcSpecialStructureElementBuilder(IIfcElementBuilder):
    def __init__(self, ifc_file):
        super().__init__(ifc_file)

    def thickness(self, thickness):
        self.element.thickness = thickness
        return self

    def build(self) -> any:
        self.element.build_representation_element()
        self.element.build_style_representation()
        self.element.build_shape_representation()
        self.element.create_element_in_ifc_file()
        return self.element
