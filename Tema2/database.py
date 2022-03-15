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
    try:
        cursor.execute(sql)
        result = [dict(row) for row in cursor.fetchall()]
    except sqlite3.OperationalError:
        # table not found
        result = dict()
    return result


def get_next_id(table_name):
    global con
    cursor = con.cursor()
    cursor.execute(f"SELECT * FROM {table_name} ORDER BY ID DESC LIMIT 1")
    for row in cursor.fetchall():
        return row['ID']+1


def insert(table_name, data):
    global con
    cursor = con.cursor()
    try:
        cursor.execute(f"SELECT * FROM {table_name}")
    except sqlite3.OperationalError:
        # table not found
        return 0
    columns = ""
    values = ""
    for column in data:
        columns += column+", "
        try:
            values += "\""+data[column]+"\", "
        except TypeError:  # value is not a str
            values += str(data[column]) + ", "
    columns += "ID"
    id = get_next_id(table_name)
    values += str(id)
    sql = f"INSERT INTO {table_name} ({columns}) VALUES({values})"
    try:
        cursor.execute(sql)
        con.commit()
        return id
    except sqlite3.IntegrityError:  # item already exists
        return -1
    except sqlite3.OperationalError: # invalid query
        return -2


def update(table_name, id, data):
    global con
    cursor = con.cursor()
    try:
        cursor.execute(f"SELECT * FROM {table_name} WHERE ID={id}")
    except sqlite3.OperationalError:
        # table not found
        return 0

    sql = f"UPDATE {table_name} SET "
    for column in data:
        try:
            sql += column + " = " + "\"" + data[column] + "\", "
        except TypeError:  # value is not a str
            sql += column + " = " + str(data[column]) + ", "
    sql = sql[:-2]
    sql += f" WHERE ID={id}"
    print(sql)
    try:
        cursor.execute(sql)
        con.commit()
        return 1
    except sqlite3.OperationalError:
        return -1



def delete(table_name, id):
    global con
    cursor = con.cursor()
    try:
        cursor.execute(f"SELECT * FROM {table_name} WHERE ID={id}")
        if not cursor.fetchall():
            # item not found
            return 0
    except sqlite3.OperationalError:
        # table not found
        return 0

    cursor.execute(f"DELETE FROM {table_name} WHERE ID={id}")
    con.commit()
    return 1

