import sqlite3
from sqlite3 import Error

from model import DBUtils


class GroupingToDictionaryProcessor:
    def __init__(self, dataset):
        self.dataset = dataset

    def execute_processor(self, lkobject_type, geometries) -> any:
        dictionary = {'lkobject_type': lkobject_type}
        DBUtils.gpkg_connection.row_factory = sqlite3.Row
        for element_id in geometries:
            query_string = "SELECT * FROM lkobjekt where T_Id =" + str(element_id)
            cur = DBUtils.gpkg_connection.execute(query_string)
            for row in cur:
                dictionary[row['T_Id']] = {'attributes': {}}
                dictionary[row['T_Id']]['attributes']['T_Ili_Tid'] = row['T_Ili_Tid']
                dictionary[row['T_Id']]['attributes']['CHLKMap_Objektart'] = row['objektart1']
                dictionary[row['T_Id']]['attributes']['CHLKMap_Lagebestimmung'] = row['lagebestimmung']
                dictionary[row['T_Id']]['attributes']['CHLKMap_Letzte_Aenderung'] = row['letzte_aenderung']
                dictionary[row['T_Id']]['attributes']['CHLKMap_Eigentuemer'] = row['eigentuemerref']
                dictionary[row['T_Id']]['attributes']['CHLKMap_Hoehenbestimmung'] = row['hoehenbestimmung']
                dictionary[row['T_Id']]['attributes']['CHLKMap_Status'] = row['astatus']
                dictionary[row['T_Id']]['geometry'] = geometries[row['T_Id']]['geometry']
                if lkobject_type == 'lklinie':
                    dictionary = self._execute_lklinie_processor(dictionary, row)
                elif lkobject_type == 'lkpunkt':
                    dictionary = self._execute_lkpunkt_processor(dictionary, row)
        return dictionary

    def _execute_lkpunkt_processor(self, lkpunkt_dictionary, row) -> any:
        lkpunkt_dictionary[row['T_Id']]['attributes']['CHLKMap_Dimension1'] = row['dimension1']
        lkpunkt_dictionary[row['T_Id']]['attributes']['CHLKMap_Dimension2'] = row['dimension2']
        lkpunkt_dictionary[row['T_Id']]['attributes']['CHLKMap_Dimension_Annahme'] = 600.0
        lkpunkt_dictionary[row['T_Id']]['attributes']['CHLKMap_SymbolOri'] = row['symbolori']
        return lkpunkt_dictionary

    def _execute_lklinie_processor(self, lklinie_dictionary, row) -> any:
        lklinie_dictionary[row['T_Id']]['attributes']['CHLKMap_Breite'] = row['breite']
        lklinie_dictionary[row['T_Id']]['attributes']['CHLKMap_Breite_Annahme'] = 250.0
        lklinie_dictionary[row['T_Id']]['attributes']['CHLKMap_Profiltyp'] = row['profiltyp']
        return lklinie_dictionary

