class FilterChain:
    def __init__(self, dataset, filter_attributes):
        self.dataset = dataset
        self.filter_attributes = filter_attributes
        self.filters = ()

    def add_filter(self, filter_type):
        self.filters += (filter_type,)

    # def execute_filters(self):
