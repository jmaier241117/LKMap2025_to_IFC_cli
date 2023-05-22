class IIfcElementBuilder:
    def assign_to_ifcFile(self):
        raise NotImplementedError()

    def element_name(self, name):
        raise NotImplementedError()

    def build(self) -> any:
        raise NotImplementedError()
