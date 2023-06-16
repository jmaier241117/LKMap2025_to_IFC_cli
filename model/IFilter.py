class IFilter:
    def __init__(self, dataset, filter_attribute):
        self.dataset = dataset
        self.filter_attribute = filter_attribute
        
    def execute_filter(self) -> any:
        raise NotImplementedError()
