class GroupingToDictionaryProcessor():
    def __init__(self, dataset, attributes):
        self.dataset = dataset
        self.attributes = attributes

    def execute_standard_processor(self, lkobject_type) -> any:
        dictionary = {'lkobject_type': lkobject_type}
        for index, row in self.dataset[lkobject_type].iterrows():
            dictionary[row.T_Ili_Tid] = {'attributes': {}}
            dictionary[row.T_Ili_Tid]['attributes']['CHLKMap_Objektart'] = \
                self.attributes['lkflaeche_object_types'][row.objektart]
            dictionary[row.T_Ili_Tid]['attributes']['CHLKMap_Lagebestimmung'] = \
                self.attributes['position_declaration_types'][row.lagebestimmung]
            dictionary[row.T_Ili_Tid]['attributes']['CHLKMap_Letzte_Aenderung'] = row.letzte_aenderung
            dictionary[row.T_Ili_Tid]['attributes']['CHLKMap_Eigentuemer'] = \
                self.attributes['organizations'][
                    row.eigentuemerref]
            dictionary[row.T_Ili_Tid]['attributes']['CHLKMap_Hoehenbestimmung'] = row.hoehenbestimmung
            dictionary[row.T_Ili_Tid]['attributes']['CHLKMap_Status'] = self.attributes['status_types'][
                row.astatus]
            dictionary[row.T_Ili_Tid]['geometry'] = row.geometry.__geo_interface__['coordinates']
        if lkobject_type == 'lkpunkt':
            dictionary = self._execute_lkpunkt_processor(dictionary)
        elif lkobject_type == 'lklinie':
            dictionary = self._execute_lklinie_processor(dictionary)
        return dictionary

    def _execute_lkpunkt_processor(self, lkpunkt_dictionary) -> any:
        for index, row in self.dataset['lkpunkt'].iterrows():
            lkpunkt_dictionary[row.T_Ili_Tid]['attributes']['CHLKMap_Dimension1'] = str(row.dimension1)
            lkpunkt_dictionary[row.T_Ili_Tid]['attributes']['CHLKMap_Dimension2'] = str(row.dimension2)
            lkpunkt_dictionary[row.T_Ili_Tid]['attributes']['CHLKMap_Dimension_Annahme'] = str(row.dimension_annahme)
            lkpunkt_dictionary[row.T_Ili_Tid]['attributes']['CHLKMap_SymbolOri'] = str(row.symbolori)
        return lkpunkt_dictionary

    def _execute_lklinie_processor(self, lklinie_dictionary) -> any:
        for index, row in self.dataset['lklinie'].iterrows():
            lklinie_dictionary[row.T_Ili_Tid]['attributes']['CHLKMap_Breite'] = str(row.breite)
            lklinie_dictionary[row.T_Ili_Tid]['attributes']['CHLKMap_Breite_Annahme'] = str(row.breite_annahme)
            lklinie_dictionary[row.T_Ili_Tid]['attributes']['CHLKMap_Profiltyp'] = self.attributes['profile_types'][
                row.profiltyp]
        return lklinie_dictionary
