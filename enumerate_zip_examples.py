names = ['Антон', 'Мария', 'Иван', 'Елена']
phones = ['87771234567', '87001234567', '87779998888', '87775553322']
grades = [85, 92, 78, 96]


print("=== ENUMERATE ===")
for i, name in enumerate(names, 1):
    print(f"{i}. {name}")


print("\nСтуденты с нумерацией:")
for i, (name, grade) in enumerate(zip(names, grades), 1):
    print(f"{i}. {name} - {grade} баллов")


print("\n=== ZIP ===")
for name, phone in zip(names, phones):
    print(f"{name}: {phone}")


phonebook = dict(zip(names, phones))
print(f"\nТелефонная книга: {phonebook}")


print("\n=== ENUMERATE + ZIP ===")
for i, (name, phone, grade) in enumerate(zip(names, phones, grades), 1):
    status = "Отлично" if grade >= 90 else "Хорошо" if grade >= 75 else "Учись лучше"
    print(f"{i}. {name} | {phone} | {grade} баллов - {status}")