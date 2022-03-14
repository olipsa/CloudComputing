import sqlite3
con = None


def connect():
    global con
    con = sqlite3.connect('library.sqlite', check_same_thread=False)
    print("Connected to db.")
    con.row_factory = sqlite3.Row


def close():
    global con
    con.close()


def select(table_name, **kwargs):
    global con
    cursor = con.cursor()
    sql = f"SELECT * FROM {table_name}"
    if len(kwargs) != 0:
        sql += " WHERE "
        for col_name in kwargs:
            sql += f"{col_name}={kwargs[col_name]}"
    print(sql)
    try:
        cursor.execute(sql)
        result = [dict(row) for row in cursor.fetchall()]
    except sqlite3.OperationalError:
        # table not found
        result = dict()
    return result


def insert(table_name):
    pass


def delete(table_name, id):
    global con
    cursor = con.cursor()
    cursor.execute(f"SELECT * FROM {table_name} WHERE ID={id}")
    if not cursor.fetchall():
        # item not found
        return 0
    try:
        sql = f"DELETE FROM {table_name} WHERE ID={id}"
        cursor.execute(sql)
        print(sql)
        con.commit()
        return 1
    except sqlite3.OperationalError:
        # table not found
        return 0
