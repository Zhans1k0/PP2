import shutil
import os


shutil.copy('contacts.csv', 'contacts_backup.csv')
print("Файл скопирован!")


if os.path.exists('contacts_backup.csv'):
    os.remove('contacts_backup.csv')
    print("Файл удалён!")
else:
    print("Файл не найден")


if os.path.exists('contacts.csv'):
    os.rename('contacts.csv', 'my_phonebook.csv')
    print("Файл переименован!")