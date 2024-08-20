import sqlite3
from sqlite3 import Connection, Cursor
from sqlite3 import Cursor

def establish_connection(table_name: str) -> tuple[Connection, Cursor]:
    conn = sqlite3.connect("suspicious_users.db")
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS {tablename} \
                (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER, osservation_thresh INTEGER)".format(tablename=table_name))
    
    return (conn, cur)

def load_db(cur: Cursor, table_name: str) -> dict:
    osservation_user_ids = {}
    cur.execute("SELECT * FROM {tablename}".format(tablename=table_name))
    rows_list = cur.fetchall()
    for row in rows_list:
        osservation_user_ids[row[1]] = row[2]
    
    return osservation_user_ids

def update(cur: Cursor, conn: Connection, table_name: str, user_id: int, osservation_thresh: int):
    query = "UPDATE {tablename} \
             SET osservation_thresh = {osservationthresh} \
             WHERE user_id = {userid}".format(tablename=table_name, userid=user_id, osservationthresh=osservation_thresh)
    cur.execute(query)
    conn.commit()

def insert(cur: Cursor, conn: Connection, table_name: str, user_id: int, osservation_thresh: int):
    query = "INSERT INTO {tablename}(user_id, osservation_thresh) \
             VALUES ({userid}, {osservationthresh})".format(tablename=table_name, userid=user_id, osservationthresh=osservation_thresh)
    cur.execute(query)
    conn.commit()
    