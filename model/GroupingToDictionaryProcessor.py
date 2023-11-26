class GroupingToDictionaryProcessor():
    def __init__(self, dataset, attributes):
        self.dataset = dataset
        self.attributes = attributes

    def execute_lkpunkt_processor(self) -> any:
        lkpunkt_dictionary = {'lkobject_type': 'lkpunkt'}
        for index, row in self.dataset['point_objects'].iterrows():
            lkpunkt_dictionary[row.T_Ili_Tid] = {'attributes': {}}
            lkpunkt_dictionary[row.T_Ili_Tid]['attributes']['CHLKMap_Objektart'] = \
                self.attributes['lkpunkt_object_types'][row.objektart]
            lkpunkt_dictionary[row.T_Ili_Tid]['attributes']['CHLKMap_Lagebestimmung'] = \
                self.attributes['position_declaration_types'][
                    row.lagebestimmung]
            lkpunkt_dictionary[row.T_Ili_Tid]['attributes']['CHLKMap_Letzte_Aenderung'] = row.letzte_aenderung
            lkpunkt_dictionary[row.T_Ili_Tid]['attributes']['CHLKMap_Eigentuemer'] = \
                self.attributes['organizations'][row.eigentuemerref]
            lkpunkt_dictionary[row.T_Ili_Tid]['attributes']['CHLKMap_Hoehenbestimmung'] = row.hoehenbestimmung
            lkpunkt_dictionary[row.T_Ili_Tid]['attributes']['CHLKMap_Status'] = self.attributes['status_types'][
                row.astatus]
            lkpunkt_dictionary[row.T_Ili_Tid]['attributes']['CHLKMap_Dimension1'] = str(row.dimension1)
            lkpunkt_dictionary[row.T_Ili_Tid]['attributes']['CHLKMap_Dimension2'] = str(row.dimension2)
            lkpunkt_dictionary[row.T_Ili_Tid]['attributes']['CHLKMap_Dimension_Annahme'] = str(row.dimension_annahme)
            lkpunkt_dictionary[row.T_Ili_Tid]['attributes']['CHLKMap_SymbolOri'] = str(row.symbolori)
            lkpunkt_dictionary[row.T_Ili_Tid]['geometry'] = row.geometry.__geo_interface__['coordinates']
        return lkpunkt_dictionary

    def execute_lklinie_processor(self) -> any:
        lklinie_dictionary = {'lkobject_type': 'lklinie'}
        for index, row in self.dataset['line_objects'].iterrows():
            lklinie_dictionary[row.T_Ili_Tid] = {'attributes': {}}
            lklinie_dictionary[row.T_Ili_Tid]['attributes']['CHLKMap_Objektart'] = self.attributes['lklinie_object_types'][
                row.objektart]
            lklinie_dictionary[row.T_Ili_Tid]['attributes']['CHLKMap_Lagebestimmung'] = \
            self.attributes['position_declaration_types'][
                row.lagebestimmung]
            lklinie_dictionary[row.T_Ili_Tid]['attributes']['CHLKMap_Letzte_Aenderung'] = row.letzte_aenderung
            lklinie_dictionary[row.T_Ili_Tid]['attributes']['CHLKMap_Eigentuemer'] = self.attributes['organizations'][
                row.eigentuemerref]
            lklinie_dictionary[row.T_Ili_Tid]['attributes']['CHLKMap_Hoehenbestimmung'] = row.hoehenbestimmung
            lklinie_dictionary[row.T_Ili_Tid]['attributes']['CHLKMap_Status'] = self.attributes['status_types'][row.astatus]
            lklinie_dictionary[row.T_Ili_Tid]['attributes']['CHLKMap_Breite'] = str(row.breite)
            lklinie_dictionary[row.T_Ili_Tid]['attributes']['CHLKMap_Breite_Annahme'] = str(row.breite_annahme)
            lklinie_dictionary[row.T_Ili_Tid]['attributes']['CHLKMap_Profiltyp'] = self.attributes['profile_types'][
                row.profiltyp]
            lklinie_dictionary[row.T_Ili_Tid]['geometry'] = row.geometry.__geo_interface__['coordinates']
        return lklinie_dictionary

    def execute_lkflaeche_processor(self) -> any:
        lkflaeche_dictionary = {'lkobject_type': 'lkflaeche'}
        for index, row in self.dataset['area_objects'].iterrows():
            lkflaeche_dictionary[row.T_Ili_Tid] = {'attributes': {}}
            lkflaeche_dictionary[row.T_Ili_Tid]['attributes']['CHLKMap_Objektart'] = \
            self.attributes['lkflaeche_object_types'][
                row.objektart]
            lkflaeche_dictionary[row.T_Ili_Tid]['attributes']['CHLKMap_Lagebestimmung'] = \
            self.attributes['position_declaration_types'][
                row.lagebestimmung]
            lkflaeche_dictionary[row.T_Ili_Tid]['attributes']['CHLKMap_Letzte_Aenderung'] = row.letzte_aenderung
            lkflaeche_dictionary[row.T_Ili_Tid]['attributes']['CHLKMap_Eigentuemer'] = self.attributes['organizations'][
                row.eigentuemerref]
            lkflaeche_dictionary[row.T_Ili_Tid]['attributes']['CHLKMap_Hoehenbestimmung'] = row.hoehenbestimmung
            lkflaeche_dictionary[row.T_Ili_Tid]['attributes']['CHLKMap_Status'] = self.attributes['status_types'][row.astatus]
            lkflaeche_dictionary[row.T_Ili_Tid]['geometry'] = row.geometry.__geo_interface__['coordinates']
        return lkflaeche_dictionary
