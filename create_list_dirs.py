import os


os.makedirs('phonebook/data/backup', exist_ok=True)
print("Папки созданы!")


print("Содержимое текущей папки:")
for item in os.listdir('.'):
    if os.path.isdir(item):
        print(f"📁 {item}")
    else:
        print(f"📄 {item}")


print("\nВсе CSV файлы:")
for root, dirs, files in os.walk('.'):
    for file in files:
        if file.endswith('.csv'):
            print(f"  {os.path.join(root, file)}")