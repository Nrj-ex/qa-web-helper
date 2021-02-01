import sqlite3 as sq
from settings import *


def create_table(bd):
    with sq.connect(bd) as con:
        cur = con.cursor()

        cur.execute("""DROP TABLE IF EXISTS links""")
        cur.execute("""CREATE TABLE IF NOT EXISTS links(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            url TEXT,
            link TEXT,
            title TEXT,
            description TEXT,
            status INTEGER DEFAULT 0,
            assert TEXT,
            try INTEGER DEFAULT 0)""")
    print("The table is created")


def sql_insert(con, entities):
    cur = con.cursor()

    cur.execute('INSERT INTO employees(url, link, title) '
                      'VALUES(?, ?, ?)', entities)

    con.commit()

def select(bd):
    with sq.connect(bd) as con:
        cur = con.cursor()

        cur.execute("""SELECT id, url, link, status FROM links """)
        return cur.fetchall()


create_table(BD)


