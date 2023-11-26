import sqlite3
from sqlite3 import Error


class AttributeProcessor:
    def __init__(self, dataset):
        self.dataset = dataset
        self.gpkg_connection = _create_connection(dataset)

    def execute_processor(self) -> any:
        attribute_types = {
            'lkflaeche_object_types': self._get_attribute_types('lkflaeche_objektart'),
            'lkpunkt_object_types': self._get_attribute_types('lkpunkt_objektart'),
            'lklinie_object_types': self._get_attribute_types('lklinie_objektart'),
            'status_types': self._get_attribute_types('astatus'),
            'position_declaration_types': self._get_attribute_types('bestimmungswert'),
            'profile_types': self._get_attribute_types('lklinie_profiltyp'),
            'organizations': self._get_organizations(),
        }
        return attribute_types

    def _get_attribute_types(self, table_name) -> any:
        cur = self.gpkg_connection.cursor()
        query_string = "SELECT T_Id, iliCode FROM " + table_name
        cur.execute(query_string)
        rows = cur.fetchall()
        attribute_types = {}
        for row in rows:
            attribute_types[row[0]] = row[1]
        return attribute_types

    def _get_organizations(self) -> any:
        cur = self.gpkg_connection.cursor()
        query_string = "SELECT T_Id, bezeichnung FROM organisation"
        cur.execute(query_string)
        rows = cur.fetchall()
        organizations = {}
        for row in rows:
            organizations[row[0]] = row[1]
        return organizations


def _create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)
    return conn
