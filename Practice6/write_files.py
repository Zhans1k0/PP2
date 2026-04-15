
contacts = [
    "Антон,87771234567",
    "Мария,87001234567",
    "Иван,87779998888"
]

with open('contacts.csv', 'w', encoding='utf-8') as file:
    file.write("name,phone\n")  # заголовок
    for contact in contacts:
        file.write(contact + "\n")

print("Файл создан!")


with open('contacts.csv', 'a', encoding='utf-8') as file:
    file.write("Елена,87775553322\n")

print("Контакт добавлен!")