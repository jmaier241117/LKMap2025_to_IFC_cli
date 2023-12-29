from ifc.IfcDistributionFlowElements import IfcPipeDistributionFlowElement, IfcDuctDistributionFlowElement, \
    IfcSpecialStructureDistributionFlowElement
from ifc.IfcUtils import Uncertainty


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

    def coordinates(self, coordinates):
        self.element.coordinates = coordinates
        return self

    def position_uncertain(self, position_uncertain, default_dimension_value=False):
        self.element.position_uncertain = position_uncertain
        self.element.default_dimension_value = default_dimension_value
        return self

    def height_position_uncertain(self, height_position_uncertain):
        self.element.height_position_uncertain = height_position_uncertain
        return self

    def build(self) -> any:
        self.element.build_representation_element()
        if self.element.position_uncertain == Uncertainty.IMPRECISE:
            self.element.build_representation_uncertainty_imprecise_element()
        elif self.element.position_uncertain == Uncertainty.UNKNOWN:
            self.element.build_representation_uncertainty_unknown_element()
        if self.element.height_position_uncertain == Uncertainty.UNKNOWN:
            self.element.build_height_uncertainty_element()
        self.element.build_style_representation()
        self.element.build_shape_representation()
        self.element.create_element_in_ifc_file()
        return self.element


class IfcDuctElementBuilder(IIfcElementBuilder):
    def __init__(self, ifc_file):
        super().__init__(ifc_file)

    def radius(self, radius):
        # Radius is delivered in mm therefore / 1000
        self.element.radius = radius / 1000
        return self


class IfcPipeElementBuilder(IIfcElementBuilder):
    def __init__(self, ifc_file):
        super().__init__(ifc_file)

    def radius(self, radius):
        # Radius is delivered in mm therefore / 1000
        self.element.radius = radius / 1000
        return self


class IfcSpecialStructureElementBuilder(IIfcElementBuilder):
    def __init__(self, ifc_file):
        super().__init__(ifc_file)

    def thickness(self, thickness):
        self.element.thickness = thickness
        return self
