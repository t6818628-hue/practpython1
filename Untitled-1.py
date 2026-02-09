import json

country_data = {
    "страна": "россия",
    "столица": "москва",
    "население": 1000000,
    "площадь": 232323
}

with open('country.json', 'w', encoding='utf-8') as file:
    json.dump(country_data, file, ensure_ascii=False, indent=2)

with open('country.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

data["язык"] = "русский"

with open('country.json', 'w', encoding='utf-8') as file:
    json.dump(data, file, ensure_ascii=False, indent=2)

print("файл country.json обновлен. добавлен ключ 'язык'.")
print(json.dumps(data, ensure_ascii=False, indent=2))
import csv
import os

test_data = {
    "Имя": "артем",
    "Возраст": "18",
    "Город": "москва"
}

with open('test_json.json', 'w', encoding='utf-8') as file:
    json.dump(test_data, file, ensure_ascii=False, indent=2)

with open('test_json.json', 'r', encoding='utf-8') as file:
    json_data = json.load(file)

csv_row = [
    json_data["Имя"],
    json_data["Возраст"], 
    json_data["Город"],
    "Стажёр",
    "50000"
]

file_exists = os.path.exists('employees_with_salary.csv')

with open('employees_with_salary.csv', 'a', encoding='utf-8', newline='') as file:
    writer = csv.writer(file)
    if not file_exists:
        headers = ["Имя", "Возраст", "Город", "Должность", "Зарплата"]
        writer.writerow(headers)
    writer.writerow(csv_row)

print("данные добавлены в файл employees_with_salary.csv")
print("добавленная строка:")
print(csv_row)

if os.path.exists('employees_with_salary.csv'):
    print("\nсодержимое файла employees_with_salary.csv:")
    with open('employees_with_salary.csv', 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        for row_num, row in enumerate(reader, 1):
            print(f'строка {row_num}: {row}')