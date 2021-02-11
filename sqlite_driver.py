import sqlite3 as sq


def create_table(db):
    with sq.connect(db) as con:
        cur = con.cursor()

        cur.execute("""CREATE TABLE IF NOT EXISTS page(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            url TEXT,
            title TEXT,
            description TEXT,
            status_code INTEGER DEFAULT 0,
            level INTEGER,
            history TEXT,
            parents TEXT,
            try INTEGER DEFAULT 0)""")

        cur.execute("""CREATE TABLE IF NOT EXISTS links_list(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    url TEXT,
                    link TEXT,
                    internal INTEGER)""")
    print("The table is created")


def drop_table(db, table):
    with sq.connect(db) as con:
        cur = con.cursor()

        cur.execute(f"""DROP TABLE IF EXISTS {table}""")
        print(f"The {table} table has been deleted.")


def truncate_table(db, table):
    with sq.connect(db) as con:
        cur = con.cursor()
        cur.execute(f"""DELETE FROM {table}""")
        print(f"{table} - cleared.")


def execute_request(con, request):
    cur = con.cursor()
    cur.execute(f"""{request}""")
    con.commit()
    print(f"request done.")


def update(db, request, entities):
    with sq.connect(db) as con:
        cur = con.cursor()
        cur.execute(request, entities)
        con.commit()


def insert(con, entities):
    cur = con.cursor()
    cur.execute('INSERT INTO employees(url, link, title) '
                'VALUES(?, ?, ?)', entities)
    con.commit()


def select(con):
    cur = con.cursor()
    cur.execute("""SELECT id, url, link, status_code FROM links """)
    return cur.fetchall()

