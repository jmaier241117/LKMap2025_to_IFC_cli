import sqlite3
from sqlite3 import Error


def select_eigenschaft_of_line_object(conn, object_id) -> any:
    cur = conn.cursor()
    t_id_query = "SELECT T_Id FROM lkpunkt where T_Ili_Tid = " + object_id
    cur.execute(t_id_query)
    t_id_data = cur.fetchone()
    query_string = "SELECT lkpunkt_eigenschaft, bezeichnung, wert FROM eigenschaften WHERE lkpunkt_eigenschaft = " + str(
        t_id_data[0])
    cur.execute(query_string)
    rows = cur.fetchall()
    characteristics = ()
    for row in rows:
        characteristics += (row,)
    return characteristics
