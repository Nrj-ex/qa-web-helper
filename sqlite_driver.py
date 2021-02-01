import sqlite3 as sq


def sql_drop_table(bd, name):
    with sq.connect(bd) as con:
        cur = con.cursor()

        cur.execute(f"""DROP TABLE IF EXISTS {name}""")
        print(f"The {name} table has been deleted.")


def sql_execute_request(bd, request):
    with sq.connect(bd) as con:
        cur = con.cursor()

        cur.execute(f"""{request}""")
        con.commit()
        print(f"request done.")


def sql_update(bd, request, entities):
    with sq.connect(bd) as con:
        cur = con.cursor()
        cur.execute(request, entities)
        con.commit()


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
            status_code INTEGER DEFAULT 0,
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

        cur.execute("""SELECT id, url, link, status_code FROM links """)
        return cur.fetchall()

