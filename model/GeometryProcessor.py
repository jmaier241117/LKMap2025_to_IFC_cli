import pyogrio


def _map_geometry_to_dictionary(dataframe) -> any:
    geometry_dictionary = {}
    if not dataframe.empty:
        for index, row in dataframe.iterrows():
            geometry_dictionary[index] = {}
            geometry_dictionary[index]['geometry'] = row.geometry.__geo_interface__['coordinates']
    return geometry_dictionary


class GeometryProcessor:

    def __init__(self, dataset, clipsrc):
        self.dataset = dataset
        self.clipsrc = clipsrc

    def execute_processor(self) -> any:
        if self.clipsrc:
            bbox_tuple = (self.clipsrc[0], self.clipsrc[1], self.clipsrc[2], self.clipsrc[3])
            areas = pyogrio.read_dataframe(self.dataset, layer='lkobjekt', bbox=bbox_tuple, fid_as_index=True)
            lines = pyogrio.read_dataframe(self.dataset, layer='lkobjekt_linie', bbox=bbox_tuple, fid_as_index=True)
            points = pyogrio.read_dataframe(self.dataset, layer='lkobjekt_symbolpos', bbox=bbox_tuple,
                                            fid_as_index=True)
        else:
            areas = pyogrio.read_dataframe(self.dataset, layer='lkobjekt', fid_as_index=True,
                                           where="T_Type == 'lkflaeche'")
            lines = pyogrio.read_dataframe(self.dataset, layer='lkobjekt_linie', fid_as_index=True)
            points = pyogrio.read_dataframe(self.dataset, layer='lkobjekt_symbolpos', fid_as_index=True)
        return {
            'lkflaeche': _map_geometry_to_dictionary(areas),
            'lklinie': _map_geometry_to_dictionary(lines),
            'lkpunkt': _map_geometry_to_dictionary(points),
        }
