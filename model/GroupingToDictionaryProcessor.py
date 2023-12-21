import pyogrio


class GroupingToDictionaryProcessor:
    def __init__(self, dataset):
        self.dataset = dataset
        self.organisations = self._get_organisations()

    def execute_processor(self, lkobject_type, geometries) -> any:
        dictionary = {'lkobject_type': lkobject_type}
        for element_id in geometries:
            data = pyogrio.read_dataframe(self.dataset, layer='lkobjekt', read_geometry=False,
                                          where='T_Id = ' + str(element_id), fid_as_index=True)
            for index, row in data.iterrows():
                dictionary[index] = {'attributes': {}}
                dictionary[index]['attributes']['T_Ili_Tid'] = row.T_Ili_Tid
                dictionary[index]['attributes']['CHLKMap_Objektart'] = row.objektart1
                dictionary[index]['attributes']['CHLKMap_Lagebestimmung'] = row.lagebestimmung
                dictionary[index]['attributes']['CHLKMap_Letzte_Aenderung'] = str(row.letzte_aenderung.date())
                dictionary[index]['attributes']['CHLKMap_Eigentuemer'] = self.organisations[row.eigentuemerref]
                dictionary[index]['attributes']['CHLKMap_Hoehenbestimmung'] = row.hoehenbestimmung
                dictionary[index]['attributes']['CHLKMap_Status'] = row.astatus
                dictionary[index]['geometry'] = geometries[index]['geometry']
                if lkobject_type == 'lklinie':
                    dictionary = self._execute_lklinie_processor(dictionary, index, row)
                elif lkobject_type == 'lkpunkt':
                    dictionary = self._execute_lkpunkt_processor(dictionary, index, row)
        return dictionary

    def _execute_lkpunkt_processor(self, lkpunkt_dictionary, index, row) -> any:
        lkpunkt_dictionary[index]['attributes']['CHLKMap_Dimension1'] = row.dimension1
        lkpunkt_dictionary[index]['attributes']['CHLKMap_Dimension2'] = row.dimension2
        lkpunkt_dictionary[index]['attributes']['CHLKMap_Dimension_Annahme'] = 600.0
        lkpunkt_dictionary[index]['attributes']['CHLKMap_SymbolOri'] = row.symbolori
        return lkpunkt_dictionary

    def _execute_lklinie_processor(self, lklinie_dictionary, index, row) -> any:
        lklinie_dictionary[index]['attributes']['CHLKMap_Breite'] = row.breite
        lklinie_dictionary[index]['attributes']['CHLKMap_Breite_Annahme'] = 250.0
        lklinie_dictionary[index]['attributes']['CHLKMap_Profiltyp'] = row.profiltyp
        return lklinie_dictionary

    def _get_organisations(self) -> any:
        organisations = pyogrio.read_dataframe(self.dataset, layer='organisation', fid_as_index=True)
        organisations_dictionary = {}
        if not organisations.empty:
            for index, row in organisations.iterrows():
                organisations_dictionary[index] = row.bezeichnung
        return organisations_dictionary
