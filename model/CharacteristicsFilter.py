import sqlite3
from sqlite3 import Error

from model.IProcessor import IProcessor


class CharacteristicsProcessor(IProcessor):
    def execute_filter(self) -> any:
        gpkg_connection = _create_connection(self.dataset)
        return _get_characteristics_of_objects(gpkg_connection, self.filter_attribute['obj_id'],
                                               self.filter_attribute['lkobject_type'])


def _get_characteristics_of_objects(conn, object_id, lkobject_type) -> any:
    cur = conn.cursor()
    query_string = "SELECT bezeichnung, wert FROM eigenschaften WHERE " + lkobject_type + "_eigenschaft = (SELECT T_Id FROM " + lkobject_type + " WHERE T_Ili_Tid = '" + object_id + "')"
    cur.execute(query_string)
    rows = cur.fetchall()
    characteristics = {}
    for row in rows:
        characteristics[row[0]] = row[1]
    return characteristics


def _create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)
    return conn
