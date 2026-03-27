from connect import connect

def call_search(pattern):
    conn = connect()
    cur = conn.cursor()

    cur.execute("SELECT * FROM search_contacts(%s)", (pattern,))
    print(cur.fetchall())

    conn.close()


def call_upsert(name, phone):
    conn = connect()
    cur = conn.cursor()

    cur.execute("CALL upsert_contact(%s, %s)", (name, phone))
    conn.commit()

    conn.close()


def call_delete(value):
    conn = connect()
    cur = conn.cursor()

    cur.execute("CALL delete_contact(%s)", (value,))
    conn.commit()

    conn.close()
