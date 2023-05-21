class IIfcElementBuilder:
    def assign_to_ifcFile(self, project_file):
        raise NotImplementedError()

    def element_name(self, name):
        raise NotImplementedError()

    def build(self, element_type) -> any:
        raise NotImplementedError()
