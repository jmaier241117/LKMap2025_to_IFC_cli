from itertools import islice


class ColorDefaults:
    def __init__(self, dataset):
        self.dataset = dataset
        self.default_color = (0.2, 0.2, 1)  # Blue RGB(51, 51, 255)
        self.rain_sewage_color = (0.1, 0.5, 0.9)  # Blue-ish RGB(26,122,232)
        self.mixed_sewage_color = (0.51, 0.63, 0.76)  # Grey-Blue RGB(131, 161, 196)
        self.dirty_sewage_color = (0.75, 0.75, 0.75)  # Grey RGB(192, 192, 192)

    def assign_color_to_objects(self) -> any:
        for key in islice(self.dataset.keys(), 1, None):
            if self.dataset[key]['characteristics']['Nutzungsart'] == 'Schmutzabwasser':
                self.dataset[key]['characteristics']['color'] = self.dirty_sewage_color
            elif self.dataset[key]['characteristics']['Nutzungsart'] == 'Mischabwasser':
                self.dataset[key]['characteristics']['color'] = self.mixed_sewage_color
            elif self.dataset[key]['characteristics']['Nutzungsart'] == 'Regenabwasser':
                self.dataset[key]['characteristics']['color'] = self.rain_sewage_color
            else:
                self.dataset[key]['characteristics']['color'] = self.default_color
        return self.dataset
