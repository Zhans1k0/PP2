import csv
import json
from connect import get_connection


def run_sql_file(filename):
    conn = get_connection()
    cur = conn.cursor()

    with open(filename, "r") as file:
        cur.execute(file.read())

    conn.commit()
    cur.close()
    conn.close()


def get_group_id(group_name):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO groups(name)
        VALUES (%s)
        ON CONFLICT (name) DO NOTHING
    """, (group_name,))

    cur.execute("SELECT id FROM groups WHERE name = %s", (group_name,))
    group_id = cur.fetchone()[0]

    conn.commit()
    cur.close()
    conn.close()

    return group_id


def add_contact():
    name = input("Name: ")
    email = input("Email: ")
    birthday = input("Birthday YYYY-MM-DD: ")
    group_name = input("Group: ")
    phone = input("Phone: ")
    phone_type = input("Phone type home/work/mobile: ")

    group_id = get_group_id(group_name)

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO contacts(name, email, birthday, group_id)
        VALUES (%s, %s, %s, %s)
        RETURNING id
    """, (name, email, birthday, group_id))

    contact_id = cur.fetchone()[0]

    cur.execute("""
        INSERT INTO phones(contact_id, phone, type)
        VALUES (%s, %s, %s)
    """, (contact_id, phone, phone_type))

    conn.commit()
    cur.close()
    conn.close()

    print("Contact added.")


def show_contacts():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT 
            c.id,
            c.name,
            c.email,
            c.birthday,
            g.name,
            p.phone,
            p.type,
            c.created_at
        FROM contacts c
        LEFT JOIN groups g ON c.group_id = g.id
        LEFT JOIN phones p ON c.id = p.contact_id
        ORDER BY c.id
    """)

    rows = cur.fetchall()

    for row in rows:
        print(row)

    cur.close()
    conn.close()


def search_contacts():
    query = input("Search name/email/phone: ")

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM search_contacts(%s)", (query,))
    rows = cur.fetchall()

    for row in rows:
        print(row)

    cur.close()
    conn.close()


def filter_by_group():
    group = input("Group name: ")

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT c.name, c.email, c.birthday, g.name, p.phone, p.type
        FROM contacts c
        LEFT JOIN groups g ON c.group_id = g.id
        LEFT JOIN phones p ON c.id = p.contact_id
        WHERE g.name = %s
    """, (group,))

    rows = cur.fetchall()

    for row in rows:
        print(row)

    cur.close()
    conn.close()


def sort_contacts():
    print("1. Sort by name")
    print("2. Sort by birthday")
    print("3. Sort by created_at")

    choice = input("Choose: ")

    if choice == "1":
        order_by = "c.name"
    elif choice == "2":
        order_by = "c.birthday"
    elif choice == "3":
        order_by = "c.created_at"
    else:
        print("Wrong choice.")
        return

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(f"""
        SELECT c.name, c.email, c.birthday, g.name, p.phone, p.type
        FROM contacts c
        LEFT JOIN groups g ON c.group_id = g.id
        LEFT JOIN phones p ON c.id = p.contact_id
        ORDER BY {order_by}
    """)

    rows = cur.fetchall()

    for row in rows:
        print(row)

    cur.close()
    conn.close()


def pagination():
    limit = 5
    offset = 0

    while True:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
            SELECT c.name, c.email, c.birthday, g.name, p.phone, p.type
            FROM contacts c
            LEFT JOIN groups g ON c.group_id = g.id
            LEFT JOIN phones p ON c.id = p.contact_id
            ORDER BY c.id
            LIMIT %s OFFSET %s
        """, (limit, offset))

        rows = cur.fetchall()

        print("\n--- PAGE ---")
        for row in rows:
            print(row)

        cur.close()
        conn.close()

        command = input("next / prev / quit: ")

        if command == "next":
            offset += limit
        elif command == "prev":
            offset = max(0, offset - limit)
        elif command == "quit":
            break
        else:
            print("Wrong command.")


def add_phone_to_contact():
    name = input("Contact name: ")
    phone = input("New phone: ")
    phone_type = input("Phone type home/work/mobile: ")

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("CALL add_phone(%s, %s, %s)", (name, phone, phone_type))

    conn.commit()
    cur.close()
    conn.close()

    print("Phone added.")


def move_contact_to_group():
    name = input("Contact name: ")
    group = input("New group: ")

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("CALL move_to_group(%s, %s)", (name, group))

    conn.commit()
    cur.close()
    conn.close()

    print("Contact moved.")


def export_json():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT 
            c.id,
            c.name,
            c.email,
            c.birthday,
            g.name,
            p.phone,
            p.type
        FROM contacts c
        LEFT JOIN groups g ON c.group_id = g.id
        LEFT JOIN phones p ON c.id = p.contact_id
        ORDER BY c.id
    """)

    rows = cur.fetchall()

    data = []

    for row in rows:
        data.append({
            "id": row[0],
            "name": row[1],
            "email": row[2],
            "birthday": str(row[3]),
            "group": row[4],
            "phone": row[5],
            "phone_type": row[6]
        })

    with open("contacts.json", "w") as file:
        json.dump(data, file, indent=4)

    cur.close()
    conn.close()

    print("Exported to contacts.json")


def import_json():
    with open("contacts.json", "r") as file:
        data = json.load(file)

    conn = get_connection()
    cur = conn.cursor()

    for item in data:
        name = item["name"]

        cur.execute("SELECT id FROM contacts WHERE name = %s", (name,))
        existing = cur.fetchone()

        if existing:
            action = input(f"{name} already exists. skip/overwrite: ")

            if action == "skip":
                continue

            if action == "overwrite":
                cur.execute("DELETE FROM contacts WHERE name = %s", (name,))

        group_id = get_group_id(item["group"])

        cur.execute("""
            INSERT INTO contacts(name, email, birthday, group_id)
            VALUES (%s, %s, %s, %s)
            RETURNING id
        """, (item["name"], item["email"], item["birthday"], group_id))

        contact_id = cur.fetchone()[0]

        cur.execute("""
            INSERT INTO phones(contact_id, phone, type)
            VALUES (%s, %s, %s)
        """, (contact_id, item["phone"], item["phone_type"]))

    conn.commit()
    cur.close()
    conn.close()

    print("Imported from JSON.")


def import_csv():
    conn = get_connection()
    cur = conn.cursor()

    with open("contacts.csv", "r") as file:
        reader = csv.DictReader(file)

        for row in reader:
            group_id = get_group_id(row["group"])

            cur.execute("""
                INSERT INTO contacts(name, email, birthday, group_id)
                VALUES (%s, %s, %s, %s)
                ON CONFLICT (name) DO NOTHING
                RETURNING id
            """, (row["name"], row["email"], row["birthday"], group_id))

            result = cur.fetchone()

            if result:
                contact_id = result[0]

                cur.execute("""
                    INSERT INTO phones(contact_id, phone, type)
                    VALUES (%s, %s, %s)
                """, (contact_id, row["phone"], row["phone_type"]))

    conn.commit()
    cur.close()
    conn.close()

    print("Imported from CSV.")


def menu():
    while True:
        print("\nPHONEBOOK MENU")
        print("1. Add contact")
        print("2. Show contacts")
        print("3. Search contacts")
        print("4. Filter by group")
        print("5. Sort contacts")
        print("6. Pagination")
        print("7. Add phone")
        print("8. Move to group")
        print("9. Export JSON")
        print("10. Import JSON")
        print("11. Import CSV")
        print("0. Exit")

        choice = input("Choose: ")

        if choice == "1":
            add_contact()
        elif choice == "2":
            show_contacts()
        elif choice == "3":
            search_contacts()
        elif choice == "4":
            filter_by_group()
        elif choice == "5":
            sort_contacts()
        elif choice == "6":
            pagination()
        elif choice == "7":
            add_phone_to_contact()
        elif choice == "8":
            move_contact_to_group()
        elif choice == "9":
            export_json()
        elif choice == "10":
            import_json()
        elif choice == "11":
            import_csv()
        elif choice == "0":
            break
        else:
            print("Wrong choice.")


if __name__ == "__main__":
    run_sql_file("schema.sql")
    run_sql_file("procedures.sql")
    menu()