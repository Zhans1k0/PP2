import csv
from connect import get_connection

def create_table():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS contacts (
        id SERIAL PRIMARY KEY,
        name VARCHAR(100),
        phone VARCHAR(20)
    )
    """)

    conn.commit()
    cur.close()
    conn.close()


# 1. Insert from CSV
def insert_from_csv(file):
    conn = get_connection()
    cur = conn.cursor()

    with open(file, newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            cur.execute("INSERT INTO contacts (name, phone) VALUES (%s, %s)", row)

    conn.commit()
    cur.close()
    conn.close()


# 2. Insert from console
def insert_from_console():
    name = input("Enter name: ")
    phone = input("Enter phone: ")

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("INSERT INTO contacts (name, phone) VALUES (%s, %s)", (name, phone))

    conn.commit()
    cur.close()
    conn.close()


# 3. Update contact
def update_contact():
    name = input("Enter name to update: ")
    new_phone = input("Enter new phone: ")

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("UPDATE contacts SET phone=%s WHERE name=%s", (new_phone, name))

    conn.commit()
    cur.close()
    conn.close()


# 4. Query with filters
def query_contacts():
    print("1 - All\n2 - By name\n3 - By phone prefix")
    choice = input("Choose: ")

    conn = get_connection()
    cur = conn.cursor()

    if choice == "1":
        cur.execute("SELECT * FROM contacts")

    elif choice == "2":
        name = input("Enter name: ")
        cur.execute("SELECT * FROM contacts WHERE name=%s", (name,))

    elif choice == "3":
        prefix = input("Enter prefix: ")
        cur.execute("SELECT * FROM contacts WHERE phone LIKE %s", (prefix + "%",))

    rows = cur.fetchall()

    for row in rows:
        print(row)

    cur.close()
    conn.close()


# 5. Delete contact
def delete_contact():
    choice = input("Delete by (1-name / 2-phone): ")

    conn = get_connection()
    cur = conn.cursor()

    if choice == "1":
        name = input("Enter name: ")
        cur.execute("DELETE FROM contacts WHERE name=%s", (name,))

    elif choice == "2":
        phone = input("Enter phone: ")
        cur.execute("DELETE FROM contacts WHERE phone=%s", (phone,))

    conn.commit()
    cur.close()
    conn.close()


# MENU
def menu():
    create_table()

    while True:
        print("\n1.Insert CSV\n2.Insert Console\n3.Update\n4.Query\n5.Delete\n0.Exit")
        choice = input("Choose: ")

        if choice == "1":
            insert_from_csv("contacts.csv")
        elif choice == "2":
            insert_from_console()
        elif choice == "3":
            update_contact()
        elif choice == "4":
            query_contacts()
        elif choice == "5":
            delete_contact()
        elif choice == "0":
            break

if __name__ == "__main__":
    menu()
