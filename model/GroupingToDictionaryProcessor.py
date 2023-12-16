import math


class GroupingToDictionaryProcessor():
    def __init__(self, dataset, attributes):
        self.dataset = dataset
        self.attributes = attributes

    def execute_processor(self, lkobject_type) -> any:
        dictionary = {'lkobject_type': lkobject_type}
        for index, row in self.dataset[lkobject_type].iterrows():
            dictionary[row.T_Ili_Tid] = {'attributes': {}}
            lookup_key = lkobject_type + '_object_types'
            dictionary[row.T_Ili_Tid]['attributes']['CHLKMap_Objektart'] = \
                self.attributes[lookup_key][row.objektart]
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
            lkpunkt_dictionary[row.T_Ili_Tid]['attributes'][
                'CHLKMap_Dimension1'] = row.dimension1 if not row.dimension1 else None
            lkpunkt_dictionary[row.T_Ili_Tid]['attributes'][
                'CHLKMap_Dimension2'] = row.dimension2 if not row.dimension2 else None
            lkpunkt_dictionary[row.T_Ili_Tid]['attributes']['CHLKMap_Dimension_Annahme'] = 600.0
            lkpunkt_dictionary[row.T_Ili_Tid]['attributes']['CHLKMap_SymbolOri'] = str(row.symbolori)
        return lkpunkt_dictionary

    def _execute_lklinie_processor(self, lklinie_dictionary) -> any:
        for index, row in self.dataset['lklinie'].iterrows():
            lklinie_dictionary[row.T_Ili_Tid]['attributes']['CHLKMap_Breite'] = row.breite if not row.breite else None
            lklinie_dictionary[row.T_Ili_Tid]['attributes']['CHLKMap_Breite_Annahme'] = 250.0
            lklinie_dictionary[row.T_Ili_Tid]['attributes']['CHLKMap_Profiltyp'] = self.attributes['profile_types'][
                row.profiltyp] if not math.isnan(row.profiltyp) else 'unbekannt'
        return lklinie_dictionary
